import pandas as pd
import csv
import os
from pathlib import Path
from Settings.Settings import DELIMITER, COURSE_NUMBER


def write_results_to_file(result: dict[str, str], file: Path) -> None:
    """Takes in all the extracted questions as well as results and stores them into a file.

    Args:
        result (dict[str, str]): Dictionary of question-correct answer pair
        filename (str): csv file containing the question-answer pairs
    """

    first_row: list[str] = None
    if not file.exists():
        first_row = (["question_code", "question", "answer"])

    with open(file, "a+") as new_file:
        f = csv.writer(new_file, 
                       delimiter=DELIMITER)

        if first_row:
             f.writerow(first_row)

        for question_code, question_answer in result.items():
                try:
                    question, answer = question_answer.split(DELIMITER)
                    row = [question_code, question, answer]
                    f.writerow(row)
                except ValueError as ve:
                    print(len(question_answer.split(DELIMITER)))



def remove_duplicates(new_results: dict[str, str], file: Path) -> dict[str, str]:

    # file does not exist. no duplicates can be checked
    if not file.exists():
         return new_results


    # file exists
    with open(file, "r") as f:
        stored_questions_from_file: pd.DataFrame = pd.read_csv(f, sep=DELIMITER)

    res_without_duplicates = dict()
    
    for question_code, question_answer in new_results.items():
        if question_code in list(stored_questions_from_file["question_code"]):
            continue

        res_without_duplicates[question_code] = question_answer

    return res_without_duplicates