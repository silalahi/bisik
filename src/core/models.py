from dataclasses import dataclass
from typing import List, Dict
from src.core.enums import PronunciationCategory


@dataclass
class Word:
    text: str
    start_time: float
    end_time: float
    confidence: float = 1.0


@dataclass
class WordComparison:
    expected_word: str
    actual_word: str
    expected_ipa: str
    actual_ipa: str
    similarity_score: float
    category: PronunciationCategory
    phoneme_errors: List[Dict[str, bool]]


@dataclass
class PronunciationResult:
    transcript: str
    expected_text: str
    overall_accuracy: float
    word_comparisons: List[WordComparison]
    words_with_timing: List[Word]
    
    def to_dict(self) -> dict:
        return {
            'transcript': self.transcript or "",
            'expected_text': self.expected_text or "",
            'overall_accuracy': float(self.overall_accuracy),
            'word_comparisons': [
                {
                    'expected_word': comp.expected_word or "",
                    'actual_word': comp.actual_word or "",
                    'expected_ipa': comp.expected_ipa or "",
                    'actual_ipa': comp.actual_ipa or "",
                    'similarity_score': float(comp.similarity_score),
                    'category': comp.category.value if hasattr(comp.category, 'value') else str(comp.category),
                    'phoneme_errors': comp.phoneme_errors or []
                }
                for comp in (self.word_comparisons or [])
            ],
            'words_with_timing': [
                {
                    'text': word.text or "",
                    'start_time': float(word.start_time),
                    'end_time': float(word.end_time),
                    'confidence': float(word.confidence)
                }
                for word in (self.words_with_timing or [])
            ]
        }