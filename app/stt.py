import io
from openai import OpenAI
from app.config import OPENAI_API_KEY
import os

def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY") or OPENAI_API_KEY)

def transcribe(audio_bytes: bytes, filename="voice.webm") -> str:
    client = get_client()
    
    # Use io.BytesIO to wrap the bytes for the OpenAI SDK
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = filename 
    
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="ar",
        prompt="المحادثة بالعامية المصرية",
    )
    return response.text