"""
Registration endpoint schemas.
Used to register new users with Device ID and preference.
"""
from pydantic import BaseModel, Field
from typing import Optional

from app.models.enums import PreferenceType


class RegisterRequest(BaseModel):
    """Request schema for user registration."""
    device_id: str = Field(
        description="Unique device identifier"
    )
    preference: str = Field(
        description="User's preference selection (e.g., vegetarian, vegan, no_restriction)"
    )


class RegisterResponse(BaseModel):
    """Response schema for user registration."""
    is_success: bool = Field(
        description="Whether registration was successful"
    )
    err_msg: Optional[str] = Field(
        default=None,
        description="Error message if registration failed"
    )
