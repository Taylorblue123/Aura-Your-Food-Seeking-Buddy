"""
Scan endpoint schemas.
Used for menu photo upload and OCR processing.
"""
from pydantic import BaseModel, Field
from typing import Optional


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
