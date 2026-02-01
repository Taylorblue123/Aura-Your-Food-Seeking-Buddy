"""
Health check endpoint for Vibe-Food API.
"""
from datetime import datetime
from fastapi import APIRouter

from app.core.config import settings
from app.schemas.health import HealthResponse

router = APIRouter()

# Track server start time for uptime calculation
_server_start_time = datetime.utcnow()


@router.get("", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns overall system status and individual service health.
    Used for monitoring and load balancer health checks.
    """
    now = datetime.utcnow()
    uptime = (now - _server_start_time).total_seconds()

    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        timestamp=now,
        services={
            "api": "healthy",
            "database": "healthy",  # Fake DB is always healthy
            "ocr": "healthy",  # Fake OCR is always healthy
            "llm": "healthy",  # Fake LLM is always healthy
        },
        uptime_seconds=uptime,
    )
