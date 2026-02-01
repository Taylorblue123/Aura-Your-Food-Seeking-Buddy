"""
Vibe-Food backend API router version 1

--- API aggregation.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import sessions, health

api_router = APIRouter()

# Session endpoints (create, scan-menu, vibes, recommendations, confirm, feedback, get)
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])

# Health check endpoint
api_router.include_router(health.router, prefix="/healthz", tags=["health"])
