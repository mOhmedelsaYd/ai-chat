import io
import base64
from app.stt import transcribe
from app.llm import generate_response
from app.tts import synthesize

# Simple in-memory session store
sessions = {}

async def run_pipeline(audio_bytes: bytes, session_id: str):
    """
    Runs the full voice-to-voice pipeline.
    """
    # Load conversation history from memory
    history = sessions.get(session_id, [])

    # 1. Speech → Text (Arabic Script from Whisper)
    transcript = transcribe(audio_bytes)

    # 2. Text → LLM reply (Structured JSON)
    # The LLM now returns a dict with 'franko' and 'arabic'
    reply_data = generate_response(transcript, history)
    reply_text_franko = reply_data.get("franko", "")
    reply_text_arabic = reply_data.get("arabic", "")

    # 3. Arabic Script → Voice (ElevenLabs likes Arabic script)
    # We use the Arabic version for TTS because it sounds way better than Franko
    reply_audio = synthesize(reply_text_arabic)

    # 4. Save updated history
    # We save the Franko version in history as it's the "persona" text
    history.extend([
        {"role": "user",      "content": transcript},
        {"role": "assistant", "content": reply_text_franko},
    ])
    sessions[session_id] = history[-16:]

    # Return the audio and the Franko text to be shown in the UI
    return reply_audio, reply_text_franko