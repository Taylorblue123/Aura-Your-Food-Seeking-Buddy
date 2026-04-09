"""
Registration endpoint schemas.
Used to register new users with Device ID and preference.
"""
from pydantic import BaseModel, Field
from typing import List, Optional

from app.models.enums import PreferenceType


class RegisterRequest(BaseModel):
    """Request schema for user registration."""
    device_id: str = Field(
        description="Unique device identifier"
    )
    preference: List[str] = Field(
        description="User's dietary preference selections (e.g., ['vegetarian', 'nut_free']). Send ['no_restriction'] if none."
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
