# Gusto — DESIGN.md (Visual Design System)

> This file defines HOW THINGS LOOK. For how things work, see SPEC.md.
> Claude Code: always follow these values exactly. Never deviate.

---

## 1. Design DNA

Gusto is a warm food companion. Every visual decision serves one goal: make the user feel caught, accompanied, and remembered.

**Reference (borrow feeling, not layout):**
- Flourish: warm glowing orb, soft rounded UI
- Pi: calm white space, conversational feel
- Headspace: generous breathing room

**Visual anti-patterns (NEVER do these):**
- Dense info grids, star ratings, review counts (Yelp)
- Dark card stacks, gamified swipe loops (Tinder)
- Chat bubbles, typing indicators (messaging apps)
- Data tables, metrics, filters (dashboards)

---

## 2. Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| --bg | #FFF8F0 | Warm cream background (never pure white) |
| --bg-warm | #FFF3E8 | Slightly warmer surface (summary cards) |
| --surface | #FFFFFF | Card backgrounds (with soft warm shadow) |
| --terracotta | #C4654A | Primary accent, primary bubbles |
| --terracotta-deep | #A8503A | Pressed/active state |
| --amber | #D4956A | Secondary accent |
| --sage | #8BA888 | Positive/success states |
| --cream-shadow | #F5EDE8 | Secondary bubble bg, tag bg |
| --text-primary | #3D2E2A | Main text (never pure black) |
| --text-secondary | #7A6B65 | Subtitles, descriptions |
| --text-tertiary | #A89B95 | Hints, timestamps |
| --orb-a | #F4A27A | Orb gradient start (peach) |
| --orb-b | #F8D4B8 | Orb gradient end (light peach) |

**NEVER use:** pure white (#FFF) as background, pure black (#000) as text, cold blue, neon, gray-heavy palettes.

---

## 3. Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Gusto greeting | Fraunces (serif) | 24-30px | 500 italic |
| Emotional headlines | Fraunces | 26-32px | 500 |
| Keyword emphasis | Fraunces | inherit | 500 italic, color: terracotta |
| Card headline | Nunito | 20px | 600 |
| Body text | Nunito | 16px | 400, line-height 1.6 |
| Bubble text | Nunito | 15-16px | 600 |
| Subtle text | Nunito | 14px | 400 |
| Tiny text | Nunito | 12px | 400, tertiary color |
| Section marker | Nunito | 10px | 800, uppercase, letter-spacing 0.2em |

**Tone rule:** Gusto speaks in first person, like a friend texting. NEVER system language ("Recommended for you based on preferences"). NEVER data language ("4.5 stars · 200 reviews · $$").

---

## 4. Spacing and Layout

| Rule | Value |
|------|-------|
| Screen padding | 24px all sides |
| Between major sections | 32px |
| Card internal padding | 20px |
| Max content width | 340px (mobile) |

**Principles:** Single column. Centered. Vertical flow. Progressive reveal (fade in, not dump). Generous whitespace — when in doubt, add more space.

---

## 5. Component Visuals

### 5.1 Gusto Orb

**Conversation mode (center):**
- Size: 80-100px diameter
- Gradient: radial, #F4A27A center → #F8D4B8 edge
- Inner highlight: white specular at top-left (22%, 18%), blur 3px
- Outer halo: radial glow, peach, blur 14px, pulsing opacity 0.5-0.78
- Shadow: `0 18px 44px -10px rgba(196,101,74,0.45)`

**Display mode (top):**
- Size: 16-20px diameter
- Same gradient, simplified (no specular, no halo)
- Shadow: `0 3px 8px -1px rgba(196,101,74,0.5)`

**Animations:**
- Resting breath: scale 1 → 1.055 → 1, 3.6s cycle, ease-in-out
- Thinking tremor: scale + x jitter, 0.6s cycle, faster
- Fade in/out: opacity 0-1, 320ms, ease
- Mode switch (center↔top): position + scale, 400ms, ease-in-out

### 5.2 Bubble Buttons

**Shape:** Circular or near-circular. NEVER horizontal ellipses. NEVER wider than tall. Organic scatter positioning, NOT a vertical stack.

**Sizes:** 60-80px for short text, up to 100px for longer. Always rounder than wider.

**Colors (varied, not uniform):**
- Primary: --terracotta fill, #FFF8F0 text
- Secondary options: varied warm tones (#F5EDE8, #E8D5C4, #D4E2D0, --cream-shadow) with --text-primary text
- Each bubble slightly different color for organic feel

**Shadows:**
- Primary: `0 14px 30px -10px rgba(196,101,74,0.48)`
- Secondary: `0 10px 24px -9px rgba(61,46,42,0.2)`

**Text:** 15-16px Nunito SemiBold, centered

**Animations:**
- Emerge: from center outward, spring stiffness 240, damping 22, staggered delay 0.08s each
- Collapse (selected): shrink to center, 320ms
- Scatter (unselected): drift outward in different directions, 450ms

### 5.3 Rounded Card

- Border-radius: 20-26px
- Background: --surface (#FFF)
- Shadow: `0 24px 60px -14px rgba(61,46,42,0.28)`
- Photo area: top of card, border-radius matches card top corners
- Photo style: warm-lit, appetizing, close-up. Looks like a friend took it. NOT stock-sterile. NOT overhead flat-lay.

**Swipe affordance hints:**
- Bottom of screen: subtle text "← not today · let's go →"
- 10px font, uppercase, letter-spacing 0.18em, tertiary color

### 5.4 Ambiance Tag

- Shape: pill, height 28px, padding 8px 14px, border-radius 999px
- Background: --cream-shadow
- Text: --text-secondary, 12px Nunito Bold
- Position: below restaurant name, before recommendation reason

### 5.5 Memory Bubble (Orb Home)

- Size: 24-36px diameter
- Contains: tiny food photo (circular, clipped) or restaurant initial letter
- Very soft glow, same peach tint as orb but much subtler
- Floating animation: gentle organic drift, not mechanical orbit
- New memory: briefly glows terracotta border on arrival

### 5.6 Transition Animations

| Transition | Duration | Easing |
|-----------|----------|--------|
| Between beats | 300ms | ease-out |
| Content fade in | 400ms | ease |
| Gusto response after tap | 200ms pause, then fade | ease |
| Card swap | 300ms out, 300ms in | ease-out |
| Orb mode switch | 400ms | ease-in-out |
| Greeting pause before bubbles | 1500ms | — |

**NEVER:** snap transitions, bounce effects, slide-from-side.

### 5.7 Scene Marker (top of screen)

- Position: absolute, top 58px, centered
- Font: 10px Nunito, weight 800, uppercase, letter-spacing 0.28em
- Color: --terracotta, opacity 0.55
- Decorative dashes on either side