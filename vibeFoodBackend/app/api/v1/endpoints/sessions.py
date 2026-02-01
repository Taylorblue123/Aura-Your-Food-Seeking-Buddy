"""
Session endpoints for Vibe-Food API.
Handles the complete recommendation flow: create session, scan menu,
submit vibes, get recommendations, confirm dishes, submit feedback.
"""
from datetime import datetime
from uuid import uuid4, UUID
from fastapi import APIRouter, HTTPException, Path

from app.models.domain import VibeData, Confirmation
from app.models.enums import SessionStatus, SessionStep, VibeType
from app.services.fake_database import db
from app.services import ocr_service, llm_service, feedback_service
from app.schemas.sessions import (
    SessionsRequest,
    SessionsResponse,
    SessionPreferences,
    GetSessionResponse,
    MenuSummary,
    VibeSummary,
    RecommendationSummary,
    ConfirmationSummary,
    FeedbackSummary,
)
from app.schemas.menu import (
    ScanMenuRequest,
    ScanMenuResponse,
    MenuItemSchema,
    RestaurantSchema,
)
from app.schemas.vibe import VibeRequest, VibeResponse, VibeContext
from app.schemas.recommendations import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendationItemSchema,
)
from app.schemas.confirm import ConfirmRequest, ConfirmResponse
from app.schemas.feedback import FeedbackRequest, FeedbackResponse

router = APIRouter()


def get_session_or_404(session_id: str):
    """Helper to get session or raise 404."""
    session = db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail={
            "error": {
                "code": "not_found",
                "message": "Session not found"
            }
        })
    if session.status == SessionStatus.EXPIRED:
        raise HTTPException(status_code=410, detail={
            "error": {
                "code": "session_expired",
                "message": "Session has expired"
            }
        })
    return session


@router.post("", response_model=SessionsResponse, status_code=201)
async def create_session(request: SessionsRequest):
    """
    Create a new session for the recommendation flow.

    - **device_id**: Optional UUID for returning users to retrieve preferences
    - **locale**: ISO locale (e.g., en-US)
    - **timezone**: IANA timezone (e.g., America/Los_Angeles)
    - **app_version**: Client app version (semver format)
    """
    session = db.create_session(
        device_id=str(request.device_id) if request.device_id else None,
        locale=request.locale,
        timezone=request.timezone,
        app_version=request.app_version,
    )

    # Build preferences response if available
    preferences = None
    if session.preferences:
        preferences = SessionPreferences(
            allergies=session.preferences.get("allergies", []),
            max_spice=session.preferences.get("max_spice"),
            dietary_restrictions=session.preferences.get("dietary_restrictions", []),
        )

    return SessionsResponse(
        session_id=UUID(session.id),
        created_at=session.created_at,
        expires_at=session.expires_at,
        preferences=preferences,
    )


@router.post("/{session_id}/scan-menu", response_model=ScanMenuResponse)
async def scan_menu(
    session_id: str = Path(description="Session ID"),
    request: ScanMenuRequest = None,
):
    """
    Scan a menu image using OCR.

    In MVP mode, returns fake Thai restaurant menu items.
    Image data is ephemeral and not stored (privacy-first).
    """
    session = get_session_or_404(session_id)

    # Process menu image (fake OCR in MVP)
    menu_data = await ocr_service.process_menu_image(
        session_id=session_id,
        image_data=None,  # Ignored in fake implementation
    )

    # Update session
    session.menu_data = menu_data
    session.current_step = SessionStep.MENU
    db.update_session(session)

    # Build response
    items = [
        MenuItemSchema(
            id=item.id,
            name=item.name,
            description=item.description,
            price=item.price,
            currency=item.currency,
            category=item.category,
            tags=item.tags,
            allergens=item.allergens,
            spice_level=item.spice_level,
            is_vegetarian=item.is_vegetarian,
            is_vegan=item.is_vegan,
            confidence=item.confidence,
        )
        for item in menu_data.items
    ]

    restaurant = None
    if menu_data.restaurant:
        restaurant = RestaurantSchema(
            name=menu_data.restaurant.name,
            cuisine_type=menu_data.restaurant.cuisine_type,
            address=menu_data.restaurant.address,
        )

    return ScanMenuResponse(
        menu_id=menu_data.id,
        restaurant=restaurant,
        items=items,
        item_count=len(items),
        extraction_method=menu_data.extraction_method.value,
        confidence=menu_data.confidence,
        extracted_at=menu_data.extracted_at,
        warnings=menu_data.warnings,
    )


@router.post("/{session_id}/vibes", response_model=VibeResponse)
async def submit_vibes(
    request: VibeRequest,
    session_id: str = Path(description="Session ID"),
):
    """
    Submit vibe/mood selection for recommendations.

    - **menu_id**: ID of the scanned menu
    - **vibes**: 1-3 vibes from: comfort, adventure, light, quick, sharing, budget, healthy, indulgent
    - **party_size**: Number of diners (1-20)
    - **constraints**: Optional dietary restrictions and allergies
    """
    session = get_session_or_404(session_id)

    # Validate session has menu data
    if not session.menu_data:
        raise HTTPException(status_code=400, detail={
            "error": {
                "code": "invalid_request",
                "message": "Menu must be scanned before submitting vibes"
            }
        })

    # Validate menu_id matches
    if session.menu_data.id != request.menu_id:
        raise HTTPException(status_code=400, detail={
            "error": {
                "code": "invalid_request",
                "message": "Menu ID does not match session's menu"
            }
        })

    # Create vibe data
    vibe_data = VibeData(
        id=str(uuid4()),
        session_id=session_id,
        menu_id=request.menu_id,
        vibes=[VibeType(v) for v in request.vibes],
        party_size=request.party_size,
        budget_per_person=request.budget_per_person,
        dietary_restrictions=request.constraints.dietary_restrictions if request.constraints else [],
        allergies=request.constraints.allergies if request.constraints else [],
        max_spice=request.constraints.max_spice if request.constraints else None,
        occasion=request.occasion,
        created_at=datetime.utcnow(),
    )

    # Update session
    session.vibe_data = vibe_data
    session.current_step = SessionStep.VIBES
    db.update_session(session)

    return VibeResponse(
        vibe_id=vibe_data.id,
        menu_id=request.menu_id,
        context=VibeContext(
            vibes=request.vibes,
            party_size=request.party_size,
            has_restrictions=bool(request.constraints and (
                request.constraints.dietary_restrictions or
                request.constraints.allergies
            )),
            occasion=request.occasion,
        ),
        created_at=vibe_data.created_at,
    )


@router.post("/{session_id}/recommendations", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest,
    session_id: str = Path(description="Session ID"),
):
    """
    Get AI-powered dish recommendations based on vibes.

    - **vibe_id**: ID of the vibe selection
    - **menu_id**: ID of the menu
    - **count**: Number of recommendations (1-5, default 3)
    """
    session = get_session_or_404(session_id)

    # Validate session state
    if not session.menu_data:
        raise HTTPException(status_code=400, detail={
            "error": {
                "code": "invalid_request",
                "message": "Menu must be scanned first"
            }
        })

    if not session.vibe_data:
        raise HTTPException(status_code=400, detail={
            "error": {
                "code": "invalid_request",
                "message": "Vibes must be submitted first"
            }
        })

    # Validate IDs match
    if session.menu_data.id != request.menu_id:
        raise HTTPException(status_code=400, detail={
            "error": {
                "code": "invalid_request",
                "message": "Menu ID does not match session's menu"
            }
        })

    if session.vibe_data.id != request.vibe_id:
        raise HTTPException(status_code=400, detail={
            "error": {
                "code": "invalid_request",
                "message": "Vibe ID does not match session's vibes"
            }
        })

    # Generate recommendations (fake LLM in MVP)
    recommendation_set = await llm_service.generate_recommendations(
        menu_data=session.menu_data,
        vibe_data=session.vibe_data,
    )

    # Limit to requested count
    recommendation_set.recommendations = recommendation_set.recommendations[:request.count]

    # Update session
    session.recommendation_set = recommendation_set
    session.current_step = SessionStep.RECOMMENDATIONS
    db.update_session(session)

    # Build response
    recommendations = [
        RecommendationItemSchema(
            id=rec.id,
            menu_item_id=rec.menu_item_id,
            name=rec.name,
            reason=rec.reason,
            match_score=rec.match_score,
            vibe_matches=rec.vibe_matches,
            price=rec.price,
            warnings=rec.warnings,
            tags=rec.tags,
        )
        for rec in recommendation_set.recommendations
    ]

    return RecommendationResponse(
        recommendation_id=recommendation_set.id,
        vibe_id=request.vibe_id,
        menu_id=request.menu_id,
        recommendations=recommendations,
        reasoning_summary=recommendation_set.reasoning_summary,
        confidence=recommendation_set.confidence,
        generated_at=recommendation_set.generated_at,
        model_version=recommendation_set.model_version,
    )


@router.post("/{session_id}/confirm", response_model=ConfirmResponse)
async def confirm_dishes(
    request: ConfirmRequest,
    session_id: str = Path(description="Session ID"),
):
    """
    Confirm dish selection.

    - **recommendation_id**: ID of the recommendation set
    - **picked_dishes**: List of recommendation IDs the user selected
    - **skipped_dishes**: List of recommendation IDs the user skipped
    """
    session = get_session_or_404(session_id)

    # Validate session state
    if not session.recommendation_set:
        raise HTTPException(status_code=400, detail={
            "error": {
                "code": "invalid_request",
                "message": "Recommendations must be generated first"
            }
        })

    if session.recommendation_set.id != request.recommendation_id:
        raise HTTPException(status_code=400, detail={
            "error": {
                "code": "invalid_request",
                "message": "Recommendation ID does not match session's recommendations"
            }
        })

    # Create confirmation
    confirmation = Confirmation(
        id=str(uuid4()),
        session_id=session_id,
        recommendation_id=request.recommendation_id,
        picked_dishes=request.picked_dishes,
        skipped_dishes=request.skipped_dishes,
        confirmed_at=datetime.utcnow(),
    )

    # Update session
    session.confirmation = confirmation
    session.current_step = SessionStep.CONFIRMED
    db.update_session(session)

    return ConfirmResponse(
        confirmation_id=confirmation.id,
        session_id=session_id,
        recommendation_id=request.recommendation_id,
        picked_count=len(request.picked_dishes),
        skipped_count=len(request.skipped_dishes),
        confirmed_at=confirmation.confirmed_at,
    )


@router.post("/{session_id}/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    request: FeedbackRequest,
    session_id: str = Path(description="Session ID"),
):
    """
    Submit feedback on recommendations.

    - **confirmation_id**: ID of the confirmation
    - **rating**: 1-5 star rating
    - **comment**: Optional text feedback
    - **would_recommend**: Optional boolean for NPS-style question
    """
    session = get_session_or_404(session_id)

    # Validate session state
    if not session.confirmation:
        raise HTTPException(status_code=400, detail={
            "error": {
                "code": "invalid_request",
                "message": "Dishes must be confirmed first"
            }
        })

    if session.confirmation.id != request.confirmation_id:
        raise HTTPException(status_code=400, detail={
            "error": {
                "code": "invalid_request",
                "message": "Confirmation ID does not match session's confirmation"
            }
        })

    # Submit feedback
    feedback = await feedback_service.submit_feedback(
        session=session,
        confirmation_id=request.confirmation_id,
        rating=request.rating,
        comment=request.comment,
        would_recommend=request.would_recommend,
    )

    return FeedbackResponse(
        feedback_id=feedback.id,
        session_id=session_id,
        confirmation_id=request.confirmation_id,
        rating=feedback.rating,
        submitted_at=feedback.submitted_at,
    )


@router.get("/{session_id}", response_model=GetSessionResponse)
async def get_session(
    session_id: str = Path(description="Session ID"),
):
    """
    Get current session state.

    Useful for resuming sessions or debugging the flow.
    """
    session = db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail={
            "error": {
                "code": "not_found",
                "message": "Session not found"
            }
        })

    # Build response with optional summaries based on progress
    menu = None
    if session.menu_data:
        menu = MenuSummary(
            menu_id=session.menu_data.id,
            item_count=len(session.menu_data.items),
            restaurant_name=session.menu_data.restaurant.name if session.menu_data.restaurant else None,
            extracted_at=session.menu_data.extracted_at,
        )

    vibes = None
    if session.vibe_data:
        vibes = VibeSummary(
            vibe_id=session.vibe_data.id,
            vibes=[v.value if hasattr(v, 'value') else v for v in session.vibe_data.vibes],
            party_size=session.vibe_data.party_size,
            created_at=session.vibe_data.created_at,
        )

    recommendations = None
    if session.recommendation_set:
        recommendations = RecommendationSummary(
            recommendation_id=session.recommendation_set.id,
            count=len(session.recommendation_set.recommendations),
            generated_at=session.recommendation_set.generated_at,
        )

    confirmation = None
    if session.confirmation:
        confirmation = ConfirmationSummary(
            confirmation_id=session.confirmation.id,
            picked_count=len(session.confirmation.picked_dishes),
            confirmed_at=session.confirmation.confirmed_at,
        )

    feedback = None
    if session.feedback:
        feedback = FeedbackSummary(
            feedback_id=session.feedback.id,
            rating=session.feedback.rating,
            submitted_at=session.feedback.submitted_at,
        )

    return GetSessionResponse(
        session_id=session.id,
        status=session.status.value,
        current_step=session.current_step.value,
        created_at=session.created_at,
        expires_at=session.expires_at,
        menu=menu,
        vibes=vibes,
        recommendations=recommendations,
        confirmation=confirmation,
        feedback=feedback,
    )
