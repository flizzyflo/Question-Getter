from typing import Union, Dict

import requests

from Settings.Settings import PARAMS, URL, COOKIES, HEADERS, IMAGE_FILE_PATH
from Workers.QuestionAnswerImageExtractor import QuestionAnswerImageExtractor
from utils.HtmlScraper import get_relevant_html


def extract_questions_for(*, current_attempt: int) -> Union[Dict[str, str], None]:
    """
    Extracts all questions for a specific attempt and stores the questions into the respective file for the course unit.


    Args:
        current_attempt (int): the number of the attepmt to extract the questions for

    Returns:
        dict[str, str]: Returns the raw results, having the question code as key and both, the questions and answer, als value of the dictionary.
    """

    PARAMS['attempt'] = current_attempt
    current_response = requests.get(URL,
                                    cookies=COOKIES,
                                    headers=HEADERS,
                                    params=PARAMS)

    if not current_response.status_code == 200:
        print(f"Could not connecto to {URL} for attempt {current_attempt} - request is aborted. HTTP Answer-Statuscode: {current_response.status_code}")
        return None

    else:

        question_divs, correct_answer_divs = get_relevant_html(current_response=current_response)
        extractor = QuestionAnswerImageExtractor(question_divs=question_divs,
                                                 correct_answers_divs=correct_answer_divs,
                                                 image_storage_path=IMAGE_FILE_PATH)

        extractor.generate_results()
        raw_result = extractor.get_results()

        return raw_result
