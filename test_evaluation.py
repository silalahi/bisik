import logging
from pathlib import Path
from src.audio.processor import AudioProcessorImpl
from src.recognition.whisper_recognizer import WhisperRecognizer
from src.phonetics.factory import PhonemeConverterFactory
from src.trainer.pronunciation_trainer import PronunciationTrainer

logging.basicConfig(level=logging.DEBUG)

# Simulate the evaluation
audio_path = Path("uploads/test.ogg")  # Use an actual uploaded file
expected_text = "The quick brown fox"
language = "en"

try:
    print("Creating components...")
    audio_processor = AudioProcessorImpl(16000)
    recognizer = WhisperRecognizer("base", language)
    phoneme_converter = PhonemeConverterFactory.create(language)
    
    print("Creating trainer...")
    trainer = PronunciationTrainer(
        audio_processor,
        recognizer,
        phoneme_converter
    )
    
    print("Starting evaluation...")
    result = trainer.evaluate(audio_path, expected_text)
    
    print(f"Success! Accuracy: {result.overall_accuracy}%")
    print(f"Transcript: {result.transcript}")
    
    print("\nConverting to dict...")
    result_dict = result.to_dict()
    
    print("✓ Everything works!")
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()