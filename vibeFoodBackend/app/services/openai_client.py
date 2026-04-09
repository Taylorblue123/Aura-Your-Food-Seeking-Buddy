"""
Shared OpenAI async client for OCR and recommendation services.
"""
from typing import Optional
from openai import AsyncOpenAI
from app.core.config import settings

_client: Optional[AsyncOpenAI] = None


def get_openai_client() -> AsyncOpenAI:
    """Get or create the shared AsyncOpenAI client."""
    global _client
    if _client is None:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError(
                "OPENAI_API_KEY not configured. Set it in .env or environment variables."
            )
        _client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    return _client
