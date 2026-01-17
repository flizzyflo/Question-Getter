from typing import List

from Settings.Settings import COURSES, COURSE_NUMBER, FILEPATH_FOR_CSV
from Workers.FileWriting import FileHandler
from utils.ResultExtractor import extract_questions_for


def get_questions_for(*, course_number: int) -> None:
         # loop through all attempts in a single course unit

         raw_result: dict[str, str]
         attempts: List[int] = COURSES[COURSE_NUMBER]

         for attempt in attempts:
             raw_result = extract_questions_for(current_attempt=attempt)

             FileHandler.store_results(results=raw_result,
                                       questions_csv_file_path=FILEPATH_FOR_CSV)
