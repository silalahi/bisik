import pytest
import torch
from src.audio.processor import AudioProcessorImpl


def test_audio_processor_initialization():
    processor = AudioProcessorImpl(target_sample_rate=16000)
    assert processor.target_sample_rate == 16000


def test_mono_conversion():
    processor = AudioProcessorImpl()
    # Test with stereo audio
    stereo_audio = torch.randn(2, 16000)
    # This would need a real file to test fully
    # Just checking the interface exists
    assert hasattr(processor, 'process_audio_file')