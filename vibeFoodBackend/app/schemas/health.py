"""
Health check related Pydantic schemas for API responses.
"""
from pydantic import BaseModel, Field
from typing import Dict
from datetime import datetime


class ServiceStatus(BaseModel):
    """Status of an individual service component."""
    status: str = Field(description="Service status: 'healthy', 'degraded', or 'unhealthy'")
    latency_ms: float = Field(default=0, description="Response latency in milliseconds")
    message: Optional[str] = Field(default=None, description="Optional status message")


from typing import Optional


class HealthResponse(BaseModel):
    """Response schema for health check endpoint."""
    status: str = Field(description="Overall system status: 'healthy', 'degraded', or 'unhealthy'")
    version: str = Field(description="API version")
    timestamp: datetime = Field(description="Current server timestamp")
    services: Dict[str, str] = Field(
        default_factory=dict,
        description="Status of individual services"
    )
    uptime_seconds: Optional[float] = Field(
        default=None,
        description="Server uptime in seconds"
    )
