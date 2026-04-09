"""
Transcription endpoint for Vibe-Food MVP.
Handles audio upload and speech-to-text via OpenAI Whisper.
"""
import io
import logging

from fastapi import APIRouter, File, UploadFile
from app.core.config import settings
from app.schemas.transcribe import TranscribeResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("", response_model=TranscribeResponse)
async def transcribe_audio(audio: UploadFile = File(...)):
    """
    Transcribe audio to text using OpenAI Whisper API.

    Accepts audio file (webm, wav, mp3, m4a) as multipart upload.
    Returns transcribed text.
    """
    if not settings.OPENAI_API_KEY:
        return TranscribeResponse(
            is_success=False,
            err_msg="Voice input requires API key. Please use vibe buttons instead."
        )

    try:
        from app.services.openai_client import get_openai_client
        client = get_openai_client()

        # Read audio data
        audio_data = await audio.read()
        if len(audio_data) < 1000:  # Very small file = likely too short
            return TranscribeResponse(
                is_success=False,
                err_msg="Recording too short. Hold the button and speak."
            )

        # Determine file extension from content type or filename
        # Browser may send content_type like "audio/webm;codecs=opus" — strip params
        content_type = (audio.content_type or "").split(";")[0].strip().lower()
        type_map = {
            "audio/webm": ("webm", "audio/webm"),
            "audio/wav": ("wav", "audio/wav"),
            "audio/wave": ("wav", "audio/wav"),
            "audio/x-wav": ("wav", "audio/wav"),
            "audio/mp3": ("mp3", "audio/mpeg"),
            "audio/mpeg": ("mp3", "audio/mpeg"),
            "audio/mp4": ("m4a", "audio/mp4"),
            "audio/m4a": ("m4a", "audio/mp4"),
            "audio/ogg": ("ogg", "audio/ogg"),
            "audio/x-m4a": ("m4a", "audio/mp4"),
            "video/webm": ("webm", "audio/webm"),  # some browsers send video/webm for audio
        }

        # Also check the uploaded filename for extension hints
        upload_name = audio.filename or ""
        ext, mime = type_map.get(content_type, ("webm", "audio/webm"))
        if upload_name.endswith(".m4a"):
            ext, mime = "m4a", "audio/mp4"
        elif upload_name.endswith(".ogg"):
            ext, mime = "ogg", "audio/ogg"

        filename = f"recording.{ext}"

        logger.info(
            "Transcribing audio (%d bytes, content_type=%s, resolved=%s/%s)",
            len(audio_data), audio.content_type, filename, mime
        )

        # Use tuple format for reliable file upload to OpenAI
        response = await client.audio.transcriptions.create(
            model="whisper-1",
            file=(filename, audio_data, mime),
        )

        transcript = response.text.strip()
        if not transcript:
            return TranscribeResponse(
                is_success=False,
                err_msg="Couldn't hear anything. Please try again."
            )

        logger.info("Transcription complete: '%s'", transcript[:100])
        return TranscribeResponse(
            is_success=True,
            transcript=transcript,
        )

    except Exception as e:
        logger.error("Transcription failed: %s", e)
        return TranscribeResponse(
            is_success=False,
            err_msg=f"Transcription failed: {str(e)}"
        )
