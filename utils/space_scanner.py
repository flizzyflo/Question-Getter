import string
from enum import StrEnum
from typing import List


class STATES(StrEnum):

    START="START"
    SPACE="SPACE"
    LETTER_DIGIT="LETTER_OR_DIGIT"
    EOL="EOL"


def find_formula_start_idx_in(input_string: str) -> List[int]:

    def move(input_string, current_idx: int) -> str:
        return input_string[current_idx]

    current_letter: str
    left_pos: int = 0
    EOL: int = len(input_string)
    STATE = STATES.START
    indices: List[int] = list()

    while STATE != STATES.EOL:

        if left_pos >= EOL or left_pos + 1 >= EOL:
            STATE = STATES.EOL


        elif STATE == STATES.START:
            current_letter = move(input_string, left_pos)
            left_pos += 1

            if current_letter.isspace():
                STATE = STATES.SPACE
            else:
                STATE = STATES.LETTER_DIGIT

        elif STATE == STATES.SPACE:
            current_letter = move(input_string, left_pos)
            left_pos += 1

            # index to be added to list, since its empty space of formula
            if current_letter.isspace():
                STATE = STATES.SPACE
                indices.append(left_pos)

            if current_letter in (",", "."):
                STATE = STATES.SPACE
                indices.append(left_pos)
                left_pos += 1

            else:
                STATE = STATES.LETTER_DIGIT

        elif STATE == STATES.LETTER_DIGIT:
            current_letter = move(input_string, left_pos)
            left_pos += 1

            if current_letter.isspace():
                STATE = STATES.SPACE

        elif left_pos == EOL:
            STATE = STATES.EOL

    return indices
