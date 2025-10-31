import epitran
from src.phonetics.base import BasePhonemeConverter


class EnglishPhonemeConverter(BasePhonemeConverter):
    def __init__(self):
        self.epi = epitran.Epitran('eng-Latn')
    
    def text_to_phonemes(self, text: str) -> str:
        return self.epi.transliterate(text)
    
    def word_to_phonemes(self, word: str) -> str:
        return self.epi.transliterate(word)