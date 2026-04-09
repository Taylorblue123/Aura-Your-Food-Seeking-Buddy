"""
Recommendation endpoint for Vibe-Food MVP.
Returns AI-powered dish recommendations based on vibe selection.
"""
import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user_profile import UserProfile
from app.models.enums import VibeType
from app.schemas.mvp_recommendation import (
    MVPRecommendationRequest,
    MVPRecommendationResponse,
    MVPRecommendationData,
    DishRecommendation,
)
from app.services import llm_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("", response_model=MVPRecommendationResponse)
async def get_recommendations(
    request: MVPRecommendationRequest,
    db: Session = Depends(get_db)
):
    """
    Get AI-powered dish recommendations based on vibe selection.

    Flow: Update current vibe -> Call LLM service -> Update recommendations -> Response

    - **device_id**: Unique device identifier
    - **vibe_selection**: Selected vibe mood

    Returns:
    - **is_success**: True if recommendation was successful
    - **recommendation**: Object with brief_summary and recommendations list
    """
    try:
        # Verify device is registered
        user_profile = db.query(UserProfile).filter(
            UserProfile.device_id == request.device_id
        ).first()

        if not user_profile:
            return MVPRecommendationResponse(
                is_success=False,
                err_msg="Device not registered. Please register first.",
                recommendation=None
            )

        # Check if menu has been scanned
        if not user_profile.current_menu:
            return MVPRecommendationResponse(
                is_success=False,
                err_msg="No menu found. Please scan a menu first.",
                recommendation=None
            )

        # Validate vibe selection
        vibe = request.vibe_selection.lower()
        voice_prompt = request.voice_prompt

        if vibe == "voice":
            # Voice input mode — skip enum validation
            if not voice_prompt or not voice_prompt.strip():
                return MVPRecommendationResponse(
                    is_success=False,
                    err_msg="Voice prompt is empty. Please try again or select a vibe.",
                    recommendation=None
                )
            user_profile.current_vibe = {"vibe": "voice", "voice_prompt": voice_prompt}
        else:
            # Standard vibe mode
            valid_vibes = [v.value for v in VibeType]
            if vibe not in valid_vibes:
                return MVPRecommendationResponse(
                    is_success=False,
                    err_msg=f"Invalid vibe. Must be one of: {', '.join(valid_vibes)}",
                    recommendation=None
                )
            user_profile.current_vibe = {"vibe": vibe}

        # Get AI-powered recommendations
        menu_data = user_profile.current_menu
        result = await llm_service.generate_recommendations(
            menu_items=menu_data.get("items", []),
            vibe=vibe,
            preference=user_profile.preference or "no_restriction",
            restaurant_info=menu_data.get("restaurant"),
            menu_language=menu_data.get("menu_language"),
            voice_prompt=voice_prompt,
        )

        # Parse into schema objects
        recommendations = [
            DishRecommendation(
                dish_name=rec.get("dish_name", "Unknown"),
                reasoning=rec.get("reasoning", ""),
                story=rec.get("story", ""),
                warnings=rec.get("warnings"),
                price=str(rec.get("price", "Ask staff")),
                emoji=rec.get("emoji"),
            )
            for rec in result.get("recommendations", [])
        ]

        recommendation_data = MVPRecommendationData(
            brief_summary=result.get("brief_summary", "Here are our recommendations for you."),
            recommendations=recommendations,
        )

        # Store recommendations in profile
        user_profile.current_recommendations = recommendation_data.model_dump()
        db.commit()

        return MVPRecommendationResponse(
            is_success=True,
            err_msg=None,
            recommendation=recommendation_data
        )

    except Exception as e:
        db.rollback()
        logger.error("Recommendation endpoint error: %s", e)
        return MVPRecommendationResponse(
            is_success=False,
            err_msg=f"Recommendation failed: {str(e)}",
            recommendation=None
        )
