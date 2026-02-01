"""
Session-related Pydantic schemas for API requests and responses.
"""
from pydantic import BaseModel, Field, constr
from typing import List, Optional, Any, Dict
from uuid import UUID, uuid4
from datetime import datetime


class SessionsRequest(BaseModel):
    """Request schema for session creation."""
    device_id: Optional[UUID] = Field(
        default=None,
        description="Device ID for returning users (UUID format)"
    )
    locale: constr(pattern=r'^[a-z]{2}-[A-Z]{2}$') = Field(
        description="ISO locale format (e.g., en-US, zh-CN)"
    )
    timezone: str = Field(
        description="IANA timezone format (e.g., America/Los_Angeles)"
    )
    app_version: constr(pattern=r'^\d+\.\d+\.\d+$') = Field(
        description="Client version in semver format (e.g., 1.0.0)"
    )


class SessionPreferences(BaseModel):
    """User preferences from device history."""
    allergies: Optional[List[str]] = Field(
        default_factory=list,
        description="Known allergies"
    )
    max_spice: Optional[int] = Field(
        default=None,
        ge=0,
        le=5,
        description="Maximum spice tolerance (0-5)"
    )
    dietary_restrictions: Optional[List[str]] = Field(
        default_factory=list,
        description="Dietary restrictions"
    )


class SessionsResponse(BaseModel):
    """Response schema for session creation."""
    session_id: UUID = Field(description="UUID v4 session identifier")
    created_at: datetime = Field(description="Session creation time (UTC)")
    expires_at: datetime = Field(description="Session expiration time (UTC)")
    preferences: Optional[SessionPreferences] = Field(
        default=None,
        description="User preferences (only present for returning users)"
    )


class MenuSummary(BaseModel):
    """Summary of menu data for session state."""
    menu_id: str
    item_count: int
    restaurant_name: Optional[str] = None
    extracted_at: datetime


class VibeSummary(BaseModel):
    """Summary of vibe data for session state."""
    vibe_id: str
    vibes: List[str]
    party_size: int
    created_at: datetime


class RecommendationSummary(BaseModel):
    """Summary of recommendations for session state."""
    recommendation_id: str
    count: int
    generated_at: datetime


class ConfirmationSummary(BaseModel):
    """Summary of confirmation for session state."""
    confirmation_id: str
    picked_count: int
    confirmed_at: datetime


class FeedbackSummary(BaseModel):
    """Summary of feedback for session state."""
    feedback_id: str
    rating: int
    submitted_at: datetime


class GetSessionResponse(BaseModel):
    """Response schema for getting session state."""
    session_id: str = Field(description="Session identifier")
    status: str = Field(description="Session status: active, expired, completed")
    current_step: str = Field(description="Current step in flow: created, menu, vibes, recommendations, confirmed")
    created_at: datetime = Field(description="Session creation time")
    expires_at: Optional[datetime] = Field(description="Session expiration time")

    # Optional data based on progress
    menu: Optional[MenuSummary] = Field(default=None, description="Menu data if scanned")
    vibes: Optional[VibeSummary] = Field(default=None, description="Vibe data if submitted")
    recommendations: Optional[RecommendationSummary] = Field(default=None, description="Recommendations if generated")
    confirmation: Optional[ConfirmationSummary] = Field(default=None, description="Confirmation if dishes confirmed")
    feedback: Optional[FeedbackSummary] = Field(default=None, description="Feedback if submitted")
