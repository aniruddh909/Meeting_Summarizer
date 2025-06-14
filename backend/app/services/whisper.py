import whisper
import tempfile
import os
from fastapi import UploadFile

async def transcribe_audio(file: UploadFile) -> str:
    """
    Transcribe audio file using Whisper model.
    """
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            
            # Load the Whisper model
            model = whisper.load_model("base")
            
            # Transcribe the audio
            result = model.transcribe(temp_file.name)
            
            # Clean up the temporary file
            os.unlink(temp_file.name)
            
            return result["text"]
            
    except Exception as e:
        print(f"Error in transcription: {str(e)}")
        raise Exception(f"Failed to transcribe audio: {str(e)}") 