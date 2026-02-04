"""
Recommendation endpoint for Vibe-Food MVP.
Returns AI-powered dish recommendations based on vibe selection.
"""
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

router = APIRouter()

# Vibe to emoji mapping
VIBE_EMOJIS = {
    "comfort": "🍲",
    "adventure": "🌶️",
    "light": "🥗",
    "quick": "⚡",
    "sharing": "🍻",
    "budget": "💰",
    "healthy": "🥬",
    "indulgent": "🍰",
}

# Fake LLM recommendations based on vibe
VIBE_RECOMMENDATIONS = {
    "comfort": [
        DishRecommendation(
            dish_name="Massaman Curry",
            reasoning="Rich and mild curry that feels like a warm hug",
            story="A comfort classic with tender meat and potatoes",
            warnings=["Contains peanuts - please verify with staff"],
            price="16",
            emoji="🍛"
        ),
        DishRecommendation(
            dish_name="Pad Thai",
            reasoning="A beloved classic with perfect sweet-savory balance",
            story="The most popular Thai dish for good reason",
            warnings=["Contains peanuts", "Contains eggs"],
            price="14",
            emoji="🍜"
        ),
    ],
    "adventure": [
        DishRecommendation(
            dish_name="Tom Yum Soup",
            reasoning="Bold flavors that awaken your taste buds",
            story="An exciting journey of sour, spicy, and aromatic notes",
            warnings=["Very spicy", "Contains shellfish"],
            price="12",
            emoji="🌶️"
        ),
        DishRecommendation(
            dish_name="Green Curry",
            reasoning="Aromatic and spicy with complex flavors",
            story="A Thai curry adventure with authentic heat",
            warnings=["Spicy", "Contains coconut"],
            price="15",
            emoji="🥘"
        ),
    ],
    "light": [
        DishRecommendation(
            dish_name="Spring Rolls",
            reasoning="Fresh and crispy without being heavy",
            story="A light start that won't weigh you down",
            warnings=None,
            price="7",
            emoji="🥟"
        ),
        DishRecommendation(
            dish_name="Tom Yum Soup",
            reasoning="Light broth-based soup full of fresh flavors",
            story="Refreshing and cleansing for the palate",
            warnings=["Spicy"],
            price="9",
            emoji="🍲"
        ),
    ],
    "quick": [
        DishRecommendation(
            dish_name="Pad Thai",
            reasoning="Quick to prepare and quick to enjoy",
            story="A fast favorite that never disappoints",
            warnings=["Contains peanuts"],
            price="14",
            emoji="⚡"
        ),
        DishRecommendation(
            dish_name="Spring Rolls",
            reasoning="Ready fast, perfect for a quick bite",
            story="Crispy satisfaction in minutes",
            warnings=None,
            price="7",
            emoji="🥟"
        ),
    ],
    "sharing": [
        DishRecommendation(
            dish_name="Spring Rolls",
            reasoning="Perfect for passing around the table",
            story="A crowd-pleaser that brings people together",
            warnings=None,
            price="7",
            emoji="🥟"
        ),
        DishRecommendation(
            dish_name="Pad Thai",
            reasoning="A generous portion great for sharing",
            story="Everyone's favorite to share",
            warnings=["Contains peanuts"],
            price="14",
            emoji="🍜"
        ),
    ],
    "budget": [
        DishRecommendation(
            dish_name="Spring Rolls",
            reasoning="Great value without compromising taste",
            story="Budget-friendly and delicious",
            warnings=None,
            price="7",
            emoji="💰"
        ),
        DishRecommendation(
            dish_name="Tom Yum Soup",
            reasoning="Filling and flavorful at a great price",
            story="Maximum flavor for minimum spend",
            warnings=["Spicy"],
            price="9",
            emoji="🍲"
        ),
    ],
    "healthy": [
        DishRecommendation(
            dish_name="Tom Yum Soup",
            reasoning="Low calorie, high flavor, immune-boosting",
            story="A healthy choice packed with herbs and spices",
            warnings=["Spicy"],
            price="9",
            emoji="🥗"
        ),
        DishRecommendation(
            dish_name="Spring Rolls",
            reasoning="Light and veggie-packed",
            story="Fresh vegetables in a light wrapper",
            warnings=None,
            price="7",
            emoji="🥬"
        ),
    ],
    "indulgent": [
        DishRecommendation(
            dish_name="Mango Sticky Rice",
            reasoning="Sweet, creamy, and absolutely decadent",
            story="A heavenly dessert you deserve",
            warnings=["Contains coconut"],
            price="8",
            emoji="🥭"
        ),
        DishRecommendation(
            dish_name="Massaman Curry",
            reasoning="Rich, creamy, and deeply satisfying",
            story="Treat yourself to this indulgent curry",
            warnings=["Contains peanuts", "Contains coconut"],
            price="16",
            emoji="🍛"
        ),
    ],
}

# Brief summaries by vibe
VIBE_SUMMARIES = {
    "comfort": "Here are some warming, comforting dishes to soothe your soul.",
    "adventure": "Ready for a flavor adventure? These dishes will excite your palate!",
    "light": "Light and refreshing options that won't weigh you down.",
    "quick": "Fast favorites when you're short on time but not on taste.",
    "sharing": "Perfect dishes for bringing the table together.",
    "budget": "Great taste without breaking the bank.",
    "healthy": "Nutritious choices that don't sacrifice flavor.",
    "indulgent": "Go ahead, treat yourself to these decadent delights.",
}


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
        valid_vibes = [v.value for v in VibeType]
        if vibe not in valid_vibes:
            return MVPRecommendationResponse(
                is_success=False,
                err_msg=f"Invalid vibe. Must be one of: {', '.join(valid_vibes)}",
                recommendation=None
            )

        # Update current vibe in profile
        user_profile.current_vibe = {"vibe": vibe}

        # Get recommendations based on vibe (fake LLM for MVP)
        recommendations = VIBE_RECOMMENDATIONS.get(vibe, VIBE_RECOMMENDATIONS["comfort"])
        summary = VIBE_SUMMARIES.get(vibe, VIBE_SUMMARIES["comfort"])

        # Store recommendations in profile
        recommendation_data = MVPRecommendationData(
            brief_summary=summary,
            recommendations=recommendations
        )

        user_profile.current_recommendations = recommendation_data.model_dump()
        db.commit()

        return MVPRecommendationResponse(
            is_success=True,
            err_msg=None,
            recommendation=recommendation_data
        )

    except Exception as e:
        db.rollback()
        return MVPRecommendationResponse(
            is_success=False,
            err_msg=f"Recommendation failed: {str(e)}",
            recommendation=None
        )
