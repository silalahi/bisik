import whisper
import sys


def download_models():
    models = ['tiny', 'base', 'small']
    
    for model_name in models:
        print(f"Downloading {model_name} model...")
        try:
            whisper.load_model(model_name)
            print(f"✓ {model_name} model downloaded successfully")
        except Exception as e:
            print(f"✗ Error downloading {model_name}: {e}")
            sys.exit(1)
    
    print("\n✓ All models downloaded successfully!")


if __name__ == '__main__':
    download_models()