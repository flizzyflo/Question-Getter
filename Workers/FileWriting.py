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

            # case file does not exist, nothing will be appended, but file will be created instead
            if header_row:
                csv_file.writerow(header_row)

            # write row by row into the file, separated by delimiter
            for unique_question_code, question_and_answer in results.items():
                question, answer = question_and_answer.split(DELIMITER)
                new_row = [unique_question_code, question, answer.strip()]
                csv_file.writerow(new_row)



    @staticmethod
    def filter_duplicates_from_stored_file(questions_csv_file_path: Path) -> None:
        """
        Checks for duplicates in the new results, meaning if the respective question codes are already stored
        within the csv file. If yes, these questions were not transfered into the return dictionary.

        Args:
            questions_csv_file_path (Path): Path to the already existing csv file to check for duplicates.

        Returns:
            dict[str, str]: Filtered results dictionary without the questions already stored within the csv file.
        """


        assert questions_csv_file_path.exists(), f"Path provided > {questions_csv_file_path} < does not exist"

        # file exists
        with open(questions_csv_file_path, "r") as csv_file:
            questions_from_file: pd.DataFrame = pd.read_csv(filepath_or_buffer=csv_file,
                                                            sep=DELIMITER)

        # for unique_question_code, question_and_answer in results.items():
        amount_before: int = questions_from_file.shape[0]
        questions_from_file["key"] = questions_from_file["question"]+questions_from_file["answer"]
        no_duplicate_questions: pd.DataFrame = questions_from_file.drop_duplicates(subset=["key"])
        no_duplicate_questions = no_duplicate_questions.drop(columns=["key"])
        amount_after: int = no_duplicate_questions.shape[0]
        print(f"Dropped {amount_before - amount_after} duplicate questions.")

        # merge answer and question cols
        no_duplicate_questions.to_csv(questions_csv_file_path, sep=DELIMITER)
