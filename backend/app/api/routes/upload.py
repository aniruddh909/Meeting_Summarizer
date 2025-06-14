from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.base import get_db
from ...services.whisper import transcribe_audio
from ...services.summarizer import summarizer

router = APIRouter()

# Maximum file size (25MB in bytes)
MAX_FILE_SIZE = 25 * 1024 * 1024

@router.post("/upload/audio")
async def upload_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload an audio file for meeting transcription and analysis.
    """
    # Validate file type
    if not file.filename.endswith(('.mp3', '.wav', '.m4a')):
        raise HTTPException(
            status_code=400,
            detail="Only audio files (MP3, WAV, M4A) are allowed"
        )
    
    # Validate file size
    file_size = 0
    chunk_size = 1024 * 1024  # 1MB chunks
    
    while chunk := await file.read(chunk_size):
        file_size += len(chunk)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File size exceeds 25MB limit"
            )
    
    # Reset file pointer for processing
    await file.seek(0)
    
    try:
        # Process the file
        transcript = await transcribe_audio(file)
        summary, action_items = await summarizer.summarize(transcript)
        
        return {
            "transcript": transcript,
            "summary": summary,
            "action_items": action_items
        }
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        ) 