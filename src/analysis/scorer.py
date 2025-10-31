from typing import List, Dict
from src.core.models import WordComparison
from src.core.enums import PronunciationCategory
from src.core.interfaces import PhonemeConverter


class PronunciationScorer:
    def __init__(self, phoneme_converter: PhonemeConverter):
        self.phoneme_converter = phoneme_converter
    
    def compare_words(self, expected: str, actual: str) -> WordComparison:
        # Convert to phonemes with fallback
        try:
            expected_ipa = self.phoneme_converter.word_to_phonemes(expected) if expected else ""
            actual_ipa = self.phoneme_converter.word_to_phonemes(actual) if actual else ""
        except Exception as e:
            expected_ipa = expected  # Fallback to original text
            actual_ipa = actual
        
        # Handle None returns
        expected_ipa = expected_ipa or expected or ""
        actual_ipa = actual_ipa or actual or ""
        
        # Calculate similarity
        similarity = self._calculate_similarity(expected_ipa, actual_ipa)
        
        # Categorize
        category = self._categorize_pronunciation(similarity, expected, actual)
        
        # Find phoneme-level errors
        phoneme_errors = self._find_phoneme_errors(expected_ipa, actual_ipa)
        
        return WordComparison(
            expected_word=expected,
            actual_word=actual,
            expected_ipa=expected_ipa,
            actual_ipa=actual_ipa,
            similarity_score=similarity,
            category=category,
            phoneme_errors=phoneme_errors
        )
    
    def _calculate_similarity(self, ipa1: str, ipa2: str) -> float:
        if not ipa1 or not ipa2:
            return 0.0
        
        distance = self._levenshtein_distance(ipa1, ipa2)
        max_len = max(len(ipa1), len(ipa2))
        
        if max_len == 0:
            return 100.0
        
        similarity = (1 - distance / max_len) * 100
        return round(similarity, 2)
    
    @staticmethod
    def _levenshtein_distance(s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return PronunciationScorer._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _categorize_pronunciation(
        self, 
        similarity: float, 
        expected: str, 
        actual: str
    ) -> PronunciationCategory:
        if not actual:
            return PronunciationCategory.MISSING
        if not expected:
            return PronunciationCategory.EXTRA
        if similarity >= 95:
            return PronunciationCategory.CORRECT
        elif similarity >= 70:
            return PronunciationCategory.SIMILAR
        else:
            return PronunciationCategory.INCORRECT
    
    def _find_phoneme_errors(self, expected_ipa: str, actual_ipa: str) -> List[Dict]:
        errors = []
        max_len = max(len(expected_ipa), len(actual_ipa))
        
        for i in range(max_len):
            expected_char = expected_ipa[i] if i < len(expected_ipa) else ""
            actual_char = actual_ipa[i] if i < len(actual_ipa) else ""
            
            errors.append({
                'position': i,
                'expected': expected_char,
                'actual': actual_char,
                'is_correct': expected_char == actual_char
            })
        
        return errors