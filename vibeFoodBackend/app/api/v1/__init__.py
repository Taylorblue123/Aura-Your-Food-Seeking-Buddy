"""
Vibe-Food backend API router version 1

--- API aggregation.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    check_in,
    register,
    scan,
    recommendation,
    feedback,
)

api_router = APIRouter()

# MVP endpoints (Device ID based, no session required)
api_router.include_router(check_in.router, prefix="/check-in", tags=["mvp"])
api_router.include_router(register.router, prefix="/register", tags=["mvp"])
api_router.include_router(scan.router, prefix="/scan", tags=["mvp"])
api_router.include_router(recommendation.router, prefix="/recommendation", tags=["mvp"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["mvp"])

# Health check endpoint
api_router.include_router(health.router, prefix="/healthz", tags=["health"])
