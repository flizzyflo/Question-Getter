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
    """
    Checks for duplicates in the new results, meaning if the respective question codes are already stored
    within the csv file. If yes, these questions were not transfered into the return dictionary.

    Args:
        new_results (dict[str, str]): Results as a dictionary, having the unique question code as key and the question-answer, separated by a delimiter, as value
        file (Path): Path to the already existing csv file to check for duplicates.

    Returns:
        dict[str, str]: Filtered results dictionary without the questions already stored within the csv file.
    """

    # file does not exist. no duplicates exists since there is no file. new_results are first results
    if not file.exists():
         return new_results

    # file exists
    with open(file, "r") as f:
        questions_from_file: pd.DataFrame = pd.read_csv(filepath_or_buffer=f, 
                                                        sep=DELIMITER)

    filtered_results: dict[str, str] = dict()
    
    for unique_question_code, question_and_answer in new_results.items():

        # skip question code, since already within file.
        if unique_question_code in list(questions_from_file["question_code"]):
            continue

        filtered_results[unique_question_code] = question_and_answer

    return filtered_results