

from Workers.FileWriting import FileHandler
from Settings.Settings import  CURRENT_COURSE_NUMBER, FILEPATH_FOR_CSV,COURSE_NAMES
from utils.AttemptExtractor import get_questions_for



if __name__ == "__main__":

    get_questions_for(course_number=CURRENT_COURSE_NUMBER)

    print("-" * 20)
    FileHandler.filter_duplicates_from_stored_file(FILEPATH_FOR_CSV)
    print("-" * 20)
    print(f"Extractions for course '{CURRENT_COURSE_NUMBER}: {COURSE_NAMES[CURRENT_COURSE_NUMBER]}' are done.")
