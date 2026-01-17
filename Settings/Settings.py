from typing import Dict, List
from pathlib import Path

# cmid: List[attempts] -> beides aus URL entnommen
COURSES: Dict[int, List[int]] = {187091: [1088549, 1088798, 1088802, 1088804, 1088809, 1088816, 1088822, 1088825, 1088830, 1088838, 1088842, 1088845, 1088850, 1088855, 1088859, 1088541],
                                 187106: [1088861, 1088864, 1088867, 1088871, 1088877, 1088880, 1088887, 1088889, 1088893, 1088898, 1088902, 1088912, 1088919, 1088923, 1088927, 1088934],
                                 187120: [1092166, 1092164, 1093710, 1093728, 1093737, 1093756, 1093763, 1093771, 1093775, 1093778, 1093782, 1093785, 1093789, 1093792, 1093795, 1093801],
                                 187133: [1093807, 1093811, 1093818, 1093826, 1093862, 1093871, 1093884, 1093891, 1093898, 1093901, 1093906, 1093908],
                                 187144: [1093913, 1093916, 1093919, 1093923, 1093926, 1093928, 1093932, 1093934, 1093936, 1093940, 1093945, 1093949],
                                 187150: [1093957, 1094013, 1094017, 1094019, 1094022, 1094026, 1094028, 1094032, 1094034, 1094036, 1094040, 1094042, 1094043],
                                 187165: [1094045, 1094055, 1094058, 1094064, 1094071, 1094075, 1094080, 1094086, 1094091, 1094094, 1094097, 1094100]}

COURSE_NAMES: Dict[int, str] = {187091: "Bayes-Klassifikation",
                                187106: "Entscheidungswälder",
                                187120: "K-Means",
                                187133: "Hierarchisches_Clustering",
                                187144: "Assoziationsregeln",
                                187150: "Anomalieerkennung",
                                187165: "Hauptkomponentenanalyse"}

URL: str = "https://moodle.fernuni-hagen.de/mod/quiz/review.php"

COURSE_NUMBER: int = 187165

# aus cookies im browser
COOKIES: Dict[str, str] = {"MoodleSession": "kginonfu6vsm0333jsf7pvls6g",
                           "MDL_SSP_SessID": "c7fd86140d34082734cc193fdbbdf0dd"}

HEADERS: Dict[str, str] = {"User-Agent": "Mozilla/5.0",
    "Accept": "text/html"}

PARAMS: Dict[str, int] = {"attempt": 0}
CSV_FILE_PATH: Path = Path(f"questions.csv")
IMAGE_FILE_PATH: Path = Path("/images")
DELIMITER: str = ";"
QUESTION_ID: int = 1