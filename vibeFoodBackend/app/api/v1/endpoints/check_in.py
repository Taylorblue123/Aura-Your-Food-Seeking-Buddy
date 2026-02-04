"""
Check-in endpoint for Vibe-Food MVP.
Checks if a device is registered on every app open.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user_profile import UserProfile
from app.schemas.check_in import CheckInRequest, CheckInResponse

router = APIRouter()


@router.post("", response_model=CheckInResponse)
async def check_in(request: CheckInRequest, db: Session = Depends(get_db)):
    """
    Check if a device is registered in the system.

    Called on every app open to determine if the user needs to register.

    - **device_id**: Unique device identifier from frontend

    Returns:
    - **is_registered**: True if device has a profile, False otherwise
    """
    try:
        user_profile = db.query(UserProfile).filter(
            UserProfile.device_id == request.device_id
        ).first()

        return CheckInResponse(
            is_registered=user_profile is not None,
            err_msg=None
        )
    except Exception as e:
        return CheckInResponse(
            is_registered=False,
            err_msg=f"Database error: {str(e)}"
        )
