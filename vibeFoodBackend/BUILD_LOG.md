# Vibe-Food Backend - Build Log

## Build Date
2026-02-04

## Overview
FastAPI backend for food recommendation MVP. Users scan restaurant menus (OCR), select mood "vibes", and receive AI-powered dish recommendations.

## Files Created

### Core Configuration
- `app/core/database.py` - SQLite database setup with SQLAlchemy

### Models
- `app/models/user_profile.py` - SQLAlchemy UserProfile model (DeviceID, Preference, CurrentMenu, CurrentVibe, CurrentRecommendations, CurrentFeedback)
- `app/models/enums.py` - Added PreferenceType enum

### Schemas (Pydantic v2)
- `app/schemas/check_in.py` - CheckInRequest/Response
- `app/schemas/register.py` - RegisterRequest/Response
- `app/schemas/scan.py` - ScanRequest/Response
- `app/schemas/mvp_recommendation.py` - MVPRecommendationRequest/Response, DishRecommendation
- `app/schemas/mvp_feedback.py` - MVPFeedbackRequest/Response

### API Endpoints
- `app/api/v1/endpoints/check_in.py` - POST /check-in
- `app/api/v1/endpoints/register.py` - POST /register
- `app/api/v1/endpoints/scan.py` - POST /scan
- `app/api/v1/endpoints/recommendation.py` - POST /recommendation
- `app/api/v1/endpoints/feedback.py` - POST /feedback

### Project Files
- `.env.example` - Example environment variables
- `.env` - Development environment configuration
- `requirements.txt` - Python dependencies

## Files Modified
- `app/main.py` - Added database initialization on startup
- `app/api/v1/__init__.py` - Added new MVP endpoint routers
- `app/models/__init__.py` - Export UserProfile and PreferenceType
- `app/schemas/__init__.py` - Export all MVP schemas

## Project Structure
```
vibeFoodBackend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app with lifespan
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py        # Router aggregation
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── check_in.py    # POST /check-in
│   │           ├── register.py    # POST /register
│   │           ├── scan.py        # POST /scan
│   │           ├── recommendation.py  # POST /recommendation
│   │           ├── feedback.py    # POST /feedback
│   │           ├── sessions.py    # Session-based endpoints
│   │           └── health.py      # Health check
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Pydantic Settings
│   │   └── database.py            # SQLAlchemy setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── enums.py               # VibeType, PreferenceType
│   │   ├── domain.py              # Domain dataclasses
│   │   └── user_profile.py        # SQLAlchemy UserProfile
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── check_in.py
│   │   ├── register.py
│   │   ├── scan.py
│   │   ├── mvp_recommendation.py
│   │   ├── mvp_feedback.py
│   │   └── ... (existing schemas)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ocr_service.py         # Fake OCR for MVP
│   │   ├── llm_service.py         # Fake LLM for MVP
│   │   ├── feedback_service.py
│   │   └── fake_database.py
│   └── utils/
│       ├── __init__.py
│       └── errors.py              # Custom exceptions
├── .env                           # Environment variables
├── .env.example                   # Example env file
├── requirements.txt               # Dependencies
├── CLAUDE.md                      # Project documentation
└── MVP Data Flow.md              # API specification
```

## MVP Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/check-in | POST | Check if device is registered |
| /api/v1/register | POST | Register new user with Device ID and preference |
| /api/v1/scan | POST | Upload menu photo (Base64) and run OCR |
| /api/v1/recommendation | POST | Get AI recommendations based on vibe selection |
| /api/v1/feedback | POST | Submit feedback after user filters recommendation list |

## How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings (defaults work for development)
```

### 3. Run Development Server
```bash
uvicorn app.main:app --reload
```

### 4. Access API
- API docs: http://localhost:8000/api/v1/openapi.json
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoint Flow

1. **Check-in**: App opens → POST /check-in with device_id → Returns if registered
2. **Register**: If not registered → POST /register with device_id + preference
3. **Scan**: Take menu photo → POST /scan with Base64 image → OCR extracts items
4. **Recommendation**: Select vibe → POST /recommendation → Get dish recommendations
5. **Feedback**: Filter dishes → POST /feedback with picked/skipped → Get summary

## Notes

- MVP uses fake OCR and LLM services (returns predefined Thai menu items)
- No authentication required (Device ID for user identification)
- SQLite database for MVP (10-100 test users)
- Menu image data is ephemeral (not stored)
