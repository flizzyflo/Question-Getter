import csv
from pathlib import Path
from Settings.Settings import DELIMITER
import pandas as pd


class FileHandler:
    """
    Class to manage the files to store questions in. Contains several static methods
    to either store the information in a file as well as checking for duplicates in 
    already existing files.

    """

    @staticmethod
    def store_results(results: dict[str, str], questions_csv_file_path: Path) -> None:
        """
        Wrapper function to call several submethods to store the results into a file at path passed in as argument.
        Filters duplicate questions based on results key, which is basically the question code.

        Args:
            results (dict[str, str]): Dictionary with unique question code as key and the question text as value
            questions_csv_file_path (Path): Path to store the file containing the extracted questions
        """        
        results: dict[str, str] = FileHandler.__filter_duplicates_from_scraped_results(results=results,
                                                                                      questions_csv_file_path=questions_csv_file_path)
        FileHandler.__create_result_file(results=results,
                                        questions_csv_file_path=questions_csv_file_path)


    @staticmethod
    def __create_result_file(results: dict[str, str], questions_csv_file_path: Path) -> None:
        """
        Takes in all the extracted questions as well as results and stores them into a file.
        If file already exists at that part, results are appended.

        Args:
            result (dict[str, str]): Dictionary of question-correct answer pair
            file (str): csv filepath containing the question-answer pairs
        """

        header_row: list[str] = None

        # need to add headers when file is created initially
        if not questions_csv_file_path.exists():
            header_row = (["question_code", "question", "answer"])

        # creation of the file
        with open(questions_csv_file_path, "a+") as csv_file:
            csv_file = csv.writer(csv_file, 
                        delimiter=DELIMITER)

            if header_row:
                csv_file.writerow(header_row)

            # write row by row into the file, separated by delimiter
            for unique_question_code, question_and_answer in results.items():
                question, answer = question_and_answer.split(DELIMITER)
                new_row = [unique_question_code, question, answer]
                csv_file.writerow(new_row)

    @staticmethod
    def __filter_duplicates_from_scraped_results(results: dict[str, str], questions_csv_file_path: Path) -> dict[str, str]:
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
        if not questions_csv_file_path.exists():
            return results

        # file exists
        with open(questions_csv_file_path, "r") as csv_file:
            questions_from_file: pd.DataFrame = pd.read_csv(filepath_or_buffer=csv_file, 
                                                            sep=DELIMITER)

        filtered_results: dict[str, str] = dict()
        
        for unique_question_code, question_and_answer in results.items():

            # skip this question code, question and answer, since it is already stored within file.
            if unique_question_code in list(questions_from_file["question_code"]):
                continue

            filtered_results[unique_question_code] = question_and_answer

        return filtered_results