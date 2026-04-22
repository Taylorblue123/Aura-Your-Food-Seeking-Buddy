# Aura (Gusto) - Agent Onboarding Guide

> This document is written for a future AI agent joining this project with zero prior context.
> Read this FIRST before touching any code or docs.

---

## What Is This Project?

**Aura** (internally evolving to **Gusto**) is an AI-powered food recommendation app. It helps users — especially international students and young professionals — decide what to eat at restaurants in under 90 seconds.

**The core loop:**
1. User snaps a photo of a restaurant menu
2. User picks a mood ("vibe") like "comfort", "adventure", or "budget"
3. AI recommends 2-5 dishes with reasoning
4. User swipes right to accept, left to skip (Tinder-style)
5. Done — confident order in 90 seconds

**Why it matters:** People (especially non-native speakers) face decision paralysis at restaurants — 50+ unfamiliar items, language barriers, group pressure. Aura solves this with AI + mood-matching.

---

## Project Structure at a Glance

```
Aura-Your-Food-Seeking-Buddy/
│
├── vibeFoodBackend/              # <-- ALL working code lives here
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── api/v1/endpoints/    # 6 API endpoints
│   │   ├── core/config.py       # Settings (.env loading)
│   │   ├── models/              # SQLAlchemy ORM (UserProfile)
│   │   ├── schemas/             # Pydantic request/response models
│   │   ├── services/            # Business logic (OCR, LLM, feedback)
│   │   └── utils/               # Error classes, validators
│   ├── static/index.html        # <-- THE ENTIRE FRONTEND (single file, 2476 lines)
│   ├── tests/                   # pytest test suite (70+ cases)
│   ├── requirements.txt         # Python dependencies
│   ├── CLAUDE.md                # Agent instructions for backend
│   ├── BUILD_LOG.md             # Build history
│   ├── MVP Data Flow.md         # Data flow specification
│   └── vibe_food.db             # SQLite database (auto-created)
│
├── docs/                         # <-- Product vision & design docs (Phase 2 direction)
│   ├── PRD.md                   # Product Requirements (Gusto vision, Next.js + Supabase)
│   ├── SPEC.md                  # Functional spec (Orb hub model, 3 moments)
│   ├── DESIGN.md                # Visual design system (colors, fonts, components)
│   ├── PHILOSOPHY.md            # UX 3.0 design philosophy (Chinese + English)
│   └── PROGRESS.md              # Development changelog
│
├── [Root-level docs]             # <-- Original MVP specs (Phase 1, partially outdated)
│   ├── PRD_Complete.md          # Original MVP PRD (v3.0, Jan 2025)
│   ├── API_SPEC_MVP.md          # Original API spec (8 session-based endpoints)
│   ├── TECHNICAL_SPEC.md        # Original tech spec (React Native + Expo)
│   ├── UIUX_SPEC_FINAL.md      # Original UX spec (linear 5-screen flow)
│   ├── DESIGN_SYSTEM.md         # Original design system (Coral/Mint palette)
│   ├── IMPLEMENTATION_GUIDE.md  # 7-day sprint guide
│   └── README.md                # Project overview
│
├── render.yaml                   # Render.com deployment config
└── openspec/                     # OpenSpec (initialized but inactive)
```

---

## Two Versions of the Product Exist in Docs — Know the Difference

| Aspect | Phase 1 (Root docs) | Phase 2 (docs/ folder) |
|--------|---------------------|----------------------|
| **Name** | Aura Food | Gusto |
| **Frontend** | React Native + Expo (never built) | PWA with Next.js (planned) |
| **UX Model** | Linear 5-screen flow | Circular Orb Hub + 3 Moments |
| **Color Palette** | Coral #FF6B6B / Mint #A8E6CF | Terracotta #C4654A / Sage #8BA888 |
| **Data Source** | OCR only | LLM + Web Search (primary) + OCR (fallback) |
| **Vibes** | 8 fixed moods | Dynamic, LLM-generated per context |
| **Memory** | None (MVP) | Persistent companion memory |
| **Backend** | FastAPI + SQLite | FastAPI + Supabase (planned) |
| **AI Provider** | OpenAI GPT-4 | Claude API (planned) |

**What's actually built today** is a hybrid — the Phase 1 backend with Phase 2 aesthetics bolted on (terracotta/sage palette, Gusto Orb, warm companion tone, i18n). The frontend is a single vanilla HTML/JS file, not React Native or Next.js.

---

## Tech Stack (What's Actually Running)

| Layer | Technology | Notes |
|-------|-----------|-------|
| **Backend** | FastAPI (Python 3.8+) | Async, Pydantic v2 |
| **Database** | SQLite | Single file `vibe_food.db`, migration to PostgreSQL planned |
| **OCR** | OpenAI Vision API (gpt-4o-mini) | Extracts menu items from photos |
| **Recommendations** | OpenAI GPT-4o | Generates dish picks based on vibe + menu + preferences |
| **Voice** | OpenAI Whisper API | Transcribes voice input to text |
| **Frontend** | Vanilla HTML/CSS/JS | Single `static/index.html` file |
| **Deployment** | Render.com | `render.yaml` configured |
| **Auth** | None | Device ID via `localStorage` (UUID) |

---

## The 6 API Endpoints

All endpoints are under `/api/v1`. No authentication — Device ID is the user identifier.

| # | Method | Path | Purpose |
|---|--------|------|---------|
| 1 | POST | `/check-in` | Check if device is registered (called on every app open) |
| 2 | POST | `/register` | Register new user with device ID + dietary preferences |
| 3 | POST | `/scan` | Upload menu photo (base64), run OCR, extract items |
| 4 | POST | `/recommendation` | Get AI dish recommendations based on vibe selection |
| 5 | POST | `/feedback` | Submit picked/skipped dishes after card swiping |
| 6 | POST | `/transcribe` | Convert voice audio to text via Whisper |

Plus `GET /healthz` for health checks.

**The user flow through these endpoints:**
```
App opens → /check-in
  ├── Not registered → /register → /scan → /recommendation → /feedback
  └── Already registered → /scan → /recommendation → /feedback
                                     ↑ (optional: /transcribe for voice input)
```

---

## Frontend Architecture (static/index.html)

The entire frontend is ONE file with 6 screens:

| Screen | What It Does |
|--------|-------------|
| **1. Welcome/Register** | 8 dietary preference bubbles, register button |
| **2. Scan Menu** | Photo upload (camera or gallery), compress + base64 encode |
| **3. Restaurant Intro** | Restaurant name, cuisine, AI-generated warm intro, menu stats |
| **4. Pick Vibe** | Time-contextual vibe suggestions + voice recording button |
| **5. Recommendations** | Tinder-style card stack with swipe left/right |
| **6. Done** | Celebration, price estimate, AI summary, restart options |

**Key frontend features:**
- **Gusto Orb**: Animated peach gradient blob — breathes, thinks, transitions between screens
- **i18n**: English + Chinese, auto-detected from menu language
- **Voice input**: Hold-to-speak, real-time audio visualization, Whisper transcription
- **Card swipe**: Touch-based drag with rotation, green/red overlays, progress dots
- **Time-aware vibes**: Different suggestions for morning/lunch/dinner/late night

---

## Database Schema

Single table. Intentionally simple for MVP.

```sql
user_profiles
├── device_id VARCHAR(255) PRIMARY KEY    -- UUID from client localStorage
├── preference VARCHAR(255)               -- CSV string: "vegetarian,nut_free"
├── current_menu JSON                     -- Full OCR extraction result
├── current_vibe JSON                     -- Selected vibe + optional voice prompt
├── current_recommendations JSON          -- LLM recommendation output
├── current_feedback JSON                 -- Picked/skipped dishes + metadata
├── created_at DATETIME
└── updated_at DATETIME
```

---

## How to Run

```bash
# 1. Go to backend
cd vibeFoodBackend

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment (create .env file)
# Required:
#   SECRET_KEY=any-random-string
#   DATABASE_URL=sqlite:///./vibe_food.db
# Optional (enables real AI features):
#   OPENAI_API_KEY=sk-your-key-here

# 5. Run
uvicorn app.main:app --reload --port 8000

# 6. Access
# Frontend: http://localhost:8000
# API docs: http://localhost:8000/docs
```

**Without OPENAI_API_KEY**: App runs with hardcoded fake Thai restaurant menu and fallback recommendations. Good for UI/UX testing.

**With OPENAI_API_KEY**: Real OCR, real recommendations, real voice transcription.

## How to Test

```bash
cd vibeFoodBackend
pytest tests/ -v
```

70+ test cases covering all endpoints, edge cases, and the full user pipeline.

---

## Key Design Decisions (Why Things Are This Way)

| Decision | Why |
|----------|-----|
| **No auth, Device ID only** | MVP for 10-100 test users. Auth adds friction without validating the core hypothesis |
| **SQLite, not PostgreSQL** | Zero setup, single file, sufficient for MVP scale |
| **Single HTML file frontend** | Rapid iteration, no build step, no framework overhead |
| **Ephemeral menu data** | Privacy-first: photos deleted after OCR, only feedback persists |
| **Hardcoded feedback (not LLM)** | Feedback endpoint doesn't need AI — saves API costs |
| **8 fixed vibes** | Covers 95% of dining moods. Dynamic vibes are Phase 2 |
| **Swipe cards over list** | Lower cognitive load, faster decisions, aligns with 90-second promise |
| **Bilingual en/zh** | Primary users are international (Chinese + English speakers) |

---

## The 8 Vibes

| Vibe | Meaning | Example Use |
|------|---------|-------------|
| `comfort` | Familiar, warm, safe | "I want something I know I'll like" |
| `adventure` | Try something new, bold | "Surprise me with something exotic" |
| `light` | Not heavy, fresh | "Something that won't make me sleepy" |
| `quick` | Fast to eat | "I only have 15 minutes" |
| `sharing` | Group-friendly portions | "We're ordering for the table" |
| `budget` | Affordable | "Keeping it under $15" |
| `healthy` | Nutritious, clean | "Something with protein and veggies" |
| `indulgent` | Treat yourself | "It's been a long week, go big" |

Plus `voice` mode — user describes what they want in their own words.

---

## Important Files to Read First

If you need to understand the project quickly, read in this order:

1. **This file** (`ONBOARDING.md`) — You are here
2. **`vibeFoodBackend/CLAUDE.md`** — Agent-specific backend instructions
3. **`vibeFoodBackend/MVP Data Flow.md`** — The actual data flow spec
4. **`docs/PROGRESS.md`** — What changed and when
5. **`docs/PHILOSOPHY.md`** — The "why" behind design decisions (has Chinese text, that's intentional)

If you need to go deeper:
- **Backend code**: Start at `vibeFoodBackend/app/main.py`, then `api/v1/endpoints/`
- **Frontend**: `vibeFoodBackend/static/index.html` (it's one big file — search by function name)
- **Product vision**: `docs/PRD.md` + `docs/SPEC.md` (this is the Phase 2 direction)

---

## Known Gaps and Future Work

### Not Yet Built (from Phase 2 vision in docs/)
- Persistent user memory (Adaptive Soul)
- Orb Home hub model (circular navigation)
- Google Places API integration
- LLM + Web Search for restaurant discovery
- Adaptive rhythm (fast mode vs. comfort mode)
- Proactive push notifications
- Account system / social features
- Next.js PWA migration
- Supabase migration
- Claude API migration (currently OpenAI)

### Current Limitations
- Frontend is a single 2476-line HTML file (needs componentization for scale)
- Preferences stored as CSV string (should be relational)
- No persistent memory between sessions
- Health check reports all services "healthy" regardless of actual state
- CORS allows all origins (fine for MVP, not for production)
- No rate limiting implemented

---

## Glossary

| Term | Meaning |
|------|---------|
| **Vibe** | A mood/context tag that influences dish recommendations |
| **Orb / Gusto Orb** | The animated companion character (peach blob) that guides the user |
| **Moment 1/2/3** | Phase 2 concept: three emotional stages of a dining companion journey |
| **OCR** | Optical Character Recognition — extracting text from menu photos |
| **Device ID** | UUID stored in browser localStorage, used as user identifier |
| **Pick/Skip** | Swiping right (pick) or left (skip) on a recommended dish card |
| **Phase 1** | Current MVP: FastAPI + single HTML file + OpenAI |
| **Phase 2** | Future vision: Next.js PWA + Supabase + Claude API + Orb Hub model |
