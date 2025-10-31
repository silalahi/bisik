import torch
import whisper
from typing import List, Tuple
import logging
from src.core.models import Word


class WhisperRecognizer:
    def __init__(self, model_size: str = "base", language: str = "en"):
        self.model = whisper.load_model(model_size)
        self.language = language
        self.logger = logging.getLogger(__name__)
    
    def transcribe(self, audio: torch.Tensor) -> Tuple[str, List[Word]]:
        """
        Transcribe audio with word-level timing
        
        Args:
            audio: Audio tensor (1, samples) at 16kHz
            
        Returns:
            Tuple of (transcript text, list of Word objects)
        """
        try:
            # Convert to numpy for Whisper
            audio_np = audio.squeeze().numpy()
            
            # Transcribe with word timestamps
            result = self.model.transcribe(
                audio_np,
                language=self.language,
                word_timestamps=True,
                verbose=False
            )
            
            transcript = result['text'].strip()
            words = self._extract_words(result)
            
            return transcript, words
            
        except Exception as e:
            self.logger.error(f"Transcription error: {e}")
            raise
    
    def _extract_words(self, whisper_result: dict) -> List[Word]:
        words = []
        
        for segment in whisper_result.get('segments', []):
            for word_info in segment.get('words', []):
                word = Word(
                    text=word_info['word'].strip(),
                    start_time=word_info['start'],
                    end_time=word_info['end'],
                    confidence=word_info.get('probability', 1.0)
                )
                words.append(word)
        
        return words