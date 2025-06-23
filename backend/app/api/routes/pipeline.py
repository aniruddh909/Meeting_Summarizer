from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
from pathlib import Path
import logging
from ...services.transcriber import transcriber
from ...services.summarizer import summarizer

logger = logging.getLogger(__name__)
router = APIRouter()

ALLOWED_EXTENSIONS = {'.mp3', '.wav', '.m4a'}

@router.post("/process")
async def process_meeting_audio(file: UploadFile = File(...)):
    """
    Process a meeting audio file: transcribe and summarize in one step.
    """
    temp_file_path = None
    
    try:
        # 1. Validate file extension
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # 2. Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
            logger.info(f"Saved uploaded file to temporary location: {temp_file_path}")

        # 3. Transcribe the audio
        try:
            logger.info("Starting transcription...")
            transcript = transcriber.transcribe_audio(temp_file_path)
            logger.info("Transcription completed successfully")
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Transcription failed: {str(e)}"
            )

        # 4. Summarize the transcript
        try:
            logger.info("Starting summarization...")
            summary, action_items = await summarizer.summarize(transcript)
            logger.info("Summarization completed successfully")
        except Exception as e:
            logger.error(f"Summarization failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Summarization failed: {str(e)}"
            )

        # 5. Return combined result
        response = {
            "transcript": transcript,
            "summary": summary,
            "action_items": action_items
        }
        logger.info("Successfully processed meeting audio")
        return JSONResponse(content=response, status_code=200)

    except HTTPException:
        # Re-raise HTTP exceptions as they're already properly formatted
        raise
    except Exception as e:
        # Catch any unexpected errors
        logger.error(f"Unexpected error during processing: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during processing: {str(e)}"
        )
    finally:
        # 6. Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
            logger.info(f"Cleaned up temporary file: {temp_file_path}") 