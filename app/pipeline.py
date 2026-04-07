import io
import base64
from app.stt import transcribe
from app.llm import generate_response
from app.tts import synthesize

# Simple in-memory session store
sessions = {}

async def run_pipeline(audio_bytes: bytes, session_id: str):
    """
    Runs the full voice-to-voice pipeline using OpenAI and ElevenLabs.
    """
    # Load conversation history from memory
    history = sessions.get(session_id, [])

    # 1. Speech → Text (High-quality Arabic from Whisper)
    transcript = transcribe(audio_bytes)

    # 2. Text → LLM reply (Structured JSON for Franko/Arabic balance)
    reply_data = generate_response(transcript, history)
    reply_text_franko = reply_data.get("franko", "")
    reply_text_arabic = reply_data.get("arabic", "")

    # 3. Arabic Script → Voice (TTS is much more natural with Arabic script)
    reply_audio = synthesize(reply_text_arabic)

    # 4. Save updated history
    # We save the Franko version in history for consistency
    history.extend([
        {"role": "user",      "content": transcript},
        {"role": "assistant", "content": reply_text_franko},
    ])
    sessions[session_id] = history[-16:]

    # Return the audio and the Franko text to be shown in the UI
    return reply_audio, reply_text_franko