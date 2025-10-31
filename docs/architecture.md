# Architecture Documentation

## Overview
The AI Pronunciation Trainer follows a clean, modular architecture with clear separation of concerns.

## Layers

### 1. Configuration Layer
- Manages all application settings
- Environment variable loading
- Path management

### 2. Core Layer
- Defines interfaces (Protocols)
- Data models (dataclasses)
- Enumerations
- No implementation logic

### 3. Implementation Layer
- Audio processing
- Speech recognition
- Phoneme conversion
- Word matching and scoring

### 4. Business Logic Layer
- PronunciationTrainer orchestrates all components
- Handles the main evaluation workflow

### 5. Web Layer
- Flask application
- REST API endpoints
- Frontend templates

## Data Flow
```
User → Web Interface → API Endpoint → Trainer → Components → Results → User
```

## Design Patterns Used
- Factory Pattern (PhonemeConverterFactory)
- Dependency Injection (all components)
- Protocol/Interface Pattern (core interfaces)
- Repository Pattern (database access - future)