from openai import OpenAI
from app.config import OPENAI_API_KEY
import os

def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = get_client()

def transcribe(audio_bytes: bytes, filename="voice.webm") -> str:
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=(filename, audio_bytes, "audio/webm"),
        language="ar",
        prompt="المحادثة بالعامية المصرية",
    )
    return response.text