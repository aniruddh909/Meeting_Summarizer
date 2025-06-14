import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import upload, meetings, transcription, pipeline

# Set tokenizer parallelism environment variable
os.environ["TOKENIZERS_PARALLELISM"] = "false"

app = FastAPI(
    title="Meeting Assistant API",
    description="API for processing and analyzing meeting recordings",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(meetings.router, prefix="/api/v1", tags=["meetings"])
app.include_router(transcription.router, prefix="/api/v1", tags=["transcription"])
app.include_router(pipeline.router, prefix="/api/v1", tags=["pipeline"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Meeting Assistant API"} 