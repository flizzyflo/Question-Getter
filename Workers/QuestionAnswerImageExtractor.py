import os
import re
from typing import List

import requests
from pathlib import Path
from bs4 import ResultSet, Tag
from Settings.Settings import DELIMITER, COOKIES, HEADERS, PARAMS, QUESTION_ID
from utils.SpaceScanner import find_formula_start_idx_in


class QuestionAnswerImageExtractor:

    """
    Class is used to manage the whole question, answer and image scraping-process from the respective webpage. 
    """

    def __init__(self, *, question_divs: ResultSet, correct_answers_divs: ResultSet, image_storage_path: Path) -> None:

        # self.set_image_storage_part(image_storage_path=image_storage_path)
        self._unique_question_codes: list[str] = list()
        self._questions: list[str] = list()
        self._correct_answers: list[str] = list()
        self._results: dict[str, str] = dict()
        self._question_divs: ResultSet = question_divs
        self._correct_answers_divs: ResultSet = correct_answers_divs
    

    def set_image_storage_part(self, image_storage_path: Path) -> None:
        """
        Sets the image storage part as instance variable. Checks whether the path for the image folder already exists. 
        If not, it will create the respective folder.

        Args:
            image_storage_path (Path): Path to a folder where the images for the respective questions should be stored later on.
        """

        if not image_storage_path.exists():
            os.makedirs(name=image_storage_path)

        self._image_storage_path = image_storage_path


    def get_image_storage_path(self) -> Path:
        return self._image_storage_path
    

    def get_question_divs(self) -> ResultSet:
        return self._question_divs
    

    def get_correct_answers_divs(self) -> ResultSet:
        return self._correct_answers_divs


    def get_unique_question_code(self, index: int) -> str:
        return self._unique_question_codes[index]


    def get_unique_question_codes(self) -> list[str]:
        return self._unique_question_codes


    def get_question(self, index: int) -> str:
        return self._questions[index]


    def get_questions(self) -> list[str]:
        return self._questions


    def get_correct_answer(self, index: int) -> list[str]:
        return self._correct_answers[index]


    def get_correct_answers(self) -> list[str]:
        return self._correct_answers


    def get_results(self) -> dict[str, str]:
        """
        Accessor function the the final results. Results are filled by calling the generate_results() method
        at a respective instance of this class.

        Returns:
            dict[str, str]: Key is the unique question code, value is a string containing the question and the answer to 
            that question. Both are separated by a specific delimiter to be transfered into csv format later on.
        """

        return self._results


    def generate_results(self) -> None:
            """
            Wrapperfunction to be called to perform extraction of question codes, questions, answers, images and storing the results into the 
            results dictionary of the respective class instance.
            """

            assert isinstance(self._question_divs, ResultSet)
            assert isinstance(self._correct_answers_divs, ResultSet)

            self.__extract_unique_question_codes()
            self.__extract_questions()
            self.__extract_correct_answers()
            self.__match_results()    


    def __extract_unique_question_codes(self) -> None:
        """
        Extracts all the unique question codes for every question. These codes will be used as keys for the questions to avoid duplicates
        as well as mapping the images to the questions as well.
        """
        global QUESTION_ID
        selection_div: Tag

        for selection_div in self.get_question_divs():
            #### commentend, since works different here
            # unique_question_code: str = selection_div.find("div", {"class": "qtext"}).find("small").text
            # self._unique_question_codes.append(unique_question_code)


            self._unique_question_codes.append(QUESTION_ID)
            QUESTION_ID += 1



    def __extract_questions(self, html_element_to_download: str = "img") -> None:
        """
        Takes in all extracted question divs and extracts the questions out of them. 
        If an image is stored within the question div, this information is passed on to a helper mehtod which  will store the image as well.

        Args:
            selection_divs (list[ResultSet]): Extracted result set containing all the  question divs from the website.
            Each question div contains the question itself and several other information.
            html_element_to_download (str): Element to look for which should be downloaded
        """

        # questions start with introduction text and question number. is filtered with this regex
        # format looks like [KE01:054b], whereas the last letter - b in this case - is optional
        selection_div: ResultSet
        unique_question_code_pattern: str = r"(Fragetext\[[A-Z]{2}\d{2}:\d{3}[a-z]{0,1}\])"
        formula_contents: List[str] = list()

        for question_number, selection_div in enumerate(self.get_question_divs(), 1):

            question_text: str = selection_div.text
            q = selection_div.get_text()
            #
            formula_spans = selection_div.contents[2].find_all("span", class_="MathJax_Preview")

            if len(formula_spans) > 0:
                formula_contents = [sp.find("img").get("alt") for sp in formula_spans]


            irrelevant_intro_text = len("Fragetext")
            irrelevant_outro_text = len(f"Frage {question_number} AntwortRichtig Keine Antwort Falsch")
            ### commentent
            # irrelevant_intro_text: int = re.match(pattern=unique_question_code_pattern, string=question_text).span()[1] # grab lenght of the text to be eliminated
            
            # question text with  unnecessary leading introductary text removed
            question_text = question_text[irrelevant_intro_text:]
            question_text = question_text[:len(question_text) - irrelevant_outro_text - 4]

            if formula_contents:
                formula_start_indices: List[int] = find_formula_start_idx_in(question_text)
                former_formula_length: int = 0
                for formula_start_idx, formula_content in zip(formula_start_indices, formula_contents):
                    first_part_of_string = question_text[:formula_start_idx + former_formula_length].strip()
                    second_part_of_string = question_text[formula_start_idx + former_formula_length:].lstrip()
                    question_text = f"{first_part_of_string} {formula_content} {second_part_of_string}"
                    former_formula_length += len(formula_content)
                formula_contents.clear()
            # image is within the current div, needs to be extracted
          #  if selection_div.find(html_element_to_download):
          #      self.__extract_and_store_image(selection_div)

            # replace delimiter to ensure correct csv creation. replace other unnecessary text as well
            question_text = question_text.replace(DELIMITER, ":").replace("__________", "").strip()
            self._questions.append(question_text)


    def __extract_and_store_image(self, page_element: Tag) -> None:
        """
        This function takes in an html-page element, detects the image tag within. It will send an request to the 
        respective url of the image and store the image as jpg file to the harddisk. Path for storage is saved as instance variable.

        Args:
            page_element (Tag): Page element containing an image. 
        """

        unique_question_code_for_image_name: str = self.__get_relevant_question_code_for_image()
        image_url: str = self.__extract_url_from(page_element=page_element) # extract the url from the html tag

        
        # not a relevant image, no need to store and function ends here
        if not ".jpg" in image_url.lower() and not ".png" in image_url.lower():
            return
        
        response = self.__download_html_element(element_url=image_url, 
                                                cookies=COOKIES, 
                                                headers=HEADERS, 
                                                params=PARAMS, 
                                                current_question_name=unique_question_code_for_image_name)
        
        unique_question_code_for_image_name = unique_question_code_for_image_name.replace(":", "_") # replace non-allowed characters for filename
        image_path: Path = Path(f"{os.path.join(self.get_image_storage_path(), unique_question_code_for_image_name)}.jpg")

        with open(image_path, "wb") as image_file:
            image_file.write(response.content)

        print(f"Image for question '{unique_question_code_for_image_name}' loaded and stored succesfully at the desired path!")


    def __get_relevant_question_code_for_image(self) -> str:
        """
        Question code is used to name the downloaded file. This allowes to connect the downloaded file to a specific question.
        This function extracts the relevant question code for the specific downloaded file to be able to match
        item and question later on.

        Returns:
            str: The unique question identifier code used as name for the downloaded file
        """        

        # relevant question code is at indexposition of the last question in the question list, since 
        # it is extracted before the current question is appended to the question list
        current_number_of_questions: int = len(self.get_questions())
        question_code: int = current_number_of_questions if current_number_of_questions > 0 else 0
        unique_question_code: str = self.get_unique_question_code(index=question_code)

        return unique_question_code


    def __extract_url_from(self, *, page_element: Tag, html_tag_type: str = "img", html_tag_attribute: str = "src") -> str:
        """
        Extracts the URL of a specific page element passed in as argument and returns the url as a string.

        Args:
            page_element (Tag): beautifulsoup Tag object of the specific html tag where the url should be extracted from
            tag_type (str, optional): exact description of the html tag where the URL should be extracted from; set to 'img' per default.
            tag_attribute (str, optional): Attribute which stores the URL within the html tag; set to 'src' per default

        Returns:
            str: URL stored at the given @tag_attribute within the html element
        """      

        html_tag: Tag = page_element.find(html_tag_type)
        extracted_url: str = html_tag[html_tag_attribute] # grabs the URL from the tag_attribute

        return extracted_url
    

    def __download_html_element(self, *, element_url: str, cookies: dict[str, str], headers: dict[str, str], params: dict[str, str], current_question_name: str) -> requests.Response:
        """
        Downloads and stores a specific element as a response object. 

        Args:
            element_url (str): URL of the element to be downloaded
            cookies (dict[str, str]): required cookies to access the URL where the element is stored at
            headers (dict[str, str]): required headers to access the URL where the element is stored at
            params (dict[str, str]): required other parameters to access the URL where the element is stored at
            current_question_name (str): unique question code where the element belongs to. Is just used to print a failure if response != 200 

        Returns:
            requests.Response: downloaded element from URL given as requests.Response object
        """        
        
        response: requests.Response = requests.get(url=element_url, 
                                                   cookies=cookies, 
                                                   headers=headers, 
                                                   params=params)
        
        if not response.status_code == 200:
            print(f"Could not connect to URL for image related to question '{current_question_name}' - download aborted and nothing is stored. HTTP Answer-Statuscode: {response.status_code}")
            return

        return response


    def __extract_correct_answers(self) -> None: 
        """
        Extracts the correct answer from the respective answer div and stores them into a list.

        Args:
            correct_answer_divs (ResultSet): all divs containing the answer
        """

        for correct_anwser_div in self.get_correct_answers_divs():
            correct_answer = correct_anwser_div.text.split(":")[1].strip()
            self._correct_answers.append(correct_answer)


    def __match_results(self) -> None:
        """
        Function matches the extracted questions, answers and unique question codes togehter within a dictionary.
        Dictionary has the unique question codes as keys, the answers and questions are put together as a string and
        were appended to the respective key.
        """

        elements_to_extract: int = min(len(self.get_unique_question_codes()), len(self.get_questions()), len(self.get_correct_answers()))
        for index_position in range(elements_to_extract):
            current_question_code = self.get_unique_question_code(index_position)
            current_question = self.get_question(index_position)
            current_answer = self.get_correct_answer(index_position)
            self._results[current_question_code] = f"{current_question}{DELIMITER} {current_answer}"



