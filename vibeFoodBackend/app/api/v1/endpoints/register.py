"""
Register endpoint for Vibe-Food MVP.
Creates a new user profile with Device ID and preference.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user_profile import UserProfile
from app.schemas.register import RegisterRequest, RegisterResponse

router = APIRouter()


@router.post("", response_model=RegisterResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user with device ID and preference.

    Called on first use when device has no record in database.

    - **device_id**: Unique device identifier
    - **preference**: User's dietary preference selection

    Returns:
    - **is_success**: True if registration was successful
    - **err_msg**: Error message if registration failed
    """
    try:
        # Check if device already registered
        existing = db.query(UserProfile).filter(
            UserProfile.device_id == request.device_id
        ).first()

        if existing:
            return RegisterResponse(
                is_success=False,
                err_msg="Device already registered"
            )

        # Create new user profile
        user_profile = UserProfile(
            device_id=request.device_id,
            preference=request.preference
        )

        db.add(user_profile)
        db.commit()

        return RegisterResponse(
            is_success=True,
            err_msg=None
        )
    except Exception as e:
        db.rollback()
        return RegisterResponse(
            is_success=False,
            err_msg=f"Registration failed: {str(e)}"
        )
