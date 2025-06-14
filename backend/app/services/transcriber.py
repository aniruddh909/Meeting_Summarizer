import whisper
import tempfile
import os
from pathlib import Path
import logging
from typing import Optional
import ffmpeg

logger = logging.getLogger(__name__)

class AudioTranscriber:
    def __init__(self):
        """Initialize the Whisper model."""
        try:
            # Load the base model - can be changed to 'tiny', 'base', 'small', 'medium', or 'large'
            self.model = whisper.load_model("base")
            logger.info("Successfully initialized Whisper model")
        except Exception as e:
            logger.error(f"Failed to initialize Whisper model: {str(e)}")
            raise

    def _validate_audio_file(self, file_path: str) -> bool:
        """Validate if the file is a valid audio file."""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return False

            # Try to probe the file with ffmpeg
            probe = ffmpeg.probe(file_path)
            if 'streams' not in probe:
                return False

            # Check if it has an audio stream
            has_audio = any(stream['codec_type'] == 'audio' for stream in probe['streams'])
            return has_audio

        except ffmpeg.Error:
            return False
        except Exception as e:
            logger.error(f"Error validating audio file: {str(e)}")
            return False

    def transcribe_audio(self, file_path: str) -> Optional[str]:
        """
        Transcribe an audio file using Whisper.
        
        Args:
            file_path (str): Path to the audio file
            
        Returns:
            Optional[str]: Transcribed text or None if transcription fails
        """
        try:
            # Validate the audio file
            if not self._validate_audio_file(file_path):
                raise ValueError("Invalid audio file format")

            # Transcribe the audio
            result = self.model.transcribe(
                file_path,
                fp16=False,  # Use CPU
                language="en"  # Can be made dynamic based on user input
            )

            return result["text"]

        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            raise

# Create a singleton instance
transcriber = AudioTranscriber() 