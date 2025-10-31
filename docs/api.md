# API Documentation

## Endpoints

### POST /api/evaluate
Evaluate pronunciation from audio recording

**Request:**
- Content-Type: multipart/form-data
- Body:
  - `audio`: Audio file (OGG format)
  - `expected_text`: Text that should be pronounced
  - `language`: Language code (`en` or `de`)

**Response:**
```json
{
  "transcript": "what you said",
  "expected_text": "what you should say",
  "overall_accuracy": 85.5,
  "word_comparisons": [
    {
      "expected_word": "hello",
      "actual_word": "hello",
      "expected_ipa": "həˈloʊ",
      "actual_ipa": "həˈloʊ",
      "similarity_score": 100.0,
      "category": "correct",
      "phoneme_errors": [...]
    }
  ],
  "words_with_timing": [...]
}
```
### GET /api/health
Health check endpoint

**Response:**
```json
{
  "status": "healthy"
}
```