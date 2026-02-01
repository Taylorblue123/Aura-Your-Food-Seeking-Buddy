"""
Confirmation-related Pydantic schemas for API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class ConfirmRequest(BaseModel):
    """Request schema for dish confirmation endpoint."""
    recommendation_id: str = Field(description="ID of the recommendation set")
    picked_dishes: List[str] = Field(
        min_length=1,
        description="List of recommendation IDs that the user picked"
    )
    skipped_dishes: List[str] = Field(
        default_factory=list,
        description="List of recommendation IDs that the user skipped"
    )


class ConfirmResponse(BaseModel):
    """Response schema for dish confirmation endpoint."""
    confirmation_id: str = Field(description="Unique identifier for this confirmation")
    session_id: str = Field(description="Associated session ID")
    recommendation_id: str = Field(description="Associated recommendation set ID")
    picked_count: int = Field(description="Number of dishes picked")
    skipped_count: int = Field(description="Number of dishes skipped")
    confirmed_at: datetime = Field(description="Timestamp of confirmation")
    message: str = Field(
        default="Selection confirmed! Enjoy your meal.",
        description="Confirmation message"
    )
