from pathlib import Path
from typing import List
import logging

from src.core.interfaces import AudioProcessor, SpeechRecognizer, PhonemeConverter
from src.core.models import PronunciationResult, WordComparison
from src.analysis.matcher import WordMatcher
from src.analysis.scorer import PronunciationScorer


class PronunciationTrainer:
    def __init__(
        self,
        audio_processor: AudioProcessor,
        speech_recognizer: SpeechRecognizer,
        phoneme_converter: PhonemeConverter
    ):
        self.audio_processor = audio_processor
        self.speech_recognizer = speech_recognizer
        self.phoneme_converter = phoneme_converter
        self.scorer = PronunciationScorer(phoneme_converter)
        self.logger = logging.getLogger(__name__)
    
    def evaluate(self, audio_file: Path, expected_text: str) -> PronunciationResult:
        try:
            # Process audio
            audio_tensor = self.audio_processor.process_audio_file(audio_file)
            
            # Transcribe
            transcript, words_with_timing = self.speech_recognizer.transcribe(audio_tensor)
            
            # Split into words
            expected_words = expected_text.lower().split()
            actual_words = transcript.lower().split()
            
            # Match words
            word_pairs = WordMatcher.match_words(expected_words, actual_words)
            
            # Compare each word
            comparisons = [
                self.scorer.compare_words(exp, act)
                for exp, act in word_pairs
            ]
            
            # Calculate overall accuracy
            overall_accuracy = self._calculate_overall_accuracy(comparisons)
            
            return PronunciationResult(
                transcript=transcript,
                expected_text=expected_text,
                overall_accuracy=overall_accuracy,
                word_comparisons=comparisons,
                words_with_timing=words_with_timing
            )
            
        except Exception as e:
            self.logger.error(f"Evaluation error: {e}")
            raise
    
    def _calculate_overall_accuracy(self, comparisons: List[WordComparison]) -> float:
        if not comparisons:
            return 0.0
        
        total_score = sum(comp.similarity_score for comp in comparisons)
        return round(total_score / len(comparisons), 2)