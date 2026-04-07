from elevenlabs.client import ElevenLabs
from app.config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def synthesize(text: str) -> bytes:
    try:
        # Removed language_code="ar" as it requires elevenlabs >= 1.50.0
        # The turbo_v2_5 model automatically detects Arabic script
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=ELEVENLABS_VOICE_ID,
            model_id="eleven_turbo_v2_5",
            output_format="mp3_44100_128",
        )
        return b"".join(audio)
    except Exception as e:
        print(f"\n[!!! TTS ERROR] Detail: {str(e)}\n")
        raise e