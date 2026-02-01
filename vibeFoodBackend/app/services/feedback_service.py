"""
Feedback service for processing and storing user feedback.
"""
from datetime import datetime
from typing import Optional
from uuid import uuid4

from app.models.domain import Feedback, Session
from app.services.fake_database import db


async def submit_feedback(
    session: Session,
    confirmation_id: str,
    rating: int,
    comment: Optional[str] = None,
    would_recommend: Optional[bool] = None,
) -> Feedback:
    """
    Process and store user feedback.

    Args:
        session: The current session
        confirmation_id: ID of the confirmation this feedback is for
        rating: 1-5 star rating
        comment: Optional text comment
        would_recommend: Optional boolean for NPS-style question

    Returns:
        The created Feedback object
    """
    feedback = Feedback(
        id=str(uuid4()),
        session_id=session.id,
        confirmation_id=confirmation_id,
        rating=rating,
        comment=comment,
        would_recommend=would_recommend,
        submitted_at=datetime.utcnow(),
    )

    # Store feedback in session
    session.feedback = feedback
    db.update_session(session)

    # If device_id exists, update device preferences with feedback data
    # This could be used to improve future recommendations
    if session.device_id:
        preferences = db.get_device_preferences(session.device_id) or {}
        feedback_history = preferences.get("feedback_history", [])
        feedback_history.append({
            "rating": rating,
            "timestamp": feedback.submitted_at.isoformat(),
        })
        preferences["feedback_history"] = feedback_history[-10:]  # Keep last 10
        preferences["avg_rating"] = sum(f["rating"] for f in feedback_history) / len(feedback_history)
        db.save_device_preferences(session.device_id, preferences)

    return feedback
