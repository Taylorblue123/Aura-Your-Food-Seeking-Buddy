"""
Scan endpoint schemas.
Used for menu photo upload and OCR processing.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class ScanRequest(BaseModel):
    """Request schema for menu scan."""
    device_id: str = Field(
        description="Unique device identifier"
    )
    image_base64: str = Field(
        description="Base64 encoded menu image"
    )


class ScanResponse(BaseModel):
    """Response schema for menu scan."""
    is_success: bool = Field(
        description="Whether image upload and OCR were successful"
    )
    err_msg: Optional[str] = Field(
        default=None,
        description="Error message if scan failed (upload or OCR)"
    )
    restaurant_name: Optional[str] = Field(
        default=None,
        description="Restaurant name extracted from menu (if detected)"
    )
    cuisine_type: Optional[str] = Field(
        default=None,
        description="Cuisine type detected from menu"
    )
    menu_item_count: Optional[int] = Field(
        default=None,
        description="Number of menu items extracted"
    )
    menu_categories: Optional[List[str]] = Field(
        default=None,
        description="Unique menu categories found (e.g., Appetizers, Mains)"
    )
    restaurant_intro: Optional[str] = Field(
        default=None,
        description="LLM-generated warm introduction about the restaurant"
    )
    menu_language: Optional[str] = Field(
        default=None,
        description="Detected language of the menu (e.g., 'en', 'zh', 'ja')"
    )
