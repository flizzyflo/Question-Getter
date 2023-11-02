import requests
from bs4 import BeautifulSoup, ResultSet

from Workers.QuestionAnswerImageExtraction import QuestionAnswerImageExtractor
from Workers.FileWriting import write_results_to_file, filter_duplicates_from_scraped_results
from Settings.Settings import URL, COURSE_NUMBER, COOKIES, HEADERS, PARAMS, CSV_FILE_PATH, IMAGE_FILE_PATH, KE_1_attempts, KE_2_attempts


def get_relevant_html() -> tuple[ResultSet]:
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


if __name__ == "__main__":

    attempts: list[str]
    correct_answer_divs: ResultSet
    question_divs: ResultSet
    response: requests.Response
    extractor: QuestionAnswerImageExtractor
    raw_result: dict[str, str]
    clean_results: dict[str, str]

    attempts = KE_1_attempts
    for attempt in attempts:
        PARAMS['attempt'] = attempt
        response = requests.get(URL, 
                                cookies=COOKIES, 
                                headers=HEADERS, 
                                params=PARAMS)
        
        if not response.status_code == 200:
            print(f"Could not connecto to {URL} for attempt {attempt} - request is aborted. HTTP Answer-Statuscode: {response.status_code}")
            continue

        question_divs, correct_answer_divs = get_relevant_html()
        extractor = QuestionAnswerImageExtractor(question_divs=question_divs,
                                                 correct_answers_divs=correct_answer_divs,
                                                 image_storage_path=IMAGE_FILE_PATH)
        extractor.generate_results()  
        raw_result = extractor.get_results()
        clean_results = filter_duplicates_from_scraped_results(new_results=raw_result, 
                                          questions_csv_file_path=CSV_FILE_PATH)

        write_results_to_file(results=clean_results, 
                              questions_csv_file_path=CSV_FILE_PATH)
        
    print("-" * 20)
    print(f"Extractions for '{COURSE_NUMBER}' are done. All detected images are saved as well.")
