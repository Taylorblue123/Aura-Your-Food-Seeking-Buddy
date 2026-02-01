"""
Menu-related Pydantic schemas for API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class MenuItemSchema(BaseModel):
    """Schema for a menu item in API responses."""
    id: str = Field(description="Unique identifier for the menu item")
    name: str = Field(description="Name of the dish")
    description: Optional[str] = Field(default=None, description="Description of the dish")
    price: Optional[float] = Field(default=None, description="Price of the dish")
    currency: str = Field(default="USD", description="Currency code")
    category: Optional[str] = Field(default=None, description="Menu category")
    tags: List[str] = Field(default_factory=list, description="Tags like 'popular', 'spicy'")
    allergens: List[str] = Field(default_factory=list, description="List of allergens")
    spice_level: Optional[int] = Field(default=None, ge=0, le=5, description="Spice level 0-5")
    is_vegetarian: bool = Field(default=False, description="Is vegetarian")
    is_vegan: bool = Field(default=False, description="Is vegan")
    confidence: float = Field(default=1.0, ge=0, le=1, description="OCR confidence score")


class RestaurantSchema(BaseModel):
    """Schema for restaurant information."""
    name: Optional[str] = Field(default=None, description="Restaurant name")
    cuisine_type: Optional[str] = Field(default=None, description="Type of cuisine")
    address: Optional[str] = Field(default=None, description="Restaurant address")


class ScanMenuRequest(BaseModel):
    """Request schema for menu scanning endpoint."""
    image_base64: Optional[str] = Field(
        default=None,
        description="Base64 encoded menu image (optional for MVP fake implementation)"
    )


class ScanMenuResponse(BaseModel):
    """Response schema for menu scanning endpoint."""
    menu_id: str = Field(description="Unique identifier for the extracted menu")
    restaurant: Optional[RestaurantSchema] = Field(default=None, description="Detected restaurant info")
    items: List[MenuItemSchema] = Field(description="List of extracted menu items")
    item_count: int = Field(description="Number of items extracted")
    extraction_method: str = Field(description="Method used for extraction (ocr, manual, qr_code)")
    confidence: float = Field(ge=0, le=1, description="Overall extraction confidence")
    extracted_at: datetime = Field(description="Timestamp of extraction")
    warnings: List[str] = Field(default_factory=list, description="Any warnings about the extraction")
