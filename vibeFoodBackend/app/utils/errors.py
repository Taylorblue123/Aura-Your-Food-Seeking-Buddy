"""
Custom exceptions for Vibe-Food application.
Standard error codes: invalid_request, validation_failed, not_found,
session_expired, rate_limited, ocr_failed, llm_failed, timeout, internal_error
"""
from typing import Optional, Dict, Any


class AppError(Exception):
    """Base exception for application errors."""
    error_code: str = "internal_error"
    status_code: int = 500
    message: str = "An internal error occurred"

    def __init__(
        self,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message or self.message
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to API response format."""
        result = {
            "error": {
                "code": self.error_code,
                "message": self.message,
            }
        }
        if self.details:
            result["error"]["details"] = self.details
        return result


class InvalidRequestError(AppError):
    """Invalid request format or parameters."""
    error_code = "invalid_request"
    status_code = 400
    message = "Invalid request"


class ValidationError(AppError):
    """Request validation failed."""
    error_code = "validation_failed"
    status_code = 422
    message = "Validation failed"


class NotFoundError(AppError):
    """Requested resource not found."""
    error_code = "not_found"
    status_code = 404
    message = "Resource not found"


class SessionExpiredError(AppError):
    """Session has expired."""
    error_code = "session_expired"
    status_code = 410
    message = "Session has expired"


class SessionNotFoundError(NotFoundError):
    """Session not found."""
    message = "Session not found"


class RateLimitedError(AppError):
    """Rate limit exceeded."""
    error_code = "rate_limited"
    status_code = 429
    message = "Rate limit exceeded"


class OCRFailedError(AppError):
    """OCR processing failed."""
    error_code = "ocr_failed"
    status_code = 500
    message = "Failed to process menu image"


class LLMFailedError(AppError):
    """LLM processing failed."""
    error_code = "llm_failed"
    status_code = 500
    message = "Failed to generate recommendations"


class TimeoutError(AppError):
    """Operation timed out."""
    error_code = "timeout"
    status_code = 504
    message = "Operation timed out"


class InvalidSessionStepError(InvalidRequestError):
    """Operation not allowed at current session step."""
    message = "Operation not allowed at current session step"
