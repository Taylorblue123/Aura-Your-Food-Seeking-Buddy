"""
Feedback endpoint for Vibe-Food MVP.
Processes user feedback after filtering recommendation list.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user_profile import UserProfile
from app.schemas.mvp_feedback import MVPFeedbackRequest, MVPFeedbackResponse

router = APIRouter()


FEEDBACK_STRINGS = {
    "en": {
        "quick": "You made a quick decision!",
        "careful": "You took your time to choose carefully.",
        "thoughtful": "You were thoughtful in your selection.",
        "nothing": "Looks like nothing caught your eye this time.",
        "loved_all": "You loved everything we recommended!",
        "mild": "You seem to prefer milder flavors.",
        "great": "Great choices based on your vibe!",
    },
    "zh": {
        "quick": "你做了一个快速的决定！",
        "careful": "你花了时间仔细选择。",
        "thoughtful": "你的选择很用心。",
        "nothing": "看起来这次没有特别吸引你的。",
        "loved_all": "你喜欢我们推荐的每一道菜！",
        "mild": "你似乎更喜欢口味温和的菜品。",
        "great": "根据你的心情，选得很棒！",
    },
}


def generate_feedback_summary(
    picked_names: list,
    skipped_names: list,
    time_ms: int,
    recommendations: dict,
    menu_language: str = "en",
) -> str:
    """
    Generate a personalized feedback summary based on user choices.
    In production, this would call the LLM service.
    """
    s = FEEDBACK_STRINGS.get(menu_language, FEEDBACK_STRINGS["en"])

    # Analyze decision speed
    if time_ms < 30000:
        decision_speed = s["quick"]
    elif time_ms < 60000:
        decision_speed = s["careful"]
    else:
        decision_speed = s["thoughtful"]

    # Analyze preferences
    if len(picked_names) == 0:
        return f"{decision_speed} {s['nothing']}"

    if len(skipped_names) == 0:
        return f"{decision_speed} {s['loved_all']}"

    # Check for patterns in skipped items
    spicy_skipped = any("spicy" in name.lower() or "curry" in name.lower() for name in skipped_names)
    if spicy_skipped:
        return f"{decision_speed} {s['mild']}"

    return f"{decision_speed} {s['great']}"


def calculate_price_estimate(picked_names: list, recommendations: dict) -> str:
    """
    Calculate total price estimate from picked dishes.
    Returns a price range string like '$24-28'.
    """
    if not recommendations or not picked_names:
        return "$0"

    rec_list = recommendations.get("recommendations", [])
    total_low = 0
    total_high = 0

    for rec in rec_list:
        if rec.get("dish_name") in picked_names:
            try:
                price = float(rec.get("price", "0").replace("$", ""))
                total_low += price
                total_high += price + 2  # Add small variance
            except (ValueError, TypeError):
                pass

    if total_low == 0:
        return "$0"

    return f"${int(total_low)}-{int(total_high)}"


@router.post("", response_model=MVPFeedbackResponse)
async def submit_feedback(
    request: MVPFeedbackRequest,
    db: Session = Depends(get_db)
):
    """
    Submit feedback after user filters through recommendation list.

    - **device_id**: Unique device identifier
    - **picked_dish_names**: List of dishes the user selected
    - **skipped_dish_names**: List of dishes the user passed on
    - **time_to_decision_ms**: Client-measured decision time

    Returns:
    - **picked_count**: Number of dishes picked
    - **total_price_estimate**: Estimated price range
    - **summary**: AI-generated insight about user preferences
    """
    try:
        # Verify device is registered
        user_profile = db.query(UserProfile).filter(
            UserProfile.device_id == request.device_id
        ).first()

        if not user_profile:
            # Return minimal response for unregistered device
            return MVPFeedbackResponse(
                picked_count=len(request.picked_dish_names),
                total_price_estimate="$0",
                summary="Please register to get personalized insights."
            )

        # Get current recommendations for price calculation
        recommendations = user_profile.current_recommendations or {}
        menu_data = user_profile.current_menu or {}
        menu_language = menu_data.get("menu_language", "en") or "en"

        # Generate summary (fake LLM for MVP)
        summary = generate_feedback_summary(
            picked_names=request.picked_dish_names,
            skipped_names=request.skipped_dish_names,
            time_ms=request.time_to_decision_ms,
            recommendations=recommendations,
            menu_language=menu_language,
        )

        # Calculate price estimate
        price_estimate = calculate_price_estimate(
            picked_names=request.picked_dish_names,
            recommendations=recommendations
        )

        # Store feedback in profile
        feedback_data = {
            "picked_dish_names": request.picked_dish_names,
            "skipped_dish_names": request.skipped_dish_names,
            "time_to_decision_ms": request.time_to_decision_ms,
            "picked_count": len(request.picked_dish_names),
            "total_price_estimate": price_estimate,
            "summary": summary,
        }

        user_profile.current_feedback = feedback_data
        db.commit()

        return MVPFeedbackResponse(
            picked_count=len(request.picked_dish_names),
            total_price_estimate=price_estimate,
            summary=summary
        )

    except Exception as e:
        db.rollback()
        return MVPFeedbackResponse(
            picked_count=len(request.picked_dish_names),
            total_price_estimate="$0",
            summary=f"Error processing feedback: {str(e)}"
        )
