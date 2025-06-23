import os
import logging
import torch
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import upload, meetings, transcription, pipeline
from .config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set environment variables for optimization
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONUNBUFFERED"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"  # Limit OpenMP threads
os.environ["MKL_NUM_THREADS"] = "1"  # Limit MKL threads
os.environ["CUDA_VISIBLE_DEVICES"] = ""  # Disable CUDA

# Configure PyTorch for CPU
torch.set_num_threads(1)
torch.set_num_interop_threads(1)
torch.set_grad_enabled(False)

app = FastAPI(
    title="Meeting Assistant API",
    description="API for processing and analyzing meeting recordings",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://meeting-assistant.vercel.app",
        "https://*.vercel.app"
    ],
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

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Meeting Assistant API...")
    # Clear any existing caches
    torch.cuda.empty_cache()
    np.empty(0)
    logger.info("Meeting Assistant API startup complete") 