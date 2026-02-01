"""
Recommendation-related Pydantic schemas for API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class RecommendationItemSchema(BaseModel):
    """Schema for a single recommendation in API responses."""
    id: str = Field(description="Unique identifier for this recommendation")
    menu_item_id: str = Field(description="ID of the corresponding menu item")
    name: str = Field(description="Name of the recommended dish")
    reason: str = Field(description="AI-generated reason for this recommendation")
    match_score: float = Field(ge=0, le=1, description="How well this matches user's vibes (0-1)")
    vibe_matches: List[str] = Field(default_factory=list, description="Which vibes this dish matches")
    price: Optional[float] = Field(default=None, description="Price of the dish")
    warnings: List[str] = Field(default_factory=list, description="Allergen or dietary warnings")
    tags: List[str] = Field(default_factory=list, description="Dish tags")


class RecommendationRequest(BaseModel):
    """Request schema for recommendations endpoint."""
    vibe_id: str = Field(description="ID of the vibe selection")
    menu_id: str = Field(description="ID of the menu to recommend from")
    count: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Number of recommendations to return (1-5)"
    )


class RecommendationResponse(BaseModel):
    """Response schema for recommendations endpoint."""
    recommendation_id: str = Field(description="Unique identifier for this recommendation set")
    vibe_id: str = Field(description="Associated vibe selection ID")
    menu_id: str = Field(description="Associated menu ID")
    recommendations: List[RecommendationItemSchema] = Field(description="List of dish recommendations")
    reasoning_summary: str = Field(description="AI-generated summary of the recommendation logic")
    confidence: float = Field(ge=0, le=1, description="Overall confidence in recommendations")
    generated_at: datetime = Field(description="Timestamp of recommendation generation")
    model_version: str = Field(description="Version of the AI model used")
