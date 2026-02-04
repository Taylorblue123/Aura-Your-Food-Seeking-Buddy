"""
Scan endpoint for Vibe-Food MVP.
Handles menu photo upload and OCR processing.
"""
import base64
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user_profile import UserProfile
from app.schemas.scan import ScanRequest, ScanResponse
from app.services import ocr_service

router = APIRouter()


@router.post("", response_model=ScanResponse)
async def scan_menu(request: ScanRequest, db: Session = Depends(get_db)):
    """
    Upload menu photo and run OCR to extract menu items.

    Flow: Save Image -> Call OCR service -> Update DB -> Response -> Delete Image
    Image data is ephemeral (deleted after OCR) for privacy.

    - **device_id**: Unique device identifier
    - **image_base64**: Base64 encoded menu image

    Returns:
    - **is_success**: True if both upload and OCR succeeded
    - **err_msg**: Error message if any step failed
    """
    try:
        # Verify device is registered
        user_profile = db.query(UserProfile).filter(
            UserProfile.device_id == request.device_id
        ).first()

        if not user_profile:
            return ScanResponse(
                is_success=False,
                err_msg="Device not registered. Please register first."
            )

        # Validate and decode base64 image
        try:
            image_data = base64.b64decode(request.image_base64)
        except Exception:
            return ScanResponse(
                is_success=False,
                err_msg="Invalid image data: Base64 decoding failed"
            )

        # Process menu image with OCR service
        # Using device_id as session_id for MVP
        menu_data = await ocr_service.process_menu_image(
            session_id=request.device_id,
            image_data=image_data,
        )

        # Convert menu_data to JSON-serializable dict
        menu_json = {
            "id": menu_data.id,
            "items": [
                {
                    "id": item.id,
                    "name": item.name,
                    "description": item.description,
                    "price": item.price,
                    "currency": item.currency,
                    "category": item.category,
                    "tags": item.tags,
                    "allergens": item.allergens,
                    "spice_level": item.spice_level,
                    "is_vegetarian": item.is_vegetarian,
                    "is_vegan": item.is_vegan,
                }
                for item in menu_data.items
            ],
            "restaurant": {
                "name": menu_data.restaurant.name if menu_data.restaurant else None,
                "cuisine_type": menu_data.restaurant.cuisine_type if menu_data.restaurant else None,
            } if menu_data.restaurant else None,
            "extraction_method": menu_data.extraction_method.value,
            "confidence": menu_data.confidence,
        }

        # Update user profile with current menu
        user_profile.current_menu = menu_json
        db.commit()

        # Image data is already ephemeral (not stored permanently)
        return ScanResponse(
            is_success=True,
            err_msg=None
        )

    except Exception as e:
        db.rollback()
        return ScanResponse(
            is_success=False,
            err_msg=f"OCR processing failed: {str(e)}"
        )
