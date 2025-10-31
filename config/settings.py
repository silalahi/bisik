from dataclasses import dataclass, field
from pathlib import Path
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class AppConfig:
    # Server settings
    host: str = "0.0.0.0"
    port: int = 3000
    debug: bool = False
    
    # Model settings
    whisper_model_size: str = "base"
    sample_rate: int = 16000
    
    # File paths - use absolute paths
    upload_folder: Path = field(default_factory=lambda: Path.cwd() / "uploads")
    database_folder: Path = field(default_factory=lambda: Path.cwd() / "databases")
    
    # Supported languages
    supported_languages: List[str] = field(default_factory=lambda: ["en", "de"])
    
    def __post_init__(self):
        self.debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
        self.whisper_model_size = os.getenv("WHISPER_MODEL_SIZE", self.whisper_model_size)
        self.sample_rate = int(os.getenv("SAMPLE_RATE", self.sample_rate))
        
        # Ensure paths are absolute
        if not self.upload_folder.is_absolute():
            self.upload_folder = Path.cwd() / self.upload_folder
        if not self.database_folder.is_absolute():
            self.database_folder = Path.cwd() / self.database_folder
        
        # Create directories with proper permissions
        self.upload_folder.mkdir(exist_ok=True, parents=True)
        self.database_folder.mkdir(exist_ok=True, parents=True)
        
        print(f"Upload folder: {self.upload_folder}")
        print(f"Database folder: {self.database_folder}")