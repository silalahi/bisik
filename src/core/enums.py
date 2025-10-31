from enum import Enum

class PronunciationCategory(Enum):
    CORRECT = "correct"
    SIMILAR = "similar"
    INCORRECT = "incorrect"
    MISSING = "missing"
    EXTRA = "extra"


class Language(Enum):
    ENGLISH = "en"
    GERMAN = "de"