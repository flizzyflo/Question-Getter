from typing import List

from Settings.Settings import COURSES, CURRENT_COURSE_NUMBER, FILEPATH_FOR_CSV
from Workers.FileWriting import FileHandler
from utils.ResultExtractor import extract_questions_for


def get_questions_for(*, course_number: int) -> None:
    """
    Extracts all questions for a given course and stores them in a CSV file.

    The function iterates over all attempts associated with the specified
    course, retrieves the corresponding questions for each attempt, and
    persists the results incrementally into a CSV file.

    The course configuration is taken from the global `COURSES` mapping,
    while question extraction and file writing are delegated to
    `extract_questions_for` and `FileHandler`, respectively.

    Returns:
        None

    Side Effects:
        - Reads course configuration from `COURSES`
        - Calls external logic to extract question data
        - Writes extracted questions to a CSV file defined by
          `FILEPATH_FOR_CSV`
    """


    # loop through all attempts in a single course unit

    raw_result: dict[str, str]
    attempts: List[int] = COURSES[course_number]

    for attempt in attempts:
     raw_result = extract_questions_for(current_attempt=attempt)

     FileHandler.store_results(results=raw_result,
                               questions_csv_file_path=FILEPATH_FOR_CSV)
