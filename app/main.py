import io
import base64
from fastapi import FastAPI, UploadFile, Header, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.pipeline import run_pipeline

app = FastAPI(title="Egyptian Arabic Voice Bot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    # Check if it's an ElevenLabs quota error
    if "quota_exceeded" in str(exc).lower():
        return JSONResponse(
            status_code=402, # Payment Required / Quota Exceeded
            content={"error": "QUOTA_EXCEEDED", "message": "ElevenLabs API credits ran out. Please check your dashboard."}
        )
    
    return JSONResponse(
        status_code=500,
        content={"error": "INTERNAL_SERVER_ERROR", "message": "An unexpected error occurred."}
    )


@app.get("/api/health")
async def health():
    from app.config import OPENAI_API_KEY, ELEVENLABS_API_KEY
    # Only return last 4 chars for security
    def mask(k): return f"...{k[-4:]}" if k and len(k) > 4 else "MISSING"
    
    return {
        "status": "ok",
        "keys_loaded": {
            "openai": mask(OPENAI_API_KEY),
            "elevenlabs": mask(ELEVENLABS_API_KEY)
        }
    }


@app.post("/api/voice/chat")
async def voice_chat(
    audio: UploadFile,
    x_session_id: str = Header(...),
):
    allowed = {"audio/webm", "audio/mpeg", "audio/wav",
               "audio/mp4", "audio/ogg", "audio/webm;codecs=opus",
               "application/octet-stream"}

    if audio.content_type not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format: {audio.content_type}"
        )

    audio_bytes = await audio.read()
    reply_audio, transcript = await run_pipeline(audio_bytes, x_session_id)

    # Encode transcript as base64 so Arabic text is safe in headers
    transcript_b64 = base64.b64encode(transcript.encode("utf-8")).decode("ascii")

    return StreamingResponse(
        io.BytesIO(reply_audio),
        media_type="audio/mpeg",
        headers={
            "X-Transcript-B64": transcript_b64,
            "X-Session-Id": x_session_id,
            "Access-Control-Expose-Headers": "X-Transcript-B64, X-Session-Id",
        },
    )


@app.delete("/api/voice/session/{session_id}")
async def clear_session(session_id: str):
    from app.pipeline import sessions
    sessions.pop(session_id, None)
    return JSONResponse({"cleared": session_id})