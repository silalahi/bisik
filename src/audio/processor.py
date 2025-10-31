import torch
import torchaudio
from pathlib import Path
import logging
import subprocess
import tempfile


class AudioProcessorImpl:
    def __init__(self, target_sample_rate: int = 16000):
        self.target_sample_rate = target_sample_rate
        self.logger = logging.getLogger(__name__)
    
    def process_audio_file(self, filepath: Path) -> torch.Tensor:
        """
        Load audio file and convert to tensor at target sample rate
        
        Args:
            filepath: Path to audio file
            
        Returns:
            Audio tensor of shape (1, samples)
        """
        try:
            self.logger.info(f"Processing audio file: {filepath}")
            
            # Check if file exists
            if not filepath.exists():
                raise FileNotFoundError(f"Audio file not found: {filepath}")
            
            # Check file size
            file_size = filepath.stat().st_size
            self.logger.info(f"File size: {file_size} bytes")
            
            if file_size == 0:
                raise ValueError("Audio file is empty")
            
            # Try loading directly with torchaudio
            try:
                waveform, sample_rate = torchaudio.load(str(filepath))
                self.logger.info(f"Loaded audio: sample_rate={sample_rate}, shape={waveform.shape}")
            except Exception as e:
                self.logger.warning(f"Direct load failed: {e}, trying ffmpeg conversion")
                waveform, sample_rate = self._convert_with_ffmpeg(filepath)
            
            # Resample if necessary
            if sample_rate != self.target_sample_rate:
                self.logger.info(f"Resampling from {sample_rate}Hz to {self.target_sample_rate}Hz")
                resampler = torchaudio.transforms.Resample(
                    sample_rate, 
                    self.target_sample_rate
                )
                waveform = resampler(waveform)
            
            # Convert to mono if stereo
            if waveform.shape[0] > 1:
                self.logger.info("Converting stereo to mono")
                waveform = torch.mean(waveform, dim=0, keepdim=True)
            
            self.logger.info(f"Final waveform shape: {waveform.shape}")
            return waveform
            
        except Exception as e:
            self.logger.error(f"Error processing audio: {e}", exc_info=True)
            raise RuntimeError(f"Error loading audio file: {e}")
    
    def _convert_with_ffmpeg(self, filepath: Path) -> tuple:
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            # Convert to WAV using ffmpeg
            cmd = [
                'ffmpeg', '-y', '-i', str(filepath),
                '-ar', str(self.target_sample_rate),
                '-ac', '1',  # mono
                '-f', 'wav',
                tmp_path
            ]
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"ffmpeg conversion failed: {result.stderr.decode()}")
            
            # Load the converted file
            waveform, sample_rate = torchaudio.load(tmp_path)
            return waveform, sample_rate
            
        finally:
            # Cleanup temp file
            Path(tmp_path).unlink(missing_ok=True)