import os
import requests
from pathlib import Path
from bs4 import ResultSet, Tag
from Settings.Settings import DELIMITER, COOKIES, HEADERS, PARAMS
import re

class QuestionAnswerImageExtractor:

    """
    Class is used to manage the whole question, answer and image scraping from the respective webpage. 
    """

    def __init__(self, *, selection_divs: ResultSet, correct_answers_divs: ResultSet, image_storage_path: Path) -> None:

        self._image_storage_path: Path = image_storage_path
        self._unique_question_codes: list[str] = list()
        self._questions: list[str] = list()
        self._correct_answers: list[str] = list()
        self._results: dict[str, str] = dict()
        self._selection_divs: ResultSet = selection_divs
        self._correct_answers_divs: ResultSet = correct_answers_divs
    
    def get_image_storage_path(self) -> Path:
        return self._image_storage_path
    
    def get_selection_divs(self) -> ResultSet:
        return self._selection_divs
    
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
        return self._results


    def __extract_unique_question_codes(self) -> None:
        
        """
        Extracts all the unique question codes for every question. These codes will be used as keys for the questions to avoid duplicates
        as well as mapping the images to the questions as well.
        """
        selection_div: Tag
        for selection_div in self.get_selection_divs():
            unique_question_code: str = selection_div.find("div", {"class": "qtext"}).find("small").text
            self._unique_question_codes.append(unique_question_code)



    def __extract_questions(self) -> None:
        """
        Takes in all extracted question divs and extracts the questions out of them. 
        If an image is stored within the question div, this information is passed on to a helper mehtod which  will store the image as well.

        Args:
            selection_divs (list[ResultSet]): Extracted result set containing all the  question divs from the website.
            Each question div contains the question itself and several other information.

        """

        # questions start with introduction text and question number. is filtered with this regex
        # format looks like [KE01:054b], whereas the last letter - b in this case - is optional
        re_pattern: str = r"(Fragetext\[[A-Z]{2}\d{2}:\d{3}[a-z]{0,1}\])"
        selection_div: ResultSet
        questions: list[str] = list()

        for selection_div in self.get_selection_divs():
            question_text: str = selection_div.text
            irrelevant_intro_text: int = re.match(pattern=re_pattern, 
                                                  string=question_text).span()[1] # grab lenght of the text to be eliminated
            
            # question text without unnecessary leading introductary text
            question_text = question_text[irrelevant_intro_text:]

            # image is within the current div, needs to be extracted
            if selection_div.find("img"):
                self.__extract_and_store_image(selection_div)

            # replace delimiter to ensure correct csv creation. replace other unnecessary text as well
            question_text = question_text.replace(DELIMITER, ":").replace("__________", "")
            self._questions.append(question_text)
            

        if question_text not in questions:
            self._questions.append(question_text)


    def __extract_correct_answers(self) -> None: 
        """
        Extracts the correct answer from the respective answer div and stores them into a list.

        Args:
            correct_answer_divs (ResultSet): all divs containing the answer

        """

        for correct_anwser_div in self.get_correct_answers_divs():
            correct_answer = correct_anwser_div.text.split(":")[1]
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


    def generate_results(self) -> None:
        """
        Wrapperfunction to be called to perform extraction of question codes, questions, answers, images and storing the results into the 
        results dictionary of the respective class instance.

        """

        self.__extract_unique_question_codes()
        self.__extract_questions()
        self.__extract_correct_answers()
        self.__match_results()    


    def __extract_and_store_image(self, page_element: Tag) -> None:
        """
        This function takes in an html-page element, detects the image tag within. It will send an request to the 
        respective url of the image and store the image as jpg file to the harddisk. Path for storage is saved as instance variable.

        Args:
            page_element (Tag): Page element containing an image. 
        """

        # question code is key to link the image to the question
        # relevant question code is at indexposition of the last question in the question list, since 
        # it is extracted before the current question is appended to the question list
        question_code = (len(self.get_questions())) if len(self.get_questions()) > 0 else 0
        unique_question_code: str = self.get_unique_question_code(index= question_code)

        image_element: Tag = page_element.find("img")
        image_url: str = image_element["src"]

        # not a relevant image, no need to store and function ends here
        if not ".jpg" in image_url.lower():
            return
        
        response: requests.Response = requests.get(url=image_url, 
                                                   cookies=COOKIES, 
                                                   headers=HEADERS, 
                                                   params=PARAMS)
        
        if not response.status_code == 200:
            print(unique_question_code, "-Bild konnte nicht heruntergeladen werden. HTTP Response: ", response.status_code)
            return
        
        unique_question_code = unique_question_code.replace(":", "_") # replace non-allowed characters for filename
        image_path: Path = Path(f"{os.path.join(self.get_image_storage_path(), unique_question_code)}.jpg")

        with open(image_path, "wb") as image_file:
            image_file.write(response.content)

        print("Bild zu '" + unique_question_code + "' erfolgreich geladen und gespeichert.")

