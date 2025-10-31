# Bhysiq
An AI-powered tool to evaluate and improve your pronunciation.

## Features
- Real-time pronunciation evaluation
- Word-level accuracy scoring
- Phonetic transcription feedback

## Quick Start
```bash
pip install -r requirements.txt
python app.py
```
Visit http://localhost:3000

## Documentation
- [Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [Contributing](docs/contributing.md)

## Quick Setup Commands

1. Create virtual environment
```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Setup environment
```
cp .env.example .env
```

4. Download models (optional, will download on first use)
```
python scripts/download_models.py
```

5. Initialize databases
```
python scripts/setup_database.py
```

6. Run the application
```
python app.py
```