# Meeting Summarizer

An AI-powered meeting assistant that transcribes audio recordings of meetings and provides intelligent summaries and action items.

## 🚀 Features

- **Audio Transcription**: Convert meeting recordings to text using OpenAI's Whisper model
- **Smart Summarization**: Generate concise summaries using Hugging Face's flan-t5-large model
- **Action Item Extraction**: Automatically identify and list action items from meetings
- **Modern UI**: Clean and responsive interface built with React and Tailwind CSS
- **Real-time Processing**: Visual feedback during transcription and summarization
- **File Validation**: Support for MP3, WAV, and M4A files with size limits

## 🛠️ Tech Stack

### Backend
- FastAPI (Python web framework)
- Whisper (Audio transcription)
- Hugging Face Transformers (Text summarization)
- SQLite (Database)
- SQLAlchemy (ORM)

### Frontend
- React
- Tailwind CSS
- Axios
- React Hot Toast (Notifications)

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn
- FFmpeg (for audio processing)

## 🚀 Getting Started

### Backend Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Start the backend server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## 📝 API Endpoints

- `POST /api/v1/process`: Process audio file (transcribe and summarize)
- `POST /api/v1/transcribe`: Transcribe audio to text
- `POST /api/v1/summarize`: Generate summary and action items
- `GET /api/v1/meetings`: Get meeting history

## 🔒 Environment Variables

Create a `.env` file in the backend directory with:
```
OPENAI_API_KEY=your_api_key_here
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI Whisper for audio transcription
- Hugging Face for the summarization model
- FastAPI for the backend framework
- React and Tailwind CSS for the frontend 
