"""
Feedback-related Pydantic schemas for API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FeedbackRequest(BaseModel):
    """Request schema for feedback submission endpoint."""
    confirmation_id: str = Field(description="ID of the confirmation this feedback is for")
    rating: int = Field(
        ge=1,
        le=5,
        description="Rating from 1-5 stars"
    )
    comment: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional text feedback (max 500 characters)"
    )
    would_recommend: Optional[bool] = Field(
        default=None,
        description="Would you recommend this to a friend?"
    )


class FeedbackResponse(BaseModel):
    """Response schema for feedback submission endpoint."""
    feedback_id: str = Field(description="Unique identifier for this feedback")
    session_id: str = Field(description="Associated session ID")
    confirmation_id: str = Field(description="Associated confirmation ID")
    rating: int = Field(description="Submitted rating")
    submitted_at: datetime = Field(description="Timestamp of feedback submission")
    message: str = Field(
        default="Thank you for your feedback!",
        description="Acknowledgment message"
    )
