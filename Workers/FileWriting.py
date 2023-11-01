import pandas as pd
import csv
from pathlib import Path
from Settings.Settings import DELIMITER


def write_results_to_file(results: dict[str, str], file: Path) -> None:
    """Takes in all the extracted questions as well as results and stores them into a file.

    Args:
        result (dict[str, str]): Dictionary of question-correct answer pair
        file (str): csv file containing the question-answer pairs
    """

    first_row: list[str] = None

    # need to add headers for initial file creation
    if not file.exists():
        first_row = (["question_code", "question", "answer"])

    with open(file, "a+") as csv_file:
        csv_file = csv.writer(csv_file, 
                       delimiter=DELIMITER)

        if first_row:
             csv_file.writerow(first_row)

        for unique_question_code, question_and_answer in results.items():
            question, answer = question_and_answer.split(DELIMITER)
            new_row = [unique_question_code, question, answer]
            csv_file.writerow(new_row)


def filter_duplicates_from_results(new_results: dict[str, str], file: Path) -> dict[str, str]:
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
    with open(file, "r") as csv_file:
        questions_from_file: pd.DataFrame = pd.read_csv(filepath_or_buffer=csv_file, 
                                                        sep=DELIMITER)

    filtered_results: dict[str, str] = dict()
    
    for unique_question_code, question_and_answer in new_results.items():

        # skip this question code, question and answer, since it is already stored within file.
        if unique_question_code in list(questions_from_file["question_code"]):
            continue

        filtered_results[unique_question_code] = question_and_answer

    return filtered_results