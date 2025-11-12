# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bisik is an AI-powered pronunciation evaluation tool that provides real-time feedback on pronunciation accuracy with word-level scoring and phonetic transcription. The application uses OpenAI Whisper for speech recognition and epitran/panphon for phonetic analysis.

## Development Commands

### Initial Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env

# Download AI models (optional - will auto-download on first use)
python scripts/download_models.py

# Initialize databases
python scripts/setup_database.py
```

### Running the Application
```bash
# Development server (with hot reload if debug=True)
python app.py

# Production server with gunicorn
gunicorn -w 4 -b 0.0.0.0:3000 'web.app_factory:create_app()'
```

### Testing
```bash
# Run all tests with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/unit/test_phonetics.py

# Run with verbose output
pytest -v

# Quick test uploads and evaluation
python test_upload.py
python test_evaluation.py
```

## Architecture Overview

The codebase follows a clean, layered architecture with strict separation of concerns:

### Core Architecture Pattern

**Dependency Injection throughout**: All major components receive their dependencies via constructor injection, making the code testable and modular.

1. **Core Layer** (`src/core/`): Defines contracts via Protocol classes and data models
   - `interfaces.py`: Protocol definitions (AudioProcessor, SpeechRecognizer, PhonemeConverter)
   - `models.py`: Dataclasses (Word, WordComparison, PronunciationResult)
   - `enums.py`: Enumerations (PronunciationCategory)
   - NO implementation logic - only interfaces and data structures

2. **Implementation Layer** (`src/`): Concrete implementations organized by domain
   - `audio/`: Audio file processing (converts audio to tensors)
   - `recognition/`: Whisper-based speech recognition
   - `phonetics/`: Phoneme conversion with Factory Pattern
     - Uses `PhonemeConverterFactory` to instantiate language-specific converters
     - Currently supports English (`en`) and German (`de`)
   - `analysis/`: Word matching (via Munkres algorithm) and pronunciation scoring

3. **Business Logic Layer** (`src/trainer/`):
   - `PronunciationTrainer` orchestrates the complete evaluation workflow
   - Coordinates: audio processing → transcription → word matching → phonetic comparison → scoring
   - Returns `PronunciationResult` with detailed feedback

4. **Web Layer** (`web/`):
   - `app_factory.py`: Flask application factory pattern
   - `routes.py`: REST API endpoints (receives dependencies via route registration)
   - Frontend uses templates and static files

5. **Configuration Layer** (`config/settings.py`):
   - `AppConfig` dataclass manages all settings
   - Loads environment variables from `.env`
   - Creates required directories on initialization

### Key Data Flow

```
Audio Upload → AudioProcessor → SpeechRecognizer → WordMatcher → PronunciationScorer → PronunciationResult
```

The `PronunciationTrainer` in `src/trainer/pronunciation_trainer.py` is the main orchestrator that coordinates all components.

### Important Design Patterns

- **Factory Pattern**: `PhonemeConverterFactory` creates language-specific phoneme converters
- **Protocol/Interface Pattern**: Core interfaces define contracts without implementation
- **Dependency Injection**: Components receive dependencies in constructors
- **Application Factory**: Flask app created via `create_app(config)` function

## Adding New Language Support

To add support for a new language:

1. Create new converter class in `src/phonetics/` (e.g., `french.py`) that inherits from `BasePhonemeConverter`
2. Register in `PhonemeConverterFactory.create()` method in `src/phonetics/factory.py`
3. Add language code to `supported_languages` in `config/settings.py`
4. Install required epitran language packs if needed

## Working with Components

### Creating a PronunciationTrainer Instance

The trainer requires three dependencies injected:
```python
from src.audio.processor import AudioProcessorImpl
from src.recognition.whisper_recognizer import WhisperRecognizer
from src.phonetics.factory import PhonemeConverterFactory
from src.trainer.pronunciation_trainer import PronunciationTrainer

trainer = PronunciationTrainer(
    audio_processor=AudioProcessorImpl(),
    speech_recognizer=WhisperRecognizer(model_size="base"),
    phoneme_converter=PhonemeConverterFactory.create("en")
)
```

### Understanding the Evaluation Flow

1. Audio file is processed into a tensor by `AudioProcessor`
2. `SpeechRecognizer` transcribes audio and extracts word timing
3. `WordMatcher` pairs expected words with actual words using Hungarian algorithm
4. `PronunciationScorer` compares phonemes and calculates similarity scores
5. Results packaged into `PronunciationResult` with overall accuracy

## File Organization

- `src/core/`: Abstract interfaces and data models (no implementation)
- `src/audio/`, `src/recognition/`, `src/phonetics/`, `src/analysis/`: Domain-specific implementations
- `src/trainer/`: Business logic orchestration
- `web/`: Flask application and HTTP layer
- `config/`: Configuration management
- `scripts/`: Utility scripts for setup and maintenance
- `tests/`: Test files organized by test type
- `databases/`: Runtime database storage
- `uploads/`: Temporary audio file storage

## Environment Variables

Key variables in `.env`:
- `FLASK_DEBUG`: Enable/disable debug mode
- `WHISPER_MODEL_SIZE`: Whisper model size (tiny/base/small/medium/large)
- `SAMPLE_RATE`: Audio sample rate (default: 16000)
- `UPLOAD_FOLDER`: Path for uploaded audio files
- `DATABASE_FOLDER`: Path for database storage

## API Usage

Main endpoint: `POST /api/evaluate`
- Accepts: multipart/form-data with `audio` (OGG), `expected_text`, `language` fields
- Returns: JSON with transcript, accuracy score, word-by-word comparisons, timing info

See `docs/api.md` for complete API documentation.
