# UI/UX Design Specification
## Vibe Food - Gesture-First Food Ordering Experience

### 🎨 Design Philosophy
**"Feels like chatting with a friend who knows your taste"**

Every interaction should feel natural, not learned. We're borrowing mental models from TikTok, Tinder, and Instagram to create instant familiarity.

---

## 🎯 UX Strategy

### Core UX Principles
1. **One Thumb Rule** - Everything reachable with one thumb
2. **10-Second Decisions** - No screen takes >10 seconds
3. **Gesture Memory** - Use gestures users already know
4. **Progressive Trust** - Earn trust before asking for data
5. **Delight Density** - 2+ smile moments per session

### Emotional Journey Map
```
Curious → Confident → Satisfied → Loyal
   ↓         ↓           ↓         ↓
"What's this?" → "I got this" → "That was easy!" → "My usual app"
```

---

## 🎨 Visual Design System

### Color Palette (Optimized for Young Internationals)

```css
/* Primary Palette - Energy & Warmth */
:root {
  /* Main Actions */
  --coral-primary: #FF6B6B;      /* CTAs, selected states */
  --coral-light: #FFB3B3;        /* Hover states */
  --coral-dark: #E85555;         /* Pressed states */

  /* Supporting Colors */
  --mint-fresh: #A8E6CF;         /* Success, positive */
  --mint-light: #C8F7E4;         /* Success backgrounds */

  --golden-joy: #FFD93D;         /* Celebrations, ratings */
  --golden-light: #FFE980;       /* Highlights */

  /* Base Colors */
  --warm-white: #FAFAF8;         /* Main background */
  --soft-gray: #F5F5F3;          /* Card backgrounds */
  --text-primary: #2C3E50;       /* Main text */
  --text-secondary: #7F8C8D;     /* Secondary text */

  /* Semantic Colors */
  --love-green: #4CAF50;         /* Swipe right */
  --nope-red: #F44336;           /* Swipe left */
  --info-blue: #2196F3;          /* Information */
}
```

### Typography System

```css
/* Display - Personality & Impact */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&display=swap');

/* Body - Readability & Performance */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;

/* Accent - Playfulness */
@import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@400;700&display=swap');

/* Type Scale */
.display-large {
  font: 700 32px/40px 'Poppins', sans-serif;
  letter-spacing: -0.02em;
}

.display-medium {
  font: 600 24px/32px 'Poppins', sans-serif;
  letter-spacing: -0.01em;
}

.body-large {
  font: 400 18px/28px system-ui;
  letter-spacing: 0;
}

.body-medium {
  font: 400 16px/24px system-ui;
  letter-spacing: 0;
}

.caption {
  font: 400 14px/20px system-ui;
  letter-spacing: 0.01em;
}

.button-text {
  font: 600 16px/24px 'Comfortaa', sans-serif;
  letter-spacing: 0.02em;
  text-transform: none; /* No uppercase */
}
```

### Spacing & Grid System

```javascript
// 8-point Grid System
const spacing = {
  xxs: 4,   // Micro spacing
  xs: 8,    // Tight spacing
  sm: 12,   // Small gaps
  md: 16,   // Default spacing
  lg: 24,   // Section spacing
  xl: 32,   // Large gaps
  xxl: 48,  // Page margins
  huge: 64  // Major sections
};

// Layout Grid
const grid = {
  columns: 12,
  gutter: 16,
  margin: 20,
  maxWidth: 390, // iPhone 14 width
};

// Safe Areas
const safeArea = {
  top: 44,      // Status bar
  bottom: 34,   // Home indicator
  sides: 20     // Thumb reach
};
```

---

## 📱 Screen Specifications

### Screen 0: Onboarding (2-Tap Magic)

#### Tap 1: Value Screen
```
Layout:
┌─────────────────────────┐
│      Status Bar (44)    │
├─────────────────────────┤
│         (120)           │
│     Animated Icon       │ ← Lottie animation
│         🍜             │   Gentle bounce
│         (80)           │
├─────────────────────────┤
│     Display Large      │
│   "Never eat alone"    │ ← Typewriter effect
│  "in confusion again"  │
│         (60)           │
├─────────────────────────┤
│                        │
│    [Skip]  [I'm ready] │ ← Ghost / Primary button
│         (100)          │
└─────────────────────────┘

Specs:
- Background: Gradient (coral → warm white)
- Animation: Icon bounces every 2s
- Buttons: Skip (ghost), Ready (filled)
- Transition: Fade + slide up
```

#### Tap 2: Preference Screen
```
Layout:
┌─────────────────────────┐
│      Progress Bar       │ ← 50% filled
├─────────────────────────┤
│     "Quick setup"      │
│   "Just 2 questions"   │
├─────────────────────────┤
│     Spice Level?       │
│   ┌────┬────┬────┐    │
│   │ 🧊 │ 🌶️ │ 🔥 │    │ ← Segmented control
│   │None│Mild│Hot │    │
│   └────┴────┴────┘    │
├─────────────────────────┤
│     Allergies?         │
│   [None] [Select →]    │ ← Chips
├─────────────────────────┤
│     [Let's eat!]       │ ← Enabled after 1 selection
└─────────────────────────┘

Interactions:
- Spice: Single select, instant feedback
- Allergies: Multi-select sheet if needed
- Progress: Smooth fill animation
- Button: Disabled → Enabled with spring
```

### Screen 1: Capture + Vibe (Adaptive Hub)

#### State A: Restaurant Detection
```
┌─────────────────────────┐
│    "Hey Alex! 👋"       │ ← Personalized, time-aware
│   "Lunch time?"         │   "Dinner?" (after 6pm)
├─────────────────────────┤
│  ╭─────────────────╮   │
│  │   📸 Camera     │   │ ← 180px height collapsed
│  │  "Scan a menu"  │   │   Expands to 70% on tap
│  ╰─────────────────╯   │   Shadow: 0 4px 12px rgba(0,0,0,0.1)
│         8px gap        │
│  ╭─────────────────╮   │
│  │   📍 Nearby     │   │ ← Auto-expands if location on
│  │  Thai House     │   │   Shows top 3 restaurants
│  │  0.3 mi • $$   │   │
│  ╰─────────────────╯   │
└─────────────────────────┘

Card Animations:
- Tap: Scale(0.98) → Scale(1.0) with spring
- Expand: Height animates over 300ms
- Shadow increases on expansion
- Other card fades to 60% opacity
```

#### State B: Vibe Selection
```
┌─────────────────────────┐
│  Thai House • Spicy 🌶️ │ ← Restaurant context (40px)
├─────────────────────────┤
│   "What's your vibe?"   │ ← Question format
│                        │
│   ╭────╮ ╭────╮ ╭────╮│ ← Vibe bubbles (100x100)
│   │ 😌 │ │ 🔥 │ │ 💰 ││   Rounded squares
│   │Safe│ │New │ │Save││   Shadow on selection
│   ╰────╯ ╰────╯ ╰────╯│
│                        │
│   ╭────╮ ╭────╮       │ ← Contextual vibes
│   │ ⚡ │ │ 👥 │       │   Appear based on time/party
│   │Fast│ │Share│      │
│   ╰────╯ ╰────╯       │
│                        │
│   Party size: [−][2][+]│ ← Stepper control
│                        │
│      [Get my plan →]   │ ← Enabled after 1 vibe
└─────────────────────────┘

Bubble Behavior:
- Idle: Subtle breathing animation
- Hover: Scale(1.05) + shadow
- Selected: Scale(0.95) + colored border
- Max 3 selections (auto-proceed)
- Haptic: Light on select
```

### Screen 2: Order Plan (Story Cards)

```
┌─────────────────────────┐
│  "Your comfort journey" │ ← Dynamic title
│      for 2 people       │   Based on vibes selected
├─────────────────────────┤
│                        │
│  ╭───────────────────╮ │ ← Card stack (peek next)
│  │  Spring Rolls 🥟   │ │   Border-radius: 20px
│  │                   │ │   Shadow: 0 8px 24px
│  │  [Image holder]   │ │
│  │                   │ │
│  │  "Light & crispy  │ │
│  │   perfect to      │ │
│  │   share"          │ │
│  │                   │ │
│  │  Why: You picked  │ │ ← Reasoning (smaller text)
│  │  'comfort+share'  │ │
│  ╰───────────────────╯ │
│                        │
│  👎 ← Swipe → 👍       │ ← Visual hints
│                        │
│  ● ● ○ ○               │ ← Progress dots
└─────────────────────────┘

Swipe Physics:
- Threshold: 30% screen width
- Max rotation: 15°
- Right: Green glow + scale(1.05)
- Left: Red fade + scale(0.95)
- Return spring: tension=40, friction=10
- Next card scales from 0.95 → 1.0
```

### Screen 3: Success State

```
┌─────────────────────────┐
│                        │
│       ✨ 🎉 ✨        │ ← Confetti animation
│                        │
│    "Nailed it!"        │ ← Celebration copy
│                        │
│   You loved 3 dishes   │
│   Skipped 1 dish       │
│                        │
│  ╭─────────────────╮   │
│  │ Save as my usual │   │ ← Optional action
│  ╰─────────────────╯   │
│                        │
│  ╭─────────────────╮   │
│  │   Try new vibes  │   │ ← Re-engage
│  ╰─────────────────╯   │
│                        │
│  [Back home] (text)    │ ← Low emphasis
└─────────────────────────┘

Animations:
- Confetti: 1.5s burst
- Text: Fade in sequence
- Buttons: Slide up staggered
- Haptic: Success pattern
```

---

## 🎬 Micro-Interactions & Animations

### Animation Principles
```javascript
// Spring configurations
const springs = {
  gentle: { tension: 120, friction: 14 },
  bouncy: { tension: 180, friction: 12 },
  stiff: { tension: 210, friction: 20 }
};

// Timing functions
const timings = {
  quick: 200,    // Feedback
  normal: 300,   // Transitions
  slow: 500      // Major changes
};

// Easing curves
const easings = {
  in: 'cubic-bezier(0.4, 0, 1, 1)',
  out: 'cubic-bezier(0, 0, 0.2, 1)',
  inOut: 'cubic-bezier(0.4, 0, 0.2, 1)'
};
```

### Gesture Feedback Matrix

| Gesture | Visual | Haptic | Duration |
|---------|---------|--------|----------|
| Tap | Scale 0.98→1.0 | Light | 150ms |
| Long Press | Scale 1.0→1.05 + blur bg | Medium | 200ms |
| Swipe Start | Rotate + fade | None | Real-time |
| Swipe Success | Fly away + fade | Success | 300ms |
| Selection | Border + shadow | Light | 200ms |
| Loading | Pulse opacity | None | 1000ms loop |

### Celebration Moments

```javascript
// Trigger conditions
const celebrations = {
  firstOrder: "confetti",      // First successful order
  allLoved: "hearts",          // Loved all dishes
  quickDecision: "lightning",  // <5 sec decision
  returning: "wave",           // Second session
  savedUsual: "bookmark"       // Saved preferences
};

// Animation specs
const confetti = {
  particles: 30,
  spread: 45,
  startVelocity: 45,
  gravity: 0.5,
  colors: ['#FF6B6B', '#A8E6CF', '#FFD93D']
};
```

---

## 📐 Component Library

### 1. AdaptiveCard Component
```jsx
// Usage
<AdaptiveCard
  priority="auto"        // auto|high|low
  expandHeight="60%"     // % of screen
  isExpanded={false}
  onExpand={() => {}}
  autoExpand={hasLocation}
>
  <CardContent />
</AdaptiveCard>

// Styles
const cardStyles = {
  collapsed: {
    height: 120,
    borderRadius: 16,
    shadow: '0 2px 8px rgba(0,0,0,0.08)'
  },
  expanded: {
    height: '60%',
    borderRadius: 20,
    shadow: '0 8px 24px rgba(0,0,0,0.12)'
  },
  animation: {
    type: 'spring',
    stiffness: 260,
    damping: 20
  }
};
```

### 2. VibeBubble Component
```jsx
// Usage
<VibeBubble
  emoji="😌"
  label="Comfort"
  subtitle="Safe choices"
  isSelected={false}
  onSelect={() => {}}
  context="time"        // time|party|history
  disabled={false}
/>

// Visual states
const bubbleStates = {
  idle: {
    scale: 1,
    opacity: 1,
    borderWidth: 0
  },
  pressed: {
    scale: 0.95,
    opacity: 0.8
  },
  selected: {
    scale: 1,
    borderWidth: 3,
    borderColor: '#FF6B6B',
    shadow: '0 4px 12px rgba(255,107,107,0.3)'
  }
};
```

### 3. SwipeableCard Component
```jsx
// Usage
<SwipeableCard
  onSwipeLeft={() => {}}   // Reject
  onSwipeRight={() => {}}  // Accept
  onSwipeUp={() => {}}     // More info
  threshold={0.3}           // 30% of screen width
>
  <DishCard data={dish} />
</SwipeableCard>

// Physics
const swipePhysics = {
  rotationMultiplier: 0.05,  // Rotation based on X
  maxRotation: 15,            // Max degrees
  swipeThreshold: 120,        // Pixels to trigger
  velocityThreshold: 0.5,     // Speed to trigger
  springBack: {
    stiffness: 185,
    damping: 15
  }
};
```

### 4. ProgressIndicator Component
```jsx
// Usage
<ProgressIndicator
  total={4}
  current={2}
  style="dots"           // dots|bar|numbers
  animated={true}
/>

// Styles
const progressStyles = {
  dot: {
    inactive: {
      size: 8,
      opacity: 0.3,
      color: '#7F8C8D'
    },
    active: {
      size: 12,
      opacity: 1,
      color: '#FF6B6B'
    }
  },
  animation: {
    scale: 'spring(1, 0.8, 300)'
  }
};
```

---

## 📱 Responsive Behavior

### Breakpoints
```javascript
const breakpoints = {
  small: 320,   // iPhone SE
  medium: 375,  // iPhone 12/13 mini
  large: 390,   // iPhone 14
  xlarge: 428,  // iPhone 14 Plus
  tablet: 768   // iPad mini
};
```

### Safe Zones
```javascript
// Thumb reachability map
const thumbZones = {
  easy: {
    top: '40%',
    bottom: '100%',
    sides: '80%'  // Of screen width
  },
  stretch: {
    top: '20%',
    bottom: '100%',
    sides: '100%'
  },
  hard: {
    top: '0%',
    bottom: '20%',
    corners: true
  }
};

// Place critical actions in easy zone
// Place navigation in stretch zone
// Avoid hard zone for interactions
```

---

## 🎯 Accessibility

### Standards
- WCAG 2.1 AA Compliance
- Minimum touch target: 44×44pt
- Color contrast: 4.5:1 minimum
- Font size: 14pt minimum

### Implementation
```javascript
// Accessibility props
const a11y = {
  // Labels
  accessibilityLabel: "Select comfort food vibe",
  accessibilityHint: "Double tap to select this vibe",
  accessibilityRole: "button",

  // States
  accessibilityState: {
    selected: isSelected,
    disabled: isDisabled
  },

  // Actions
  accessibilityActions: [
    { name: 'activate', label: 'Select' },
    { name: 'longpress', label: 'Preview' }
  ],

  // Live regions
  accessibilityLiveRegion: "polite",
  accessibilityValue: { text: `${current} of ${total}` }
};
```

---

## 🧪 Usability Testing Checklist

### Task Success Metrics
- [ ] Complete onboarding < 20 seconds
- [ ] Select restaurant < 10 seconds
- [ ] Choose vibes < 10 seconds
- [ ] Review all cards < 30 seconds
- [ ] Complete full flow < 90 seconds

### Delight Metrics
- [ ] User smiles/laughs: >1 time
- [ ] "Cool" or "Wow": >1 time
- [ ] Shows friend: >20% of users
- [ ] Returns next day: >40% of users

### Error Recovery
- [ ] Can go back at any point
- [ ] Can skip any step
- [ ] Can restart flow easily
- [ ] Errors are friendly/helpful

---

## 🚀 Implementation Priority

### Phase 1: Core Mechanics (Day 1-2)
1. Swipe gesture system
2. Basic card components
3. Screen transitions

### Phase 2: Visual Polish (Day 3-4)
1. Color system
2. Typography
3. Shadows/elevation

### Phase 3: Delight (Day 5-6)
1. Micro-animations
2. Haptic feedback
3. Celebration moments

### Phase 4: Optimization (Day 7)
1. Performance tuning
2. Accessibility
3. Error states

---

*"Design is not just what it looks like. Design is how it works." - Steve Jobs*

*For Vibe Food: Design is how it feels in your thumb.*