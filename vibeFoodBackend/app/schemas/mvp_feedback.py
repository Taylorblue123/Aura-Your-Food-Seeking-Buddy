"""
Feedback endpoint schemas for MVP.
Used for submitting user feedback after filtering recommendations.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class MVPFeedbackRequest(BaseModel):
    """Request schema for MVP feedback endpoint."""
    device_id: str = Field(
        description="Unique device identifier"
    )
    picked_dish_names: List[str] = Field(
        description="List of dish names the user selected"
    )
    skipped_dish_names: List[str] = Field(
        description="List of dish names the user skipped"
    )
    time_to_decision_ms: int = Field(
        description="Time taken to make decision in milliseconds (client-side measured)"
    )


class MVPFeedbackResponse(BaseModel):
    """Response schema for MVP feedback endpoint."""
    picked_count: int = Field(
        description="Number of dishes picked"
    )
    total_price_estimate: str = Field(
        description="Estimated total price range (e.g., '$24-28')"
    )
    summary: str = Field(
        description="AI-generated summary of user preferences (e.g., 'You don't like spicy food, and a bit hesitate')"
    )
