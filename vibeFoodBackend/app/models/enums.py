"""
Enumeration types for Vibe-Food application.
"""
from enum import Enum


class VibeType(str, Enum):
    """Eight mood/vibe selections for food recommendations."""
    COMFORT = "comfort"
    ADVENTURE = "adventure"
    LIGHT = "light"
    QUICK = "quick"
    SHARING = "sharing"
    BUDGET = "budget"
    HEALTHY = "healthy"
    INDULGENT = "indulgent"


class SessionStatus(str, Enum):
    """Status of a user session."""
    ACTIVE = "active"
    EXPIRED = "expired"
    COMPLETED = "completed"


class SessionStep(str, Enum):
    """Current step in the session flow."""
    CREATED = "created"
    MENU = "menu"
    VIBES = "vibes"
    RECOMMENDATIONS = "recommendations"
    CONFIRMED = "confirmed"


class ExtractionMethod(str, Enum):
    """Method used for menu extraction."""
    OCR = "ocr"
    MANUAL = "manual"
    QR_CODE = "qr_code"


class CelebrationType(str, Enum):
    """Types of celebrations/occasions."""
    NONE = "none"
    BIRTHDAY = "birthday"
    ANNIVERSARY = "anniversary"
    DATE_NIGHT = "date_night"
    BUSINESS = "business"
    CASUAL = "casual"
