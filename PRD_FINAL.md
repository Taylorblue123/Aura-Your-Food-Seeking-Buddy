# Product Requirements Document - FINAL
## Vibe Food: Never Eat Alone in Confusion Again

### 🎯 Product Vision
**"Your taste, understood"**

We're building an empathetic food companion that eliminates ordering anxiety for young internationals through familiar gestures, smart defaults, and progressive learning.

### 🧠 Core Insight
Young internationals don't need more information - they need confident decisions. Our app reduces infinite choices to 3 perfect options in under 90 seconds.

---

## 👥 User Personas (Refined)

### Primary: "Alex" (80% of users)
- **Age**: 22-28, international student/young professional
- **Digital Native**: Uses TikTok, Instagram, BeReal daily
- **Pain**: Menu paralysis, FOMO, language barriers
- **Behavior**: Makes decisions in <10 seconds on other apps
- **Success**: Orders confidently, discovers favorites, feels local

### Secondary: "Sam" (20% of users)
- **Age**: 25-35, social organizer
- **Context**: Group dinners, dates, team meals
- **Pain**: Accommodating preferences, decision fatigue
- **Success**: Quick consensus, happy group

---

## 🎨 Design Principles (UX-First)

### Core Principles
1. **Gesture > Buttons** - Swipe, pinch, drag (no hunting for buttons)
2. **Progressive Disclosure** - Right info at the right moment
3. **Emotional Design** - Each screen evokes: Curiosity → Confidence → Satisfaction
4. **Time-Boxed** - Every decision <10 seconds
5. **Thumb-Friendly** - All interactions in bottom 60% of screen

### Visual Identity
```css
/* Color System - Young & Warm */
--primary: #FF6B6B;     /* Sunset Coral - Energy */
--secondary: #A8E6CF;   /* Mint - Fresh */
--accent: #FFD93D;      /* Golden - Joy */
--base: #FAFAF8;        /* Warm White - Clean */
--text: #2C3E50;        /* Soft Black - Readable */

/* Typography */
--display: 'Poppins';   /* Headers - Friendly */
--body: -apple-system;  /* System - Performance */
--rounded: 'Comfortaa'; /* CTAs - Playful */
```

---

## 🗺️ User Journey (3 Core Screens)

### Screen 0: Onboarding (First Use Only - 20 seconds max)

#### The 2-Tap Onboarding
```
Tap 1: Value Promise
┌─────────────────────────┐
│                         │
│     Never eat alone     │
│    in confusion again   │
│                         │
│         🍜              │
│                         │
│   [Skip]  [I'm ready]   │
└─────────────────────────┘

Tap 2: Critical Info
┌─────────────────────────┐
│  Just need to know...   │
│                         │
│  Spice tolerance?       │
│  [🧊][🌶️][🔥]         │
│                         │
│  Any allergies?         │
│  [None] [Select]        │
│                         │
│     [Let's eat!]        │
└─────────────────────────┘
```

**Success Metrics**:
- Completion: >85% in <20 seconds
- Skip rate: <15%

### Screen 1: Capture + Vibe (Combined - 30 seconds max)

#### Adaptive Single Page
```
State A: Auto-Context Detection
┌─────────────────────────┐
│  Hey Alex, hungry? 😊   │ ← Personalized greeting
├─────────────────────────┤
│                         │
│  📸 Scan Menu           │ ← Auto-expands if no location
│  ─────────────          │
│  📍 Thai House nearby   │ ← Auto-expands if location detected
│                         │
└─────────────────────────┘

State B: Vibe Selection (Appears after restaurant selected)
┌─────────────────────────┐
│ Thai House 🌶️          │
│ "Authentic & spicy"     │
├─────────────────────────┤
│ What's your vibe?       │
│                         │
│  😌      🔥      💰     │ ← Primary vibes
│ Comfort  New   Budget   │
│                         │
│  ⚡ Quick (Lunch hour)  │ ← Contextual
│                         │
│ Party of [2] ↕          │
│                         │
│    [Get my order →]     │ ← Proceeds after 1+ selection
└─────────────────────────┘
```

**Interaction Design**:
- Auto-detection reduces taps by 50%
- Vibes auto-proceed at 3 selections
- Time-aware suggestions (lunch = quick)

### Screen 2: Order Plan (Swipeable - 30 seconds max)

#### Story-Driven Cards
```
┌─────────────────────────┐
│ Your Comfort Journey 🗺️ │ ← Narrative header
├─────────────────────────┤
│                         │
│   Start light...        │ ← Story beat
│ ╭───────────────────╮   │
│ │                   │   │
│ │   Spring Rolls    │   │
│ │   "Crispy & safe" │   │
│ │                   │   │
│ │ Because you picked │   │ ← Reasoning
│ │    'comfort'      │   │
│ ╰───────────────────╯   │
│                         │
│  ← Nope     Love it →   │ ← Swipe hints
│                         │
│     ● ○ ○ ○            │ ← Progress
└─────────────────────────┘

After all swipes:
┌─────────────────────────┐
│     Nailed it! 🎉      │
│                         │
│  You loved 3 dishes     │
│  Skipped 1 dish         │
│                         │
│ [Save as "My Usual"]    │
│ [Try Different Vibes]   │
│ [I'm Done]              │
└─────────────────────────┘
```

**Swipe Mechanics**:
- Right: ❤️ Love (green glow + haptic)
- Left: 👎 Nope (red fade + haptic)
- Up: ℹ️ Tell me more
- Down: Skip to summary

### Screen 3: Success & Learning (10 seconds)

```
┌─────────────────────────┐
│    Order saved! ✨      │
│                         │
│  Next time I'll know:   │
│  • You love mild       │
│  • You avoid seafood   │
│                         │
│    [Back to home]       │
└─────────────────────────┘
```

---

## 📊 Success Metrics (Revised)

### North Star Metric
**Time to Confident Order: <90 seconds**

### Key Performance Indicators

| Metric | Target | Measurement |
|--------|--------|-------------|
| Onboarding completion | >85% | % completing in <20s |
| First order success | >70% | % reaching order plan |
| Swipe completion | >70% | % swiping all cards |
| Return rate (7-day) | >40% | % using app again |
| Decision time | <10s per screen | Avg time on each decision |
| Delight moments | >2 per session | Celebrations triggered |

### Emotional Metrics
- App Store rating: >4.5
- "Wow" moments: >1 per first use
- Share rate: >20% tell a friend

---

## 🚀 MVP Scope (7 Days)

### MUST HAVE (Day 1-5)
✅ 3 core screens (Capture+Vibe, Plan, Success)
✅ Swipe gestures for feedback
✅ 3 mock restaurants
✅ 6 primary vibe bubbles
✅ Auto-context detection (time-based)
✅ Progress indicators
✅ Celebration moments

### NICE TO HAVE (Day 6-7)
🎯 Haptic feedback
🎯 Card stack animation
🎯 "My Usual" save
🎯 Voice input for vibes
🎯 Weather-based suggestions

### NOT IN MVP (Future)
❌ User accounts
❌ Real restaurant APIs
❌ Social sharing
❌ Payment integration
❌ AR preview
❌ Multi-language

---

## 🧩 Component Architecture

### Core Components (Reusable)

```javascript
// 1. AdaptiveCard
{
  states: ['collapsed', 'expanding', 'expanded'],
  props: {
    priority: 'auto|high|low',
    expandHeight: '30%|60%|80%',
    onExpand: Function,
    autoExpand: Boolean
  },
  animation: 'spring',
  duration: 300
}

// 2. VibeBubble
{
  states: ['idle', 'pressed', 'selected'],
  props: {
    emoji: String,
    label: String,
    context: 'time|party|history',
    maxSelection: 3
  },
  animation: 'scale',
  haptic: true
}

// 3. SwipeCard
{
  states: ['idle', 'dragging', 'swiping', 'swiped'],
  props: {
    threshold: 30, // % of screen width
    onSwipeRight: Function,
    onSwipeLeft: Function,
    rotationMax: 15 // degrees
  },
  physics: 'spring',
  returnAnimation: 200
}

// 4. ProgressDots
{
  props: {
    total: Number,
    current: Number,
    style: 'dots|bar|numbers'
  },
  animation: 'fade',
  size: { inactive: 8, active: 12 }
}
```

---

## 🎭 Interaction Patterns

### Gesture Dictionary
| Gesture | Action | Feedback |
|---------|--------|----------|
| Tap | Select/Expand | Scale + Haptic |
| Swipe Right | Approve | Green glow |
| Swipe Left | Reject | Red fade |
| Swipe Up | More info | Card flip |
| Swipe Down | Skip | Bounce down |
| Pinch | Zoom menu | Scale |
| Long Press | Preview | Peek card |

### Micro-Interactions
- Loading: Pulsing vibe bubbles
- Success: Confetti burst
- Error: Gentle shake
- Waiting: Breathing glow

---

## 📱 Technical Constraints

### Performance Targets
- Cold start: <2 seconds
- Screen transition: <300ms
- Gesture response: <16ms (60fps)
- API response: <3 seconds
- Offline capability: Last 3 restaurants cached

### Device Support
- iOS 13+ / Android 10+
- Screen: 5.5" - 6.7"
- Portrait only
- Minimum RAM: 2GB

---

## 🧪 Validation Plan

### Day 1-2: Technical Validation
- [ ] Swipe gestures working
- [ ] Screen transitions smooth
- [ ] Context detection accurate

### Day 3-4: UX Validation
- [ ] 5 users complete flow <90 seconds
- [ ] 3/5 users say "cool" or smile
- [ ] No users get stuck

### Day 5-7: Polish Validation
- [ ] Haptic feedback working
- [ ] Animations at 60fps
- [ ] Memory persists correctly

---

## 🎯 Why This Will Succeed

### The Magic Formula
1. **Familiar Gestures** (Tinder swipes) + **New Context** (Food) = Instant understanding
2. **Progressive Disclosure** + **Smart Defaults** = Reduced anxiety
3. **Emotional Design** + **Micro-Delights** = Memorable experience
4. **90-Second Promise** + **3 Screens** = Achievable satisfaction

### Competitive Advantage
- No app does swipe-based food selection
- No app combines context + preferences + memory
- No app targets international youth specifically
- No app makes ordering this fast

---

## 📈 Post-MVP Roadmap

### Week 2: Enhancement
- Real restaurant API
- Voice vibes
- Social proof ("3 friends loved this")

### Month 2: Expansion
- Group ordering
- Restaurant partnerships
- Dietary complexity

### Month 6: Intelligence
- Predictive ordering
- Meal planning
- Nutrition tracking

---

*"Make ordering food feel like swiping through TikTok - fast, fun, and personalized"*