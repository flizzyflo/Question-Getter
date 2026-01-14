import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup, ResultSet

from Workers.QuestionAnswerImageExtractor import QuestionAnswerImageExtractor
from Workers.FileWriting import FileHandler
from Settings.Settings import COURSES, URL, COURSE_NUMBER, COOKIES, HEADERS, PARAMS, CSV_FILE_PATH, IMAGE_FILE_PATH, COURSE_NAMES


def get_relevant_html(response: requests.Response = None) -> tuple[ResultSet]:
    """
    Wrapper function to encapsulate the beautiful soup logic which extracts the relevant html information for the
    later processing of the data.

    Returns:
        tuple[ResultSet]: Returning a tuple of bs4.Result sets. First element in tuple is the selection div result set,
        which contains all the question related information. Second element are the correct answers for the respective question.
    """

    soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
    selection_divs: ResultSet = soup.find_all("div", {"class": "formulation clearfix" })
    correct_answer_divs: ResultSet = soup.find_all("div", {"class": "rightanswer"})

    return selection_divs, correct_answer_divs


def extract_questions_for(*, attempt: int) -> dict[str, str]:
    """
    Extracts all questions for a specific attempt and stores the questions into the respective file for the course unit.
    

    Args:
        attempt (int): the number of the attepmt to extract the questions for

    Returns:
        dict[str, str]: Returns the raw results, having the question code as key and both, the questions and answer, als value of the dictionary.
    """    

    PARAMS['attempt'] = attempt
    response = requests.get(URL,
                             cookies=COOKIES,
                             headers=HEADERS,
                             params=PARAMS)
    
    if not response.status_code == 200:
        print(f"Could not connecto to {URL} for attempt {attempt} - request is aborted. HTTP Answer-Statuscode: {response.status_code}")
        return
    
    question_divs, correct_answer_divs = get_relevant_html(response=response)
    extractor = QuestionAnswerImageExtractor(question_divs=question_divs,
                                             correct_answers_divs=correct_answer_divs,
                                             image_storage_path=IMAGE_FILE_PATH)

    extractor.generate_results()  
    raw_result = extractor.get_results()

    return raw_result
    


if __name__ == "__main__":

    # variable declaration
    attempts: list[int]
    correct_answer_divs: ResultSet
    question_divs: ResultSet
    response: requests.Response
    extractor: QuestionAnswerImageExtractor
    raw_result: dict[str, str]
    clean_results: dict[str, str]
    
    # selected course attempts
    attempts = COURSES[COURSE_NUMBER]
    FILEPATH_FOR_CSV=Path(f"results{os.sep}{COURSE_NAMES[COURSE_NUMBER]}_{CSV_FILE_PATH}")


    # loop through all attempts in a single course unit
    for attempt in attempts:
        raw_result = extract_questions_for(attempt=attempt)

        FileHandler.store_results(results=raw_result,
                                  questions_csv_file_path=FILEPATH_FOR_CSV)

    FileHandler.filter_duplicates_from_stored_file(FILEPATH_FOR_CSV)
        
    print("-" * 20)
    print(f"Extractions for course '{COURSE_NUMBER}' are done. All detected images are saved as well.")
