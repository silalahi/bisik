from typing import List, Tuple


class WordMatcher:
    """Matches expected words with actual spoken words"""
    
    @staticmethod
    def match_words(expected: List[str], actual: List[str]) -> List[Tuple[str, str]]:
        """
        Match expected and actual word lists
        
        Args:
            expected: List of expected words
            actual: List of actual spoken words
            
        Returns:
            List of (expected_word, actual_word) pairs
        """
        pairs = []
        min_len = min(len(expected), len(actual))
        
        # Basic matching
        for i in range(min_len):
            pairs.append((expected[i], actual[i]))
        
        # Handle missing words
        if len(expected) > len(actual):
            for i in range(min_len, len(expected)):
                pairs.append((expected[i], ""))
        
        # Handle extra words
        elif len(actual) > len(expected):
            for i in range(min_len, len(actual)):
                pairs.append(("", actual[i]))
        
        return pairs