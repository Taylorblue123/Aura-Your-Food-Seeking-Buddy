"""
Transcription endpoint schemas.
Used for voice-to-text via OpenAI Whisper.
"""
from pydantic import BaseModel, Field
from typing import Optional


class TranscribeResponse(BaseModel):
    """Response schema for audio transcription."""
    is_success: bool = Field(
        description="Whether transcription was successful"
    )
    transcript: Optional[str] = Field(
        default=None,
        description="Transcribed text from audio"
    )
    err_msg: Optional[str] = Field(
        default=None,
        description="Error message if transcription failed"
    )
