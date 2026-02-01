# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Vibe-Food is a FastAPI backend for a food recommendation MVP. Users scan restaurant menus (OCR), select mood "vibes", and receive AI-powered dish recommendations in a 90-second decision flow.

## Tech Stack

- **Framework**: FastAPI with async/await
- **Validation**: Pydantic v2 (`pydantic_settings`)
- **Database**: SQLite (MVP), migration path to PostgreSQL planned
- **External APIs**: Google Vision API (OCR), OpenAI GPT-4 (recommendations)
- **Server**: uvicorn

## Common Commands

```bash
# Run development server
uvicorn app.main:app --reload

# Run with specific host/port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Configuration

Settings loaded from `.env` file via `pydantic_settings`. Required variables:
- `SECRET_KEY` - Application secret
- `DATABASE_URL` - SQLite/PostgreSQL connection string

Optional: `REDIS_URL`, SMTP settings for email

## Architecture

```
app/
├── main.py              # FastAPI app initialization, CORS, router mounting
├── api/v1/              # Versioned API routes
│   ├── __init__.py      # Router aggregation (api_router)
│   └── endpoints/       # Individual endpoint modules
├── core/config.py       # Pydantic Settings configuration
├── schemas/             # Pydantic request/response models
├── models/              # SQLAlchemy ORM models (planned)
├── services/            # Business logic (ocr_service, llm_service, feedback_service)
└── utils/               # Utilities (errors, validators)
```

## API Design

- Base path: `/api/v1`
- Session-based (no auth in MVP) - 1 hour TTL
- 8 endpoints defined in `API_SPEC_MVP.md`:
  1. `POST /sessions` - Create session
  2. `POST /sessions/{id}/scan-menu` - OCR menu photo
  3. `POST /sessions/{id}/vibes` - Submit vibe selection
  4. `POST /sessions/{id}/recommendations` - Get AI recommendations
  5. `POST /sessions/{id}/confirm` - Confirm dish selection
  6. `POST /sessions/{id}/feedback` - Submit feedback
  7. `GET /sessions/{id}` - Resume/debug session
  8. `GET /healthz` - Health check

## Key Design Decisions (from API_SPEC_MVP.md)

- No user authentication for MVP (device_id for returning users)
- Menu photo data is ephemeral (deleted after OCR, privacy-first)
- Confidence scores on all AI outputs for trust/transparency
- Warnings array pattern for allergen safety
- SQLite sufficient for 10-100 test users

## Vibe Types

Eight mood selections: `comfort`, `adventure`, `light`, `quick`, `sharing`, `budget`, `healthy`, `indulgent`

## Error Handling

Standard error codes: `invalid_request`, `validation_failed`, `not_found`, `session_expired`, `rate_limited`, `ocr_failed`, `llm_failed`, `timeout`, `internal_error`
