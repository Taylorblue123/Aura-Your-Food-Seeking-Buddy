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
- Device-based identification (no auth in MVP) - uses unique Device ID
- 5 endpoints defined in `MVP Data Flow.md`:
  1. `POST /check-in` - Check if device is registered (called on every app open)
  2. `POST /register` - Register new user with Device ID and preference selection
  3. `POST /scan` - Upload menu photo (Base64) and run OCR
  4. `POST /recommendation` - Get AI recommendations based on vibe selection
  5. `POST /feedback` - Submit feedback after user filters recommendation list

## Key Design Decisions (from MVP Data Flow.md)

- No user authentication for MVP (Device ID for user identification)
- Menu photo data is ephemeral (deleted after OCR, privacy-first)
- Warnings array pattern for allergen safety
- SQLite sufficient for 10-100 test users
- User profile stores: Device ID, preferences, current menu, vibe, recommendations, and feedback

## Vibe Types

Eight mood selections: `comfort`, `adventure`, `light`, `quick`, `sharing`, `budget`, `healthy`, `indulgent`

## Error Handling

Standard error codes: `invalid_request`, `validation_failed`, `not_found`, `session_expired`, `rate_limited`, `ocr_failed`, `llm_failed`, `timeout`, `internal_error`
