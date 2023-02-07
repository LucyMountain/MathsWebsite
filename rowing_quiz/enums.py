from enum import Enum


class QuizState(Enum):
    ASSIGN_CREWS = 1
    DETAIL = 2
    NEXT_ROUND = 3
    SUBMIT = 4
    RESULTS = 5
