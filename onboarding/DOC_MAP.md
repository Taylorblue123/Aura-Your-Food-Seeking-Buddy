# Aura Project - Document Map

> Quick reference for finding the right doc. All paths are relative to the project root (`Aura-Your-Food-Seeking-Buddy/`).

---

## Start Here (Onboarding)

| File | What It Tells You |
|------|-------------------|
| `onboarding/ONBOARDING.md` | Full project context for a new agent — structure, tech stack, endpoints, how to run, design decisions, glossary |
| `vibeFoodBackend/CLAUDE.md` | Agent-specific coding instructions — architecture, commands, patterns |

---

## Understanding the Current Code

| File | What It Tells You |
|------|-------------------|
| `vibeFoodBackend/MVP Data Flow.md` | The actual data flow spec for the 5 core endpoints (check-in, register, scan, recommendation, feedback) |
| `vibeFoodBackend/BUILD_LOG.md` | History of what was built and when |
| `docs/PROGRESS.md` | Detailed changelog of the April 2026 redesign session (7 commits, before/after comparisons) |

---

## Product Vision & Requirements

| File | Phase | What It Tells You |
|------|-------|-------------------|
| `PRD_Complete.md` | Phase 1 (MVP) | Original PRD v3.0 — hypothesis, target users, success metrics, 7-day sprint scope |
| `docs/PRD.md` | Phase 2 (Gusto) | Future vision — Orb Hub model, 3 Moments, LLM+Web Search, Supabase, Claude API |
| `PRD_ChangeLog.md` | Phase 1 | Why PRD went from v2.0 to v3.0 (removed unverified market claims) |

---

## Design & UX

| File | Phase | What It Tells You |
|------|-------|-------------------|
| `docs/PHILOSOPHY.md` | Phase 2 | The "why" — UX 3.0 companion design, 6 principles, 3 Moments concept (Chinese + English) |
| `docs/DESIGN.md` | Phase 2 | Visual system — terracotta/sage palette, Fraunces/Nunito fonts, Orb specs, component details |
| `docs/SPEC.md` | Phase 2 | Functional spec — Orb behavior rules, screen flows, interaction patterns, adaptive rhythm |
| `UIUX_SPEC_FINAL.md` | Phase 1 | Original UX spec — linear 5-screen flow, microcopy, animations, accessibility |
| `DESIGN_SYSTEM.md` | Phase 1 | Original design — Coral/Mint palette, Poppins/Comfortaa fonts (mostly superseded) |

---

## Technical Specs

| File | Phase | What It Tells You |
|------|-------|-------------------|
| `API_SPEC_MVP.md` | Phase 1 | Original API spec — 8 session-based endpoints (different from current implementation) |
| `TECHNICAL_SPEC.md` | Phase 1 | Original tech spec — React Native + Expo architecture (never built) |
| `IMPLEMENTATION_GUIDE.md` | Phase 1 | 7-day sprint plan — day-by-day tasks (JavaScript, not TypeScript) |

---

## Deployment & Config

| File | What It Tells You |
|------|-------------------|
| `render.yaml` | Render.com deployment — single Python web service, env vars |
| `vibeFoodBackend/requirements.txt` | Python dependencies |

---

## Important: What's Outdated

These documents describe plans that were **never implemented as written**:

- `TECHNICAL_SPEC.md` — Describes React Native + Expo + Zustand. Actual frontend is vanilla HTML/JS.
- `API_SPEC_MVP.md` — Describes session-based endpoints (`/sessions/{id}/...`). Actual API uses device-based flat endpoints (`/check-in`, `/scan`, etc.).
- `DESIGN_SYSTEM.md` — Describes Coral #FF6B6B / Mint #A8E6CF palette. Actual palette is Terracotta #C4654A / Sage #8BA888.
- `IMPLEMENTATION_GUIDE.md` — 7-day sprint plan. Actual build happened differently.

These are kept for historical context but should **not** be treated as source of truth for current code.

---

## Reading Order for Different Goals

### "I need to fix a bug or add a feature"
1. `onboarding/ONBOARDING.md` (5 min overview)
2. `vibeFoodBackend/CLAUDE.md` (coding instructions)
3. Read the relevant source code directly

### "I need to understand the product vision"
1. `docs/PHILOSOPHY.md` (the why)
2. `docs/PRD.md` (the what)
3. `docs/SPEC.md` (the how)

### "I need to understand what was built and why"
1. `onboarding/ONBOARDING.md`
2. `docs/PROGRESS.md`
3. `vibeFoodBackend/MVP Data Flow.md`

### "I need to understand the design system"
1. `docs/DESIGN.md` (current visual system)
2. `vibeFoodBackend/static/index.html` lines 10-45 (CSS variables — the actual implementation)
