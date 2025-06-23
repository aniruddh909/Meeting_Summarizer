from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ...services.summarizer import summarizer

router = APIRouter()

class TranscriptRequest(BaseModel):
    transcript: str

@router.post("/summarize")
async def summarize_transcript(request: TranscriptRequest):
    """
    Summarize a meeting transcript and extract action items.
    """
    try:
        result = await summarizer.summarize(request.transcript)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 