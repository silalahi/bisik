import pytest
from pathlib import Path
import torch

from config.settings import AppConfig
from src.audio.processor import AudioProcessorImpl
from src.recognition.whisper_recognizer import WhisperRecognizer
from src.phonetics.factory import PhonemeConverterFactory


@pytest.fixture
def config():
    return AppConfig()


@pytest.fixture
def audio_processor():
    return AudioProcessorImpl()


@pytest.fixture
def recognizer():
    return WhisperRecognizer(model_size="tiny")  # Use tiny for faster tests


@pytest.fixture
def phoneme_converter():
    return PhonemeConverterFactory.create("en")


@pytest.fixture
def sample_audio():
    # Generate 1 second of silence at 16kHz
    return torch.zeros(1, 16000)