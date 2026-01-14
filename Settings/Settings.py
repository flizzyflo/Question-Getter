from typing import Dict, List
from pathlib import Path

COURSES: Dict[int, List[int]] = {187091: [1088549, 1088798, 1088802, 1088804, 1088809, 1088816, 1088822, 1088825, 1088830, 1088838, 1088842, 1088845, 1088850, 1088855, 1088859, 1088541],
                                 187106: [1088861, 1088864, 1088867, 1088871, 1088877, 1088880, 1088887, 1088889, 1088893, 1088898, 1088902, 1088912, 1088919, 1088923, 1088927, 1088934],
                                 187120: [1092166, 1092164]}

COURSE_NAMES: Dict[int, str] = {187091: "Bayes-Klassifikation",
                                187106: "Entscheidungswälder",
                                187120: "K-Means"}

URL: str = "https://moodle.fernuni-hagen.de/mod/quiz/review.php"

COURSE_NUMBER: str = 187120
COOKIES: Dict[str, str] = {"MoodleSession": "c5rl9a1vpr490ihvpll8hhnvfa",
                           "MDL_SSP_SessID": "c7fd86140d34082734cc193fdbbdf0dd"}

HEADERS: Dict[str, str] = {"User-Agent": "Mozilla/5.0",
    "Accept": "text/html"}

PARAMS: Dict[str, int] = {"attempt": 0}
CSV_FILE_PATH: Path = Path(f"questions.csv")
IMAGE_FILE_PATH: Path = Path("/images")
DELIMITER: str = ";"
QUESTION_ID: int = 1