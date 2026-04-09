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
from app.services import ocr_service, llm_service

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

        # Validate base64 image data
        try:
            base64.b64decode(request.image_base64)
        except Exception:
            return ScanResponse(
                is_success=False,
                err_msg="Invalid image data: Base64 decoding failed"
            )

        # Process menu image with OCR service
        # Using device_id as session_id for MVP
        menu_data = await ocr_service.process_menu_image(
            session_id=request.device_id,
            image_base64=request.image_base64,
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
            "menu_language": menu_data.menu_language,
        }

        # Update user profile with current menu
        user_profile.current_menu = menu_json
        db.commit()

        # Extract restaurant summary for frontend intro page
        restaurant_info = menu_json.get("restaurant") or {}
        restaurant_name = restaurant_info.get("name")
        cuisine_type = restaurant_info.get("cuisine_type")
        items = menu_json.get("items", [])
        menu_item_count = len(items)
        categories = list({
            item.get("category")
            for item in items
            if item.get("category")
        })
        sample_items = [item.get("name", "") for item in items[:6]]
        menu_language = menu_json.get("menu_language")

        # Generate warm restaurant intro (non-blocking — fallback to None)
        restaurant_intro = None
        try:
            restaurant_intro = await llm_service.generate_restaurant_intro(
                restaurant_name=restaurant_name,
                cuisine_type=cuisine_type,
                categories=categories,
                sample_items=sample_items,
                menu_language=menu_language,
            )
        except Exception:
            pass  # Frontend handles None gracefully

        return ScanResponse(
            is_success=True,
            err_msg=None,
            restaurant_name=restaurant_name,
            cuisine_type=cuisine_type,
            menu_item_count=menu_item_count,
            menu_categories=categories if categories else None,
            restaurant_intro=restaurant_intro,
            menu_language=menu_language,
        )

    except Exception as e:
        db.rollback()
        return ScanResponse(
            is_success=False,
            err_msg=f"OCR processing failed: {str(e)}"
        )
