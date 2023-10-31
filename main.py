from pathlib import Path
import requests, os
from bs4 import BeautifulSoup, ResultSet

from Workers.QuestionAnswerImageExtraction import QuestionAnswerImageExtractor
from Workers.FileWriting import write_results_to_file, remove_duplicates
from Settings.Settings import URL, COURSE_NUMBER, COOKIES, HEADERS, PARAMS, KE_1_attempts, KE_2_attempts


if __name__ == "__main__":

    attempts: list[str] = KE_1_attempts
    for attempt in attempts:
        PARAMS['attempt'] = attempt
        response: requests.Response = requests.get(URL, 
                                                   cookies=COOKIES, 
                                                   headers=HEADERS, 
                                                   params=PARAMS)
        
        if not response.status_code == 200:
            print("Konnte nicht zu ", URL, " verbinden. Abbruch. HTTP Statuscode: ", response.status_code)
            continue

        soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
        question_divs: ResultSet = soup.find_all("div", {"class": "qtext" })
        selection_divs: ResultSet = soup.find_all("div", {"class": "formulation clearfix" })
        correct_answer_divs: ResultSet = soup.find_all("div", {"class": "rightanswer"})

        # setting up filepaths for storing the information and images
        general_file_path: Path = Path(f"{os.sep}Users{os.sep}florianluebke{os.sep}Desktop{os.sep}Question-Getter{os.sep}ExtractedQuestions{os.sep}{COURSE_NUMBER}")
        anki_import_file_path: Path = Path(os.path.join(general_file_path, Path(f"Frage_{COURSE_NUMBER}.csv")))
        image_path: Path = Path(os.path.join(general_file_path,"images"))

        extractor: QuestionAnswerImageExtractor = QuestionAnswerImageExtractor(course_number=COURSE_NUMBER, 
                                                                               image_storage_path=image_path)
        extractor.extract_unique_question_codes(selection_divs=selection_divs)
        extractor.extract_questions(question_divs=selection_divs)
        extractor.extract_correct_answers(correct_answer_divs=correct_answer_divs)
        extractor.generate_results()    
        raw_result: dict[str, str] = extractor.get_results()
        clean_results = remove_duplicates(new_results=raw_result, 
                                          file=anki_import_file_path)

        write_results_to_file(result=clean_results, 
                              file=anki_import_file_path)
