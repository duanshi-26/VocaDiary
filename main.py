from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import nltk
import speech_recognition as sr
from pydub import AudioSegment
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from textblob import TextBlob
import os
import pyaudio
import wave
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

# Download punkt (only once)
nltk.download('punkt')

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # loosened for local dev; tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DATABASE SETUP ----------------
# MONGO_URI = "mongodb+srv://dua_db:260104@voca-diary-server.xmit145.mongodb.net/vocadiary?retryWrites=true&w=majority"
MONGO_URI = "mongodb://localhost:27017"  # Local MongoDB URI for development
client = AsyncIOMotorClient(MONGO_URI)
db = client["voca-diary"]   # database name
collection = db["entries"]  # collection name

# ---------------- AUDIO RECORDING ----------------
def record_audio(duration=5):
    """Record audio for specified duration and return the file path"""
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    
    p = pyaudio.PyAudio()
    
    # Create a unique filename based on timestamp
    filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    filepath = os.path.join(tempfile.gettempdir(), filename)
    
    stream = p.open(format=FORMAT,
                   channels=CHANNELS,
                   rate=RATE,
                   input=True,
                   frames_per_buffer=CHUNK)
    
    print("* recording")
    frames = []
    
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("* done recording")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return filepath

# ---------------- HELPERS ----------------
def transcribe_audio(wav_path: str) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Service error: {e}"
    except Exception as e:
        return f"Error: {e}"

def summarize_lsa(text: str, sentence_count: int = 3) -> str:
    if not text or not text.strip():
        return ""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(s) for s in summary)

def analyze_sentiment(text: str) -> str:
    if not text.strip():
        return "Neutral sentiment"
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive sentiment"
    elif polarity < 0:
        return "Negative sentiment"
    return "Neutral sentiment"

def convert_to_wav(src_path: str, src_filename: str) -> str:
    ext = os.path.splitext(src_filename.lower())[1].replace(".", "")
    if ext not in {"webm", "wav", "mp3", "m4a", "ogg"}:
        raise ValueError("Unsupported audio format. Use webm/wav/mp3/m4a/ogg.")
    audio = AudioSegment.from_file(src_path, format=ext if ext != "m4a" else "mp4")
    wav_path = src_path + ".wav"
    audio.export(wav_path, format="wav")
    return wav_path

# ---------------- ROUTES ----------------
from pydantic import BaseModel

class RecordingRequest(BaseModel):
    duration: int = 5

@app.post("/start_recording")
async def start_recording(request: RecordingRequest):
    try:
        print(f"Starting recording for {request.duration} seconds")
        audio_file = record_audio(request.duration)
        print(f"Audio recorded to {audio_file}")
        transcript = transcribe_audio(audio_file)
        print(f"Transcription: {transcript}")
        summary = summarize_lsa(transcript, sentence_count=3)
        sentiment = analyze_sentiment(summary)

        # Save to MongoDB
        entry = {
            "transcript": transcript,
            "summary": summary,
            "sentiment": sentiment,
            "timestamp": datetime.utcnow()
        }
        result = await collection.insert_one(entry)

        # Clean up the temporary file
        os.remove(audio_file)
        
        # Return entry without ObjectId for JSON serialization
        return {
            "transcript": transcript,
            "summary": summary,
            "sentiment": sentiment,
            "timestamp": entry["timestamp"].isoformat(),
            "id": str(result.inserted_id)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error recording audio: {str(e)}"}
        )

@app.post("/analyze_audio")
async def analyze_audio(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1] or 'webm'}") as tmp:
            content = await file.read()
            tmp.write(content)
            src_path = tmp.name

        wav_path = convert_to_wav(src_path, file.filename)
        transcript = transcribe_audio(wav_path)
        if transcript.startswith(("Service error:", "Error:")):
            return {"transcript": transcript, "summary": "", "sentiment": ""}

        summary = summarize_lsa(transcript, sentence_count=3)
        sentiment = analyze_sentiment(summary)

        # Save to MongoDB
        entry = {
            "transcript": transcript,
            "summary": summary,
            "sentiment": sentiment,
            "timestamp": datetime.utcnow()
        }
        result = await collection.insert_one(entry)

        # Return entry without ObjectId for JSON serialization
        return {
            "transcript": transcript,
            "summary": summary,
            "sentiment": sentiment,
            "timestamp": entry["timestamp"].isoformat(),
            "id": str(result.inserted_id)
        }
    except Exception as e:
        return {"transcript": f"Error processing audio: {e}", "summary": "", "sentiment": ""}
