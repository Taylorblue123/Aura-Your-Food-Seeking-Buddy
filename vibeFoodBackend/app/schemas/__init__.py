"""
Schemas package for Vibe-Food application.
"""
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
    MenuItemSchema,
    RestaurantSchema,
    ScanMenuRequest,
    ScanMenuResponse,
)
from app.schemas.vibe import (
    VibeRequest,
    VibeResponse,
    VibeConstraints,
    VibeContext,
    ErrorResponse,
)
from app.schemas.recommendations import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendationItemSchema,
)
from app.schemas.confirm import (
    ConfirmRequest,
    ConfirmResponse,
)
from app.schemas.feedback import (
    FeedbackRequest,
    FeedbackResponse,
)
from app.schemas.health import (
    HealthResponse,
    ServiceStatus,
)
# MVP schemas
from app.schemas.check_in import (
    CheckInRequest,
    CheckInResponse,
)
from app.schemas.register import (
    RegisterRequest,
    RegisterResponse,
)
from app.schemas.scan import (
    ScanRequest,
    ScanResponse,
)
from app.schemas.mvp_recommendation import (
    MVPRecommendationRequest,
    MVPRecommendationResponse,
    MVPRecommendationData,
    DishRecommendation,
)
from app.schemas.mvp_feedback import (
    MVPFeedbackRequest,
    MVPFeedbackResponse,
)

__all__ = [
    # Sessions
    "SessionsRequest",
    "SessionsResponse",
    "SessionPreferences",
    "GetSessionResponse",
    "MenuSummary",
    "VibeSummary",
    "RecommendationSummary",
    "ConfirmationSummary",
    "FeedbackSummary",
    # Menu
    "MenuItemSchema",
    "RestaurantSchema",
    "ScanMenuRequest",
    "ScanMenuResponse",
    # Vibe
    "VibeRequest",
    "VibeResponse",
    "VibeConstraints",
    "VibeContext",
    "ErrorResponse",
    # Recommendations
    "RecommendationRequest",
    "RecommendationResponse",
    "RecommendationItemSchema",
    # Confirm
    "ConfirmRequest",
    "ConfirmResponse",
    # Feedback
    "FeedbackRequest",
    "FeedbackResponse",
    # Health
    "HealthResponse",
    "ServiceStatus",
    # MVP Check-in
    "CheckInRequest",
    "CheckInResponse",
    # MVP Register
    "RegisterRequest",
    "RegisterResponse",
    # MVP Scan
    "ScanRequest",
    "ScanResponse",
    # MVP Recommendation
    "MVPRecommendationRequest",
    "MVPRecommendationResponse",
    "MVPRecommendationData",
    "DishRecommendation",
    # MVP Feedback
    "MVPFeedbackRequest",
    "MVPFeedbackResponse",
]
