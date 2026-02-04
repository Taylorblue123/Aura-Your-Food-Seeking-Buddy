"""
Recommendation endpoint schemas for MVP.
Used for getting AI-powered dish recommendations.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class DishRecommendation(BaseModel):
    """Schema for a single dish recommendation."""
    dish_name: str = Field(description="Name of the recommended dish")
    reasoning: str = Field(description="Why this dish is recommended for the user")
    story: str = Field(description="A brief story or context about the dish")
    warnings: Optional[List[str]] = Field(
        default=None,
        description="Allergen or dietary warnings (e.g., 'Contains peanuts - please verify with staff')"
    )
    price: str = Field(description="Price of the dish as string")
    emoji: Optional[str] = Field(
        default=None,
        description="Emoji representing the dish mood"
    )


class MVPRecommendationRequest(BaseModel):
    """Request schema for MVP recommendation endpoint."""
    device_id: str = Field(
        description="Unique device identifier"
    )
    vibe_selection: str = Field(
        description="Selected vibe (comfort, adventure, light, quick, sharing, budget, healthy, indulgent)"
    )


class MVPRecommendationData(BaseModel):
    """Schema for recommendation data including summary and list."""
    brief_summary: str = Field(
        description="A one-sentence summary of the recommendations"
    )
    recommendations: List[DishRecommendation] = Field(
        description="List of dish recommendations"
    )


class MVPRecommendationResponse(BaseModel):
    """Response schema for MVP recommendation endpoint."""
    is_success: bool = Field(
        description="Whether recommendation generation was successful"
    )
    err_msg: Optional[str] = Field(
        default=None,
        description="Error message if recommendation failed"
    )
    recommendation: Optional[MVPRecommendationData] = Field(
        default=None,
        description="Recommendation data (only present on success)"
    )
