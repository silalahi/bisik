from typing import Protocol, List, Tuple
from pathlib import Path
import torch
from src.core.models import Word


class AudioProcessor(Protocol):
    def process_audio_file(self, filepath: Path) -> torch.Tensor:
        ...


class SpeechRecognizer(Protocol):
    def transcribe(self, audio: torch.Tensor) -> Tuple[str, List[Word]]:
        ...


class PhonemeConverter(Protocol):
    def text_to_phonemes(self, text: str) -> str:
        ...
    
    def word_to_phonemes(self, word: str) -> str:

        ...