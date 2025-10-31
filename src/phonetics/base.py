class BasePhonemeConverter:    
    def text_to_phonemes(self, text: str) -> str:
        raise NotImplementedError
    
    def word_to_phonemes(self, word: str) -> str:
        raise NotImplementedError