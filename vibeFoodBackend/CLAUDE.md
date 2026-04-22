# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Aura (codename: Gusto) is a FastAPI backend + vanilla JS frontend for a food recommendation MVP. Users scan restaurant menus (OCR), select mood "vibes", and receive AI-powered dish recommendations in a 90-second decision flow. The companion character "Gusto" (an animated orb) guides users through the experience.

**For full project context, read `../onboarding/ONBOARDING.md` first.**

## Tech Stack

- **Framework**: FastAPI with async/await
- **Validation**: Pydantic v2 (`pydantic_settings`)
- **Database**: SQLite (MVP), single table `user_profiles`, migration to PostgreSQL planned
- **External APIs**: OpenAI Vision API (OCR via gpt-4o-mini), OpenAI GPT-4o (recommendations), OpenAI Whisper (voice transcription)
- **Frontend**: Single vanilla HTML/CSS/JS file at `static/index.html` (2476 lines)
- **Server**: uvicorn
- **Deployment**: Render.com (`../render.yaml`)

## Common Commands

```bash
# Run development server
uvicorn app.main:app --reload

# Run with specific host/port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest tests/ -v
```

## Configuration

Settings loaded from `.env` file via `pydantic_settings`. Required variables:
- `SECRET_KEY` - Application secret
- `DATABASE_URL` - SQLite/PostgreSQL connection string (default: `sqlite:///./vibe_food.db`)

Optional:
- `OPENAI_API_KEY` - Enables real OCR, LLM recommendations, and voice transcription. Without it, app uses hardcoded fake data (Thai restaurant fallback).

## Architecture

```
vibeFoodBackend/
├── app/
│   ├── main.py              # FastAPI app init, CORS (allow all), static file mount, router mount
│   ├── api/v1/
│   │   ├── __init__.py      # Router aggregation (api_router)
│   │   └── endpoints/       # 6 endpoint modules + healthz
│   ├── core/config.py       # Pydantic Settings (loads .env)
│   ├── schemas/             # Pydantic request/response models
│   ├── models/              # SQLAlchemy ORM (UserProfile — single table)
│   ├── services/
│   │   ├── ocr_service.py   # OpenAI Vision API menu extraction + fake fallback
│   │   ├── llm_service.py   # GPT-4o recommendations + restaurant intros + fallback
│   │   ├── openai_client.py # Shared async OpenAI client singleton
│   │   └── feedback.py      # Hardcoded feedback generation (not LLM-based)
│   └── utils/
│       └── errors.py        # Custom exception hierarchy (AppError + 9 subtypes)
├── static/
│   └── index.html           # THE ENTIRE FRONTEND — 6 screens, Gusto Orb, card swipe, voice, i18n
├── tests/
│   ├── conftest.py          # Fixtures: in-memory SQLite, TestClient, mock OpenAI responses
│   └── test_pipeline.py     # 70+ test cases covering all endpoints + full pipeline
├── requirements.txt
├── CLAUDE.md                # You are here
├── BUILD_LOG.md
├── MVP Data Flow.md         # Data flow specification for the 5 core endpoints
└── vibe_food.db             # SQLite database file (auto-created on first run)
```

## API Endpoints

Base path: `/api/v1`. Device-based identification (no auth).

| # | Method | Path | Purpose |
|---|--------|------|---------|
| 1 | POST | `/check-in` | Check if device is registered |
| 2 | POST | `/register` | Register with device ID + dietary preferences (List[str]) |
| 3 | POST | `/scan` | Upload menu photo (base64) → OCR → extract items + restaurant intro |
| 4 | POST | `/recommendation` | Get AI dish picks based on vibe + menu + preferences |
| 5 | POST | `/feedback` | Submit picked/skipped dishes after card swiping |
| 6 | POST | `/transcribe` | Voice audio → text via Whisper (multipart upload) |
| 7 | GET | `/healthz` | Health check |

**User flow**: check-in → register (if new) → scan → recommendation → feedback

## Frontend (static/index.html)

Single-file app with 6 screens. Key patterns:
- **State**: Global JS variables (deviceId, selectedPrefs, recommendations, etc.)
- **Device ID**: `crypto.randomUUID()` stored in `localStorage`
- **API calls**: `api(path, body)` helper function (POST + JSON)
- **Screen transitions**: `showScreen(id, orbMode)` with fade animations
- **i18n**: `t(key)` function, `TRANSLATIONS` object (en + zh), auto-detected from menu language
- **Gusto Orb**: CSS animated blob, two modes (center=large, top=small dot)
- **Card swipe**: Touch-based drag with threshold detection (>100px = pick/skip)
- **Voice**: MediaRecorder + audio visualization, sends to /transcribe endpoint

## Key Design Decisions

- No user authentication for MVP (Device ID for user identification)
- Menu photo data is ephemeral (deleted after OCR, privacy-first)
- Warnings array pattern for allergen safety
- SQLite sufficient for 10-100 test users
- Preferences stored as CSV string in single column (simple but not normalized)
- All complex data (menu, recommendations, feedback) stored as JSON columns
- Frontend and backend in same service (static files served by FastAPI)
- Fallback data when no API key: fake Thai menu + hardcoded recommendations per vibe

## Vibe Types

Eight mood selections: `comfort`, `adventure`, `light`, `quick`, `sharing`, `budget`, `healthy`, `indulgent`

Plus `voice` mode (free-form text from Whisper transcription).

Adaptive dish count: 1-2 for solo/light/quick, 3-4 standard, 4-6 for groups/sharing.

## Error Handling

Custom exception hierarchy in `utils/errors.py`:
- `AppError` (base, 500) → `InvalidRequestError` (400), `ValidationError` (422), `NotFoundError` (404), `SessionExpiredError` (410), `RateLimitedError` (429), `OCRFailedError` (500), `LLMFailedError` (500), `TimeoutError` (504)

Standard error codes: `invalid_request`, `validation_failed`, `not_found`, `session_expired`, `rate_limited`, `ocr_failed`, `llm_failed`, `timeout`, `internal_error`

## Design Language

The frontend uses a warm companion aesthetic (not generic UI):
- **Colors**: Terracotta (#C4654A), Sage (#8BA888), Warm cream (#FFF8F0)
- **Fonts**: Fraunces (serif italic for headings), Nunito (sans for body)
- **Tone**: First-person, friend-like ("Let me find something special for you")
- **Character**: Gusto Orb — peach gradient, breathing animation, thinking state

## What's NOT Implemented Yet

- Persistent user memory / learning across sessions
- Rate limiting middleware
- Real health checks (currently hardcoded "healthy")
- PostgreSQL migration
- Authentication / account system
- Analytics pipeline
- Next.js / PWA frontend (Phase 2 vision in `../docs/`)

## Onboarding

New to this project? Start at `../onboarding/` — it has everything you need to get up to speed.