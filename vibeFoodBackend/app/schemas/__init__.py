"""
Schemas package for Vibe-Food application.
"""
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
