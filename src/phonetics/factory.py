from src.phonetics.base import BasePhonemeConverter
from src.phonetics.english import EnglishPhonemeConverter
from src.phonetics.german import GermanPhonemeConverter


class PhonemeConverterFactory:
    @staticmethod
    def create(language: str) -> BasePhonemeConverter:
        converters = {
            'en': EnglishPhonemeConverter,
            'de': GermanPhonemeConverter
        }
        
        if language not in converters:
            raise ValueError(f"Unsupported language: {language}")
        
        return converters[language]()