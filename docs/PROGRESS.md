# Aura (Gusto) — Development Progress Log

> Tracking all changes from the initial MVP state (`cb345ad`) to the current state (`e7a9767`).
> Session date: 2026-04-08 to 2026-04-09

---

## Starting Point — What We Had (`cb345ad`)

The app was a functional but bare-bones MVP: a FastAPI backend with 5 JSON endpoints and a single `index.html` frontend.

### Backend (5 endpoints)
| Endpoint | Function |
|----------|----------|
| `POST /check-in` | Check if device is registered |
| `POST /register` | Register with single dietary preference (string) |
| `POST /scan` | Upload menu image → OCR → returns `{is_success}` only |
| `POST /recommendation` | Send vibe string → get 3-5 dish recommendations |
| `POST /feedback` | Submit picked/skipped dishes → get English-only summary |

### Frontend (generic CRUD app)
- 5 screens: Welcome, Scan, Vibe, Recommendations, Done
- System fonts (`-apple-system, Roboto`), pure white `#FFFFFF` background, coral-red `#FF6B6B` primary
- No animations, no transitions, instant screen swaps
- Recommendations displayed as a **flat vertical list** with toggle buttons (pick/skip)
- No companion feel, no warmth — looked like a generic form app
- Single-select dietary preference (radio-button behavior)
- Fixed 8 vibe buttons in a 2x2 grid, all equal weight
- English only

---

## What Changed — Commit by Commit

### Commit 1: `06bd868` — Complete UI/UX Redesign
**The big rewrite.** Transformed every screen.

| Aspect | Before | After |
|--------|--------|-------|
| Color palette | Pure white `#FFF`, coral `#FF6B6B` | Warm cream `#FFF8F0`, terracotta `#C4654A` |
| Typography | System fonts | Fraunces (serif italic) + Nunito (sans) via Google Fonts |
| Companion element | None | Gusto Orb — peach gradient, breathing animation, thinking tremor |
| Screen transitions | Instant show/hide | Fade out (300ms) → fade in (400ms) |
| Preference buttons | Flat 2x2 grid | Circular bubble buttons, varied warm colors, spring-emerge animation |
| Vibe selection | 2x2 grid, all equal | Contextual presets: 3-4 suggested vibes based on time of day + "More vibes" toggle |
| Recommendations | Flat list with toggles | **Tinder-like card swipe**: drag right = pick, drag left = skip, with overlays, rotation, spring-back |
| Card design | Plain gray rectangles | Rounded cards (26px radius), warm shadows, emoji strip, Fraunces italic story text |
| Feedback | Alert + summary | Auto-submit after last swipe, animated done screen |
| Restaurant intro | None | **New screen** between scan and vibe: restaurant name, cuisine tag, LLM-generated intro, category pills |
| Language | English only | **Full i18n**: en + zh, app language follows menu language |
| Menu language detection | None | OCR now detects `menu_language`, all LLM outputs match that language |
| Scan response | `{is_success}` only | Extended: `restaurant_name`, `cuisine_type`, `menu_item_count`, `menu_categories`, `restaurant_intro`, `menu_language` |
| Feedback summaries | English hardcoded | Localized (en/zh) based on menu language |

**New backend additions:**
- `llm_service.generate_restaurant_intro()` — LLM-generated warm description of the restaurant
- OCR prompt detects `menu_language` field
- All 3 LLM prompts (OCR, intro, recommendations) include language-matching rules
- `json.dumps` with `ensure_ascii=False` so Chinese characters aren't escaped

### Commit 2: `033d15a` — Voice Recording Bug Fixes
Fixed 3 critical bugs in the press-and-hold voice recording:
1. **Async race condition**: `getUserMedia()` shows browser permission prompt — if user releases finger during prompt, recording would start with no way to stop. Fixed with `isPointerDown` flag.
2. **Empty audio chunks**: Changed `MediaRecorder.start()` to `start(250)` (timeslice) so data is collected periodically.
3. **Stream leaks**: Added `activeStream` tracking for cleanup in all error/cancel paths.

### Commit 3: `aaf36f8` — Mobile Touch Conflicts
Fixed two mobile web UX problems:
1. **Page scroll during card swipe**: Added `touch-action: none` on card-stack-area and recs screen, `overscroll-behavior: none` on html/body, `e.preventDefault()` on card pointerdown.
2. **Text selection on long-press record button**: Added `-webkit-user-select: none`, `-webkit-touch-callout: none` on voice area, record button, and mic SVG. Set `pointer-events: none` on SVG icon.

### Commit 4: `fcdb3f4` — Scan UX Improvements
1. **Camera + Gallery**: Removed `capture="environment"` so mobile browsers show both "Take Photo" and "Choose from Library".
2. **No dishes found**: When scan succeeds but `menu_item_count === 0`, shows friendly message "We didn't find any dishes" with retry button instead of proceeding to empty restaurant intro.

### Commit 5: `4822cfd` — Orb Overlap Fix (Global)
The Gusto Orb was in `center` mode (large, 90px, fixed at 38% from top) on the welcome screen and done screen, visually overlapping interactive content (preference bubbles, summary cards). Fixed by:
- Changing orb to `top` mode (tiny 18px dot) on ALL screens
- Removed spacer divs that compensated for centered orb
- Set default HTML class to `top` to prevent flash-of-centered-orb before JS loads

### Commit 6: `f5763de` — Adaptive Dish Count
Replaced fixed "recommend 3-5 dishes" rule with context-aware logic:
- Solo/light/quick mentions → 1-2 dishes
- Standard vibe → 3-4 dishes
- Group/sharing/many people → 4-6 dishes
- LLM infers from voice prompt context (e.g., "随便吃点" = 1-2, "人很多" = 5-6)

### Commit 7: `e7a9767` — Multi-Select Dietary Preferences
Changed onboarding from single-select to multi-select:
- Bubble buttons now toggle independently (tap to add, tap to remove)
- "No limits" acts as reset — clears all others
- Selecting any restriction auto-deselects "No limits"
- Backend: `preference` field changed from `str` to `List[str]`, stored as comma-separated string
- DB column widened from `String(50)` to `String(255)`

---

## Current State — Architecture Overview

### Backend (6 endpoints)
| Endpoint | Changes from original |
|----------|----------------------|
| `POST /check-in` | Unchanged |
| `POST /register` | `preference` now accepts `List[str]` instead of single `str` |
| `POST /scan` | Returns 7 new fields: restaurant_name, cuisine_type, menu_item_count, menu_categories, restaurant_intro, menu_language |
| `POST /recommendation` | Accepts optional `voice_prompt`, supports `vibe_selection: "voice"`, adaptive dish count |
| `POST /feedback` | Localized summaries (en/zh) based on stored menu_language |
| **`POST /transcribe`** | **NEW** — accepts audio file upload, returns Whisper transcription |

### Frontend (6 screens)
1. **Welcome/Register** — Gusto greeting, multi-select dietary preference bubbles
2. **Scan Menu** — Camera/gallery upload, no-dishes-found retry flow
3. **Restaurant Intro** — **NEW** — Restaurant name, cuisine tag, LLM intro, category pills
4. **Pick Vibe** — Time-contextual suggested vibes + voice record button with live waveform
5. **Recommendations** — Tinder-like swipeable card stack with pick/skip overlays
6. **Done** — Localized summary with dish count and price estimate

### New Files Created
- `vibeFoodBackend/app/api/v1/endpoints/transcribe.py` — Whisper audio transcription
- `vibeFoodBackend/app/schemas/transcribe.py` — Transcription response schema
- `docs/DESIGN.md` — Visual design system
- `docs/PHILOSOPHY.md` — Product design philosophy
- `docs/SPEC.md` — Product specification
- `docs/PRD.md` — Product requirements document

---

## Alignment with PHILOSOPHY.md

| Philosophy Principle | Implementation Status |
|---------------------|----------------------|
| **Safe Corner** — App feels like warm shelter, not info tool | Warm cream palette, Fraunces typography, breathing orb — implemented |
| **One Thing, Not a List** — Show one recommendation at a time | Tinder card swipe shows one dish at a time — implemented |
| **Companion, Not Algorithm** — Feels like a friend's suggestion | Conversational copy ("Hey, I'm Gusto"), Fraunces italic stories, voice input — implemented |
| **Catch Me** — Zero cognitive load on open | Time-contextual vibe presets, voice "just tell me" option — implemented |
| **Adaptive Soul** — Personality grows with user | Not yet implemented (requires persistent memory across sessions) |
| **Adaptive Rhythm** — Fast when hungry, slow when lonely | Not yet implemented (requires context detection beyond time-of-day) |

## What's NOT Done Yet (Future Work)

1. **Persistent memory** — Gusto doesn't remember past sessions or dining experiences
2. **Adaptive personality** — Same tone for all users, no learning from interaction patterns
3. **Proactive notifications** — App only responds when opened, doesn't reach out
4. **Restaurant discovery** — Currently menu-scan only, no location-based restaurant suggestions
5. **Moment 2 (Go With You)** — No walking navigation, restaurant story, or "what to order" flow
6. **Moment 3 (Remember Us)** — No post-meal photo sharing, no emotional feedback beyond pick/skip
7. **Onboarding visual taste test** — No swipeable food photo preferences (described in SPEC.md)
8. **Orb conversation mode** — Orb is always in tiny-dot mode; the full center-orb dialogue flow from SPEC.md is not implemented
9. **Settings page** — No way to update dietary preferences after onboarding

---

## Stats

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Frontend lines | ~565 | ~2,476 | +1,911 |
| Backend files modified | 0 | 9 | +9 |
| New files created | 0 | 6 | +6 |
| API endpoints | 5 | 6 | +1 |
| Supported languages | 1 (en) | 2 (en, zh) | +1 |
| CSS animations | 0 | 8 keyframes | +8 |
| Total lines changed | — | +2,496 / -106 | net +2,390 |
| Commits in session | 0 | 7 | +7 |
