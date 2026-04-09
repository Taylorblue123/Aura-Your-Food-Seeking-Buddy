"""
Test fixtures for Vibe-Food integration tests.
Uses in-memory SQLite and mocks external services (OpenAI).
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.main import app


# In-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    """Create tables before each test, drop after."""
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=test_engine)
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def registered_device(client):
    """Register a device and return its device_id."""
    device_id = "test-device-001"
    res = client.post("/api/v1/register", json={
        "device_id": device_id,
        "preference": "no_restriction",
    })
    assert res.status_code == 200
    assert res.json()["is_success"] is True
    return device_id


# --- Mock OpenAI responses ---

MOCK_OCR_RESPONSE = {
    "restaurant": {"name": "Test Bistro", "cuisine_type": "American"},
    "items": [
        {"name": "Classic Burger", "description": "Beef patty with lettuce and tomato", "price": 12.99, "currency": "USD", "category": "Mains", "tags": ["popular"], "allergens": ["gluten"], "spice_level": 0, "is_vegetarian": False, "is_vegan": False},
        {"name": "Caesar Salad", "description": "Romaine lettuce with caesar dressing", "price": 9.99, "currency": "USD", "category": "Salads", "tags": ["healthy"], "allergens": ["dairy", "gluten"], "spice_level": 0, "is_vegetarian": True, "is_vegan": False},
        {"name": "Fish Tacos", "description": "Grilled fish with slaw and lime crema", "price": 14.99, "currency": "USD", "category": "Mains", "tags": ["spicy"], "allergens": ["fish", "gluten"], "spice_level": 2, "is_vegetarian": False, "is_vegan": False},
        {"name": "Chocolate Cake", "description": "Rich chocolate layer cake", "price": 7.99, "currency": "USD", "category": "Desserts", "tags": ["sweet"], "allergens": ["dairy", "gluten", "eggs"], "spice_level": 0, "is_vegetarian": True, "is_vegan": False},
    ],
    "confidence": 0.92,
    "warnings": [],
}

MOCK_REC_RESPONSE = {
    "brief_summary": "Here are some comforting dishes to warm your soul.",
    "recommendations": [
        {"dish_name": "Classic Burger", "reasoning": "A hearty comfort classic", "story": "Nothing beats a juicy burger on a comfort day", "warnings": ["Contains gluten"], "price": "12.99", "emoji": "🍔"},
        {"dish_name": "Chocolate Cake", "reasoning": "Sweet comfort in every bite", "story": "Indulge in rich chocolate layers", "warnings": None, "price": "7.99", "emoji": "🍫"},
        {"dish_name": "Caesar Salad", "reasoning": "A familiar favorite", "story": "Crisp and satisfying", "warnings": ["Contains dairy"], "price": "9.99", "emoji": "🥗"},
    ],
}


def _make_mock_openai_response(content_dict):
    """Create a mock OpenAI ChatCompletion response."""
    import json
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = json.dumps(content_dict)
    mock_response.usage = MagicMock()
    mock_response.usage.prompt_tokens = 100
    mock_response.usage.completion_tokens = 50
    return mock_response


@pytest.fixture
def mock_openai_ocr():
    """Mock OpenAI Vision API for OCR."""
    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(
        return_value=_make_mock_openai_response(MOCK_OCR_RESPONSE)
    )
    with patch("app.services.ocr_service._extract_with_openai") as mock_extract:
        # Directly mock the internal function to return parsed dict
        import asyncio
        mock_extract.return_value = MOCK_OCR_RESPONSE
        yield mock_extract


@pytest.fixture
def mock_openai_rec():
    """Mock OpenAI API for recommendations."""
    with patch("app.services.llm_service._call_openai") as mock_call:
        mock_call.return_value = MOCK_REC_RESPONSE
        yield mock_call


@pytest.fixture
def mock_openai_key():
    """Ensure OPENAI_API_KEY is set so services don't use fallback."""
    with patch("app.services.ocr_service.settings") as mock_ocr_settings, \
         patch("app.services.llm_service.settings") as mock_llm_settings:
        mock_ocr_settings.OPENAI_API_KEY = "sk-test-fake-key"
        mock_llm_settings.OPENAI_API_KEY = "sk-test-fake-key"
        yield
