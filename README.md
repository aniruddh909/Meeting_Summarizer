# Meeting Assistant

An AI-powered application that helps users analyze and summarize their meetings using OpenAI's Whisper and GPT-4.

## Features

- Audio file upload and transcription
- Meeting summarization
- Action item extraction
- User authentication
- SQLite database for data persistence

## Tech Stack

- Backend: FastAPI (Python)
- Frontend: React + TailwindCSS
- AI: OpenAI Whisper & GPT-4
- Database: SQLite
- Hosting: Render.com (backend), Vercel (frontend)

## Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory with:
```
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secret_key
```

4. Run the development server:
```bash
cd backend
uvicorn app.main:app --reload --port 8001
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── app/
│   ├── api/          # API routes
│   ├── core/         # Core functionality
│   ├── db/           # Database models and connection
│   ├── services/     # External service integrations
│   └── schemas/      # Pydantic models
└── requirements.txt
``` 