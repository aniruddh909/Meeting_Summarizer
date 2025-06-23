import whisper
import tempfile
import os
import gc
from fastapi import UploadFile
import logging
import torch
import numpy as np

logger = logging.getLogger(__name__)

# Global model instance
_whisper_model = None

def get_whisper_model():
    """Get or initialize the Whisper model."""
    global _whisper_model
    if _whisper_model is None:
        try:
            logger.info("Loading Whisper model...")
            # Force CPU and disable CUDA
            torch.cuda.is_available = lambda: False
            os.environ["CUDA_VISIBLE_DEVICES"] = ""
            
            # Set memory optimization flags
            torch.set_num_threads(1)
            torch.set_num_interop_threads(1)
            
            # Load tiny model with CPU optimizations
            _whisper_model = whisper.load_model(
                "tiny",
                device="cpu",
                download_root=os.path.join(os.path.dirname(__file__), "models")
            )
            
            # Optimize model for inference
            _whisper_model.eval()
            torch.set_grad_enabled(False)
            
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {str(e)}")
            raise
    return _whisper_model

async def transcribe_audio(file: UploadFile) -> str:
    """
    Transcribe audio file using Whisper model with memory optimizations.
    """
    temp_file_path = None
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Get the model
        model = get_whisper_model()
        
        # Transcribe the audio with memory optimizations
        with torch.no_grad(), torch.cuda.amp.autocast(enabled=False):
            result = model.transcribe(
                temp_file_path,
                fp16=False,  # Use CPU
                language="en",
                beam_size=1,  # Reduce beam size for lower memory usage
                best_of=1,    # Reduce best_of for lower memory usage
                temperature=0.0,  # Disable sampling
                condition_on_previous_text=False,  # Disable conditioning
                compression_ratio_threshold=2.4,  # Increase compression threshold
                logprob_threshold=-1.0,  # Disable logprob threshold
                no_speech_threshold=0.6,  # Increase no speech threshold
            )
        
        return result["text"]
            
    except Exception as e:
        logger.error(f"Error in transcription: {str(e)}")
        raise Exception(f"Failed to transcribe audio: {str(e)}")
    finally:
        # Clean up the temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        # Force garbage collection
        gc.collect()
        torch.cuda.empty_cache()  # Clear CUDA cache if available
        np.empty(0)  # Clear numpy cache 