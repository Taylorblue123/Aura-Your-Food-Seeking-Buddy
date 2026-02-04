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


class ExtractionMethod(str, Enum):
    """Method used for menu extraction."""
    OCR = "ocr"
    MANUAL = "manual"
    QR_CODE = "qr_code"


class PreferenceType(str, Enum):
    """User dietary preference types for registration."""
    NO_RESTRICTION = "no_restriction"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    HALAL = "halal"
    KOSHER = "kosher"
    GLUTEN_FREE = "gluten_free"
    DAIRY_FREE = "dairy_free"
    NUT_FREE = "nut_free"
