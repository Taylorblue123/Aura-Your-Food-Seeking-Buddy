# Backend API Specification - Aura Food MVP

## Version 1.0 - 7-Day Sprint Edition

---

## Work Log

- **What I read**: PRD_Complete.md (core hypothesis H1, MVP scope, technical requirements, data models)
- **What I decided**: Session-based architecture with minimal state, SQLite for MVP storage, no auth required, focus on recommendation flow
- **What I wrote**: Complete API contracts for 8 endpoints supporting the 90-second decision flow

## Decision Record

| Decision                     | Rationale                                                                        |
| ---------------------------- | -------------------------------------------------------------------------------- |
| Session-based (no auth)      | MVP focuses on testing H1 - auth adds complexity without value for 10 test users |
| SQLite for storage           | Sufficient for 10-100 users, no external dependencies, easy migration path       |
| Confidence scores everywhere | Builds trust, enables A/B testing recommendation thresholds                      |
| No real menu persistence     | OCR results are ephemeral - only feedback is stored                              |
| Warnings array pattern       | Safety-first for allergens, never assert without source                          |

---

## 1. MVP Contract Summary

### Core Flow (90 seconds)

1. **Create session** → session_id (device-based, no auth)
2. **Capture menu** → OCR text extraction OR manual text input
3. **Select vibes** → 1-3 mood bubbles + party size
4. **Get recommendations** → 3-5 dish cards with reasoning
5. **Confirm selection** → Mark dishes as picked/skipped
6. **Submit feedback** → Quick rating for learning

### Entry Methods Supported

- **Photo upload**: Base64 image → Google Vision OCR
- **Fallback text**: Manual text input if OCR fails
- **NO seeded menus in MVP**: Real capture only

---

## 2. Backend Responsibilities

### What Backend DOES (MVP)

- Generate session IDs (UUID v4)
- Process menu photos via Google Vision OCR
- Generate contextual vibe recommendations
- Call GPT-4 for dish recommendations with structured output
- Track analytics events for H1 validation

### What Backend DOES NOT (Post-MVP)

- User authentication/accounts
- Real restaurant API integration
- Store feedback for preference learning
- Payment processing
- Delivery coordination
- Social features
- Multi-language menu processing
- Redis caching
- Background jobs
- Push notifications

---

## 3. Data Contracts

### Core Entities

```typescript
// MenuItem - Extracted from menu
interface MenuItem {
  id: string; // UUID
  name: string; // "Pad Thai"
  description?: string; // "Stir-fried rice noodles..."
  price_range?: string; // "$12-14"
  tags?: string[]; // ["spicy", "contains-nuts"]
  source: "ocr" | "manual"; // How it was captured
  confidence?: number; // 0.0-1.0 for OCR
}

// VibeSelection - User's mood/context
interface VibeSelection {
  vibes: VibeType[]; // ["comfort", "budget"]
  party_size: number; // 1-8
  constraints?: {
    allergies?: string[]; // ["nuts", "dairy"]
    max_spice?: 1 | 2 | 3; // Tolerance level
    budget_per_person?: number; // Optional $ limit
  };
  context?: {
    time_of_day?: "breakfast" | "lunch" | "dinner" | "late_night";
    weather?: "hot" | "cold" | "rainy";
    occasion?: string; // "date", "business"
  };
}

// Recommendation - AI-generated suggestion
interface Recommendation {
  dish_id: string; // References MenuItem.id
  dish_name: string; // Display name
  reasoning: string; // "Mild and shareable..."
  story?: string; // Narrative hook
  confidence: number; // 0.0-1.0
  warnings?: string[]; // ["Contains dairy - verify with restaurant"]
  price_estimate?: string; // "$12-14"
  metadata?: Record<string, any>; // Future expansion
}

// Feedback - User response
interface Feedback {
  picked_dishes: string[]; // dish_ids selected
  skipped_dishes: string[]; // dish_ids rejected
  rating?: 1 | 2 | 3 | 4 | 5; // Overall satisfaction
  issues?: string[]; // ["too_spicy", "portion_small"]
  would_order_again?: boolean;
  time_to_decision_ms?: number; // Client-side measurement
}

// Enums
type VibeType =
  | "comfort" // 😌 Familiar, warm
  | "adventure" // 🔥 Try new things
  | "light" // 🥗 Not heavy
  | "quick" // ⚡ Fast eating
  | "sharing" // 👥 Group friendly
  | "budget" // 💰 Cost conscious
  | "healthy" // 💪 Nutritious
  | "indulgent"; // 🎉 Treat yourself
```

---

## 4. API Endpoints

### Base URL

```
https://api.aurafood.app/api/v1
```

### 4.1 POST /api/v1/sessions

**Purpose**: Create a new session for the user journey

**Request**:

```json
{
  "device_id": "string (UUID)", // Optional, for return users
  "locale": "en-US", // ISO locale
  "timezone": "America/Los_Angeles", // IANA timezone
  "app_version": "1.0.0" // Client version
}
```

**Response** (201 Created):

```json
{
  "session_id": "uuid-v4",
  "created_at": "2024-01-20T12:00:00Z",
  "expires_at": "2024-01-20T13:00:00Z", // 1 hour TTL
  "preferences": {
    // If device_id recognized
    "allergies": ["nuts"],
    "max_spice": 2
  }
}
```

**Errors**:

- 400: Invalid request format
- 429: Rate limit exceeded

---

### 4.2 POST /api/v1/sessions/{session_id}/scan-menu

**Purpose**: Upload menu photo or retrieving

**Request** (multipart/form-data OR JSON):

```json
{
  "image_base64"?: "string",         // Option 1: Photo
}
```

**Response** (200 OK):

```json
{
  "menu_id": "uuid-v4",
  "extraction_method": "ocr" | "selection",
  "confidence": 0.85,                 // Overall extraction confidence, if selection, 1.00
  "restaurant": {
    "name": "Thai House",
    "cuisine": "thai"
  },
  "menu_items": [
    {
      "id": "uuid",
      "name": "Pad Thai",
      "description": "Stir-fried rice noodles with tamarind sauce",
      "price_range": "$12-14",
      "tags": ["mild", "contains-peanuts"],
    },
    {
      "id": "uuid",
      "name": "Pad Thai",
      "description": "Stir-fried rice noodles with tamarind sauce",
      "price_range": "$12-14",
      "tags": ["mild", "contains-peanuts"],
    },
  ],
}
```

**Errors**:

- 400: No image or text provided
- 404: Session not found
- 413: Image too large (>5MB)
- 422: OCR failed completely
- 503: OCR service unavailable

---

### 4.3 POST /api/v1/sessions/{session_id}/vibes

**Purpose**: Submit vibe selection and constraints

**Request**:

```json
{
  "menu_id": "uuid",                  // From previous step
  "vibes": ["comfort", "budget"],     // 1-3 selections
  "party_size": 2,
  "constraints"?: {
    "allergies": ["nuts", "dairy"],
    "max_spice": 2,                   // 1=mild, 2=medium, 3=hot
    "budget_per_person": 20
  },
  "context"?: {
    "time_of_day": "lunch",
    "weather": "hot",
    "occasion": "casual"
  }
}
```

**Response** (200 OK):

```json
{
  "vibe_id": "uuid",
  "accepted": true
}
```

**Errors**:

- 404: Session or menu not found

---

### 4.4 POST /api/v1/sessions/{session_id}/recommendations

**Purpose**: Generate AI-powered dish recommendations

**Request**:

```json
{
  "vibe_id": "uuid",                  // From previous step
  "menu_id": "uuid",                  // From previous step
  "regenerate"?: false,               // Force new recommendations
  "exclude_dishes"?: ["uuid1"]        // Previously rejected
}
```

**Response** (200 OK):

```json
{
  "recommendation_id": "uuid",
  "recommendations": [
    {
      "dish_id": "uuid",
      "dish_name": "Pad Thai",
      "reasoning": "A mild, sweet noodle dish perfect for first-timers",
      "story": "The most popular Thai dish for a reason",
      "confidence": 0.89,
      "warnings"?: ["Contains peanuts - please verify with staff"],
      "price_estimate": "$12-14",
      "metadata": {
        "spice_level": 1,
        "portion_size": "medium"
      }
    }
  ],
  "session_context": {
    "total_recommendations": 4,
    "average_confidence": 0.85,
    "generation_time_ms": 1823
  },
  "fallback_reason"?: "Low confidence - showing popular items"
}
```

**Errors**:

- 404: Session or vibe not found
- 503: LLM service unavailable
- 504: LLM timeout (>5s)

---

### 4.5 POST /api/v1/sessions/{session_id}/confirm

**Purpose**: Confirm selected dishes (user's "I'll order these")

**Request**:

```json
{
  "recommendation_id": "uuid",
  "picked_dishes": ["dish_id_1", "dish_id_2"],
  "skipped_dishes": ["dish_id_3"],
  "time_to_decision_ms": 45230 // Client-side measured
}
```

**Response** (200 OK):

```json
{
  "confirmation_id": "uuid",
  "status": "confirmed",
  "picked_count": 2,
  "total_price_estimate": "$24-28",
  "celebration_type": "first_order" | "perfect_match" | "quick_decision" | null
}
```

**Errors**:

- 400: No dishes picked
- 404: Session or recommendation not found

---

### 4.6 POST /api/v1/sessions/{session_id}/feedback

**Purpose**: Collect post-order feedback for learning

**Request**:

```json
{
  "confirmation_id": "uuid",
  "rating"?: 4,                        // 1-5 stars
  "issues"?: ["too_spicy", "portion_small", "wrong_item"],
  "would_order_again"?: true,
  "comments"?: "Great suggestions!"
}
```

**Response** (200 OK):

```json
{
  "feedback_id": "uuid",
  "status": "recorded",
  "preference_updated": true
}
```

**Errors**:

- 404: Session or confirmation not found

---

### 4.7 GET /api/v1/sessions/{session_id}

**Purpose**: Resume session or debug state

**Response** (200 OK):

```json
{
  "session_id": "uuid",
  "status": "active" | "expired",
  "created_at": "2024-01-20T12:00:00Z",
  "current_step": "menu" | "vibes" | "recommendations" | "confirmed",
  "menu_id"?: "uuid",
  "vibe_id"?: "uuid",
  "recommendation_id"?: "uuid",
  "confirmation_id"?: "uuid"
}
```

**Errors**:

- 404: Session not found

---

### 4.8 GET /api/v1/healthz

**Purpose**: Health check for monitoring

**Response** (200 OK):

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-20T12:00:00Z",
  "services": {
    "database": "ok",
    "ocr": "ok",
    "llm": "ok"
  }
}
```

---

## 5. Error Model

### Standard Error Response

```json
{
  "error_code": "string",              // Enum, see below
  "message": "string",                 // User-safe message
  "detail": "string",                  // Developer details
  "field_errors"?: [                   // Validation errors
    {
      "field": "vibes",
      "message": "Maximum 3 vibes allowed"
    }
  ],
  "retryable": boolean,
  "request_id": "uuid"                 // For debugging
}
```

### Error Codes

| Code                | HTTP Status | Description                      | Retryable |
| ------------------- | ----------- | -------------------------------- | --------- |
| `invalid_request`   | 400         | Malformed request                | No        |
| `validation_failed` | 422         | Business logic validation failed | No        |
| `not_found`         | 404         | Resource doesn't exist           | No        |
| `session_expired`   | 410         | Session TTL exceeded             | No        |
| `rate_limited`      | 429         | Too many requests                | Yes       |
| `ocr_failed`        | 422         | Cannot extract menu              | No        |
| `llm_failed`        | 503         | LLM service error                | Yes       |
| `timeout`           | 504         | Operation timed out              | Yes       |
| `internal_error`    | 500         | Unexpected server error          | Yes       |

---

## 6. Persistence Strategy

### Storage: SQLite (MVP)

**Rationale**: No external dependencies, sufficient for 10-100 users, built-in with Python

### Tables

```sql
-- Core session tracking
CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  device_id TEXT,
  created_at TIMESTAMP,
  expires_at TIMESTAMP,
  locale TEXT,
  timezone TEXT
);

-- Feedback for learning
CREATE TABLE feedback (
  id TEXT PRIMARY KEY,
  session_id TEXT,
  confirmation_id TEXT,
  picked_dishes JSON,
  skipped_dishes JSON,
  rating INTEGER,
  issues JSON,
  created_at TIMESTAMP
);

-- Analytics events
CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT,
  event_name TEXT,
  properties JSON,
  timestamp TIMESTAMP
);
```

### What's Persisted vs Ephemeral

- **Persisted**: Sessions, feedback, events
- **Ephemeral**: Menu extractions, vibes, recommendations (stored in session memory)
- **Photos**: Discarded after OCR (privacy-first)

### Migration Path to Postgres

1. Same schema works in Postgres
2. Change connection string
3. Add connection pooling
4. Enable JSON column indexing

---

## 7. Frontend Integration Notes

### Screen-to-Endpoint Mapping

| Screen State            | Endpoint                            | Purpose         |
| ----------------------- | ----------------------------------- | --------------- |
| App launch              | POST /sessions                      | Initialize      |
| Camera capture          | POST /sessions/{id}/menu            | Extract menu    |
| Vibe selection          | POST /sessions/{id}/vibes           | Submit mood     |
| Loading recommendations | POST /sessions/{id}/recommendations | Get dishes      |
| Swipe cards done        | POST /sessions/{id}/confirm         | Mark picked     |
| Success screen          | POST /sessions/{id}/feedback        | Rate experience |

### Required Client State

```typescript
interface ClientState {
  session_id: string; // From POST /sessions
  menu_id?: string; // From POST /menu
  vibe_id?: string; // From POST /vibes
  recommendation_id?: string; // From POST /recommendations
  confirmation_id?: string; // From POST /confirm
}
```

### Retry Strategy

```typescript
const retryConfig = {
  maxAttempts: 3,
  backoff: [1000, 2000, 4000], // ms
  retryableCodes: ["llm_failed", "timeout", "internal_error"],
};
```

### Analytics Events (Frontend → Backend)

```typescript
// Aligned with H1 validation
const events = {
  'session_started': {},
  'menu_captured': { method: 'camera' | 'manual' },
  'ocr_completed': { confidence: number, item_count: number },
  'vibes_selected': { vibes: string[], party_size: number },
  'recommendations_shown': { count: number },
  'dish_swiped': { dish_id: string, direction: 'right' | 'left' },
  'order_confirmed': { picked_count: number, time_ms: number },  // PRIMARY H1 METRIC
  'feedback_submitted': { rating: number }
};
```

---

## 8. Security & Privacy (MVP)

### PII Policy

- **No PII collected**: No names, emails, phone numbers
- **Device ID only**: UUID for returning users
- **Location**: Not collected (use timezone only)

### Session Management

- **Identification**: UUID v4 (cryptographically random)
- **TTL**: 1 hour (sufficient for restaurant visit)
- **No cookies**: Session ID in memory/local storage

### Photo Handling

- **Immediate disposal**: Delete after OCR completes
- **No cloud storage**: Process in memory
- **Max size**: 5MB to prevent abuse

### Rate Limiting

```python
# Per device_id or IP
limits = {
  '/sessions': '10/hour',
  '/menu': '20/hour',
  '/recommendations': '30/hour',
  '*': '100/hour'  # Global
}
```

---

## 9. Implementation Checklist

### FastAPI Structure

```python
app/
├── main.py                 # FastAPI app + CORS
├── routers/
│   ├── sessions.py         # Session endpoints
│   ├── menu.py            # Menu processing
│   ├── recommendations.py # AI generation
│   └── health.py          # Health check
├── models/
│   ├── session.py         # Pydantic models
│   ├── menu.py
│   ├── vibe.py
│   └── recommendation.py
├── services/
│   ├── ocr_service.py     # Google Vision wrapper
│   ├── llm_service.py     # OpenAI wrapper
│   └── feedback_service.py # Learning system
├── db/
│   ├── database.py        # SQLite connection
│   └── models.py          # SQLAlchemy models
└── utils/
    ├── errors.py          # Exception classes
    └── validators.py      # Business validation
```

### Pydantic Models (v2)

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal
from datetime import datetime
from uuid import UUID

class CreateSessionRequest(BaseModel):
    device_id: Optional[UUID] = None
    locale: str = "en-US"
    timezone: str = "UTC"
    app_version: str = Field(..., regex="^\d+\.\d+\.\d+$")

class MenuUploadRequest(BaseModel):
    image_base64: Optional[str] = None
    menu_text: Optional[str] = None
    restaurant_name: Optional[str] = None
    cuisine_type: Optional[str] = None

    @validator('*', pre=True)
    def validate_input(cls, v, values):
        if not values.get('image_base64') and not values.get('menu_text'):
            raise ValueError('Either image_base64 or menu_text required')
        return v

class VibeSelectionRequest(BaseModel):
    menu_id: UUID
    vibes: List[Literal["comfort", "adventure", "light", "quick",
                        "sharing", "budget", "healthy", "indulgent"]]
    party_size: int = Field(ge=1, le=8)
    constraints: Optional[dict] = None
    context: Optional[dict] = None

    @validator('vibes')
    def validate_vibes(cls, v):
        if len(v) < 1 or len(v) > 3:
            raise ValueError('Select 1-3 vibes')
        return v
```

### Service Stubs

```python
# ocr_service.py
class OCRService:
    async def extract_menu(self, image_base64: str) -> dict:
        """Call Google Vision API, parse menu items"""
        pass

# llm_service.py
class LLMService:
    async def generate_recommendations(
        self,
        menu_items: list,
        vibes: list,
        constraints: dict
    ) -> list:
        """Call GPT-4 with structured output"""
        pass

# feedback_service.py
class FeedbackService:
    async def process_feedback(self, feedback: dict) -> None:
        """Store feedback, update preferences"""
        pass
```

### Smoke Tests

```python
# Happy path
async def test_full_flow():
    """Create session → Upload menu → Select vibes → Get recommendations → Confirm"""

# OCR failure
async def test_ocr_failure_recovery():
    """Upload bad image → Get error → Retry with text"""

# LLM timeout
async def test_llm_timeout_handling():
    """Mock slow LLM → Verify timeout → Check retry works"""
```

---

## Work Log Summary

- **What I read**: PRD sections on technical spec, data models, API contracts, LLM usage, storage strategy
- **What I decided**: Session-based flow with SQLite, minimal schema for MVP validation, safety-first approach for allergens
- **What I wrote**: 9 sections covering the complete backend contract with implementation-ready detail

## Decision Record Summary

- **No auth for MVP**: Faster to market, sufficient for 10 test users
- **SQLite over Postgres**: Zero dependencies, easy local development
- **Ephemeral menu data**: Privacy-first, reduce storage needs
- **Confidence scores everywhere**: Build trust through transparency
- **Forward-compatible schemas**: Optional fields and metadata objects for evolution
