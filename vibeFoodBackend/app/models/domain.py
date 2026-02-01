"""
Domain models for Vibe-Food application.
Internal data classes representing core business entities.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4

from app.models.enums import VibeType, SessionStatus, SessionStep, ExtractionMethod


@dataclass
class MenuItem:
    """Represents a single menu item extracted from OCR or manual input."""
    id: str
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    currency: str = "USD"
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    allergens: List[str] = field(default_factory=list)
    spice_level: Optional[int] = None  # 0-5
    is_vegetarian: bool = False
    is_vegan: bool = False
    confidence: float = 1.0  # OCR confidence score


@dataclass
class Restaurant:
    """Restaurant information extracted from menu."""
    name: Optional[str] = None
    cuisine_type: Optional[str] = None
    address: Optional[str] = None


@dataclass
class MenuData:
    """Complete menu data from OCR extraction."""
    id: str
    session_id: str
    items: List[MenuItem] = field(default_factory=list)
    restaurant: Optional[Restaurant] = None
    extraction_method: ExtractionMethod = ExtractionMethod.OCR
    confidence: float = 0.0
    extracted_at: datetime = field(default_factory=datetime.utcnow)
    raw_text: Optional[str] = None
    warnings: List[str] = field(default_factory=list)


@dataclass
class VibeData:
    """User's vibe selection and constraints."""
    id: str
    session_id: str
    menu_id: str
    vibes: List[VibeType] = field(default_factory=list)
    party_size: int = 1
    budget_per_person: Optional[float] = None
    dietary_restrictions: List[str] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)
    max_spice: Optional[int] = None
    occasion: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Recommendation:
    """A single dish recommendation."""
    id: str
    menu_item_id: str
    name: str
    reason: str
    match_score: float  # 0.0 - 1.0
    vibe_matches: List[str] = field(default_factory=list)
    price: Optional[float] = None
    warnings: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class RecommendationSet:
    """Set of recommendations for a session."""
    id: str
    session_id: str
    vibe_id: str
    menu_id: str
    recommendations: List[Recommendation] = field(default_factory=list)
    reasoning_summary: str = ""
    confidence: float = 0.0
    generated_at: datetime = field(default_factory=datetime.utcnow)
    model_version: str = "fake-v1"


@dataclass
class Confirmation:
    """User's confirmed dish selection."""
    id: str
    session_id: str
    recommendation_id: str
    picked_dishes: List[str] = field(default_factory=list)  # dish IDs
    skipped_dishes: List[str] = field(default_factory=list)  # dish IDs
    confirmed_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Feedback:
    """User feedback on recommendations."""
    id: str
    session_id: str
    confirmation_id: str
    rating: int  # 1-5
    comment: Optional[str] = None
    would_recommend: Optional[bool] = None
    submitted_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Session:
    """User session tracking the entire recommendation flow."""
    id: str
    device_id: Optional[str] = None
    locale: str = "en-US"
    timezone: str = "UTC"
    app_version: str = "1.0.0"
    status: SessionStatus = SessionStatus.ACTIVE
    current_step: SessionStep = SessionStep.CREATED
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None

    # Session data references
    menu_data: Optional[MenuData] = None
    vibe_data: Optional[VibeData] = None
    recommendation_set: Optional[RecommendationSet] = None
    confirmation: Optional[Confirmation] = None
    feedback: Optional[Feedback] = None

    # User preferences (from device history)
    preferences: Optional[Dict[str, Any]] = None
