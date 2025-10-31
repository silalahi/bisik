from flask import Flask, request, jsonify, render_template
from pathlib import Path
import logging

from config.settings import AppConfig
from src.audio.processor import AudioProcessorImpl
from src.recognition.whisper_recognizer import WhisperRecognizer
from src.phonetics.factory import PhonemeConverterFactory
from src.trainer.pronunciation_trainer import PronunciationTrainer

def register_routes(app: Flask, config: AppConfig):
    logger = logging.getLogger(__name__)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/api/random-sentence', methods=['GET'])
    def get_random_sentence():
        try:
            import csv
            import random
            
            language = request.args.get('language', 'en')
            
            # Determine CSV file based on language
            csv_files = {
                'en': config.database_folder / 'english_samples.csv',
                'de': config.database_folder / 'german_samples.csv'
            }
            
            csv_file = csv_files.get(language)
            
            if not csv_file or not csv_file.exists():
                return jsonify({'error': f'Database for {language} not found'}), 404
            
            # Read CSV and get random sentence
            sentences = []
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sentences.append({
                        'id': row.get('id', ''),
                        'text': row.get('text', ''),
                        'difficulty': row.get('difficulty', 'unknown'),
                        'category': row.get('category', 'general')
                    })
            
            if not sentences:
                return jsonify({'error': 'No sentences found in database'}), 404
            
            # Select random sentence
            random_sentence = random.choice(sentences)
            
            return jsonify(random_sentence)
            
        except Exception as e:
            logger.error(f"Error loading random sentence: {e}", exc_info=True)
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/evaluate', methods=['POST'])
    def evaluate_pronunciation():
        audio_path = None
        try:
            # Get data from request
            audio_file = request.files.get('audio')
            expected_text = request.form.get('expected_text')
            language = request.form.get('language', 'en')
            
            logger.info(f"Received request: text='{expected_text}', language='{language}'")
            
            if not audio_file or not expected_text:
                return jsonify({'error': 'Missing audio or text'}), 400
            
            # Ensure uploads directory exists
            config.upload_folder.mkdir(exist_ok=True)
            
            # Generate unique filename
            import uuid
            import time
            unique_filename = f"recording_{int(time.time())}_{uuid.uuid4().hex[:8]}.ogg"
            audio_path = config.upload_folder / unique_filename
            
            # Save audio file
            logger.info(f"Saving audio to: {audio_path}")
            audio_file.save(str(audio_path))
            
            if not audio_path.exists():
                return jsonify({'error': 'Failed to save audio file'}), 500
            
            logger.info(f"Audio saved: {audio_path.stat().st_size} bytes")
            
            # Create components
            logger.info("Creating audio processor...")
            audio_processor = AudioProcessorImpl(config.sample_rate)
            
            logger.info("Creating recognizer...")
            recognizer = WhisperRecognizer(config.whisper_model_size, language)
            
            logger.info("Creating phoneme converter...")
            phoneme_converter = PhonemeConverterFactory.create(language)
            
            # Evaluate
            logger.info("Creating trainer...")
            trainer = PronunciationTrainer(
                audio_processor,
                recognizer,
                phoneme_converter
            )
            
            logger.info("Starting evaluation...")
            result = trainer.evaluate(audio_path, expected_text)
            
            logger.info(f"Evaluation complete. Accuracy: {result.overall_accuracy}%")
            
            # Convert to dict
            logger.info("Converting result to dict...")
            result_dict = result.to_dict()
            
            logger.info("Returning JSON response...")
            response = jsonify(result_dict)
            
            return response
            
        except Exception as e:
            logger.error(f"ERROR in evaluation: {type(e).__name__}: {e}", exc_info=True)
            return jsonify({'error': f"{type(e).__name__}: {str(e)}"}), 500
        
        finally:
            # Cleanup
            if audio_path and audio_path.exists():
                try:
                    audio_path.unlink()
                    logger.info("Temp file cleaned up")
                except Exception as e:
                    logger.warning(f"Failed to delete temp file: {e}")
    
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy'})