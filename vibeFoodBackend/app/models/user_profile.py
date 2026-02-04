"""
SQLAlchemy UserProfile model for Vibe-Food application.
Stores user data identified by Device ID.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Text, JSON
from sqlalchemy.sql import func

from app.core.database import Base


class UserProfile(Base):
    """
    User profile table storing device-identified user data.

    Attributes:
        device_id: Unique device identifier (primary key)
        preference: User's preference selection (enum value)
        current_menu: JSON of current menu data from OCR
        current_vibe: JSON of current vibe selection
        current_recommendations: JSON of AI recommendations
        current_feedback: JSON of user feedback
        created_at: Profile creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "user_profiles"

    device_id = Column(String(255), primary_key=True, index=True)
    preference = Column(String(50), nullable=True)
    current_menu = Column(JSON, nullable=True)
    current_vibe = Column(JSON, nullable=True)
    current_recommendations = Column(JSON, nullable=True)
    current_feedback = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<UserProfile(device_id={self.device_id}, preference={self.preference})>"
