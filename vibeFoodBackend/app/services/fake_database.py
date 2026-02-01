"""
Fake in-memory database for MVP testing.
Provides session and device preference storage.
"""
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from uuid import uuid4

from app.models.domain import Session
from app.models.enums import SessionStatus, SessionStep


class FakeDatabase:
    """In-memory storage for sessions and device preferences."""

    # Session TTL in hours
    SESSION_TTL_HOURS = 1

    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.device_preferences: Dict[str, Dict[str, Any]] = {}

    def create_session(
        self,
        device_id: Optional[str] = None,
        locale: str = "en-US",
        timezone: str = "UTC",
        app_version: str = "1.0.0",
    ) -> Session:
        """Create a new session."""
        session_id = str(uuid4())
        now = datetime.utcnow()
        expires_at = now + timedelta(hours=self.SESSION_TTL_HOURS)

        # Look up device preferences if device_id provided
        preferences = None
        if device_id and device_id in self.device_preferences:
            preferences = self.device_preferences[device_id]

        session = Session(
            id=session_id,
            device_id=device_id,
            locale=locale,
            timezone=timezone,
            app_version=app_version,
            status=SessionStatus.ACTIVE,
            current_step=SessionStep.CREATED,
            created_at=now,
            expires_at=expires_at,
            preferences=preferences,
        )

        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID, checking for expiration."""
        session = self.sessions.get(session_id)
        if not session:
            return None

        # Check expiration
        if session.expires_at and datetime.utcnow() > session.expires_at:
            session.status = SessionStatus.EXPIRED
            self.sessions[session_id] = session

        return session

    def update_session(self, session: Session) -> Session:
        """Update an existing session."""
        self.sessions[session.id] = session
        return session

    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def save_device_preferences(
        self,
        device_id: str,
        preferences: Dict[str, Any]
    ) -> None:
        """Save or update device preferences."""
        self.device_preferences[device_id] = preferences

    def get_device_preferences(
        self,
        device_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get preferences for a device."""
        return self.device_preferences.get(device_id)

    def clear_all(self) -> None:
        """Clear all data (for testing)."""
        self.sessions.clear()
        self.device_preferences.clear()


# Global singleton instance
db = FakeDatabase()
