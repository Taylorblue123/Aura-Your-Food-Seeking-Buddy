"""
Vibe-Food Backend API - FastAPI application initialization.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import init_db
from app.api.v1 import api_router
from app.utils.errors import AppError


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables on startup."""
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Food recommendation MVP API - Users scan menus, select vibes, and get AI-powered dish recommendations.",
    lifespan=lifespan,
)

# CORS middleware - allow all origins for MVP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    """Handle custom application errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Vibe-Food API",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/openapi.json",
    }
