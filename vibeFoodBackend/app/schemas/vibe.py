"""
Vibe-related Pydantic schemas for API requests and responses.
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

from app.models.enums import VibeType


class VibeConstraints(BaseModel):
    """Dietary and preference constraints for vibe selection."""
    dietary_restrictions: List[str] = Field(
        default_factory=list,
        description="Dietary restrictions like 'vegetarian', 'vegan', 'gluten-free'"
    )
    allergies: List[str] = Field(
        default_factory=list,
        description="Food allergies to avoid"
    )
    max_spice: Optional[int] = Field(
        default=None,
        ge=0,
        le=5,
        description="Maximum spice level tolerance (0-5)"
    )


class VibeRequest(BaseModel):
    """Request schema for vibe submission endpoint."""
    menu_id: str = Field(description="ID of the menu to get recommendations for")
    vibes: List[str] = Field(
        min_length=1,
        max_length=3,
        description="Selected vibes (1-3 from: comfort, adventure, light, quick, sharing, budget, healthy, indulgent)"
    )
    party_size: int = Field(
        default=1,
        ge=1,
        le=20,
        description="Number of people dining"
    )
    budget_per_person: Optional[float] = Field(
        default=None,
        gt=0,
        description="Budget per person in local currency"
    )
    constraints: Optional[VibeConstraints] = Field(
        default=None,
        description="Dietary restrictions and preferences"
    )
    occasion: Optional[str] = Field(
        default=None,
        description="Special occasion like 'birthday', 'date_night', 'business'"
    )

    @field_validator("vibes")
    @classmethod
    def validate_vibes(cls, v: List[str]) -> List[str]:
        """Validate that all vibes are valid VibeType values."""
        valid_vibes = [vt.value for vt in VibeType]
        for vibe in v:
            if vibe not in valid_vibes:
                raise ValueError(
                    f"Invalid vibe '{vibe}'. Must be one of: {', '.join(valid_vibes)}"
                )
        return v


class VibeContext(BaseModel):
    """Context information about the vibe selection."""
    vibes: List[str] = Field(description="Selected vibes")
    party_size: int = Field(description="Number of diners")
    has_restrictions: bool = Field(description="Whether dietary restrictions were specified")
    occasion: Optional[str] = Field(default=None, description="Special occasion if specified")


class VibeResponse(BaseModel):
    """Response schema for vibe submission endpoint."""
    vibe_id: str = Field(description="Unique identifier for this vibe selection")
    menu_id: str = Field(description="Associated menu ID")
    context: VibeContext = Field(description="Summary of vibe context")
    created_at: datetime = Field(description="Timestamp of vibe submission")
    message: str = Field(
        default="Vibes recorded successfully. Ready for recommendations.",
        description="Status message"
    )


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    message: str
    error_code: Optional[str] = None
