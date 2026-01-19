# Vibe Food App - Design System & UI/UX Guide

## 🎯 Design Philosophy
**"Warm, Minimal, Delightful"** - Every interaction should feel like a friendly food recommendation from a local friend.

## 🎨 4-Hour Design Sprint Plan

### Hour 1: Core Screens Wireframes (Low-Fidelity)
Focus on user flow, not aesthetics.

### Hour 2: Visual Design System
Colors, typography, spacing, components.

### Hour 3: High-Fidelity Key Screens
Polish the 6 essential screens.

### Hour 4: Interactions & Micro-animations
Define transitions and feedback.

## 📱 6 Essential Screens

### 1. Onboarding (First-time only)
```
┌─────────────────────┐
│     Welcome!        │
│                     │
│   🍜  Vibe Food    │
│                     │
│  "Your AI food      │
│   companion"        │
│                     │
│ [Get Started] →     │
└─────────────────────┘
```
**Components:** Hero image, tagline, CTA button
**Time to design:** 15 min

### 2. Capture Screen (Tab 1)
```
┌─────────────────────┐
│ 📸 Camera View      │
│                     │
│ ┌─────────────────┐ │
│ │                 │ │
│ │  Camera Feed    │ │
│ │                 │ │
│ └─────────────────┘ │
│                     │
│ [Capture Menu] 📸   │
│                     │
│ or select nearby ↓  │
└─────────────────────┘
```
**Components:** Camera view, capture button, alternative action
**Time to design:** 30 min

### 3. Restaurant Picker (Modal)
```
┌─────────────────────┐
│ 📍 Nearby (0.5 mi)  │
├─────────────────────┤
│ Thai House          │
│ Thai • $$ • 0.3 mi  │
│ ★★★★☆ (4.5)        │
├─────────────────────┤
│ Burger Joint        │
│ American • $ • 0.5  │
│ ★★★★☆ (4.2)        │
├─────────────────────┤
│ Sushi Spot          │
│ Japanese • $$$      │
│ ★★★★★ (4.7)        │
└─────────────────────┘
```
**Components:** Restaurant cards, filters, search
**Time to design:** 30 min

### 4. Vibe Selection (Tab 2)
```
┌─────────────────────┐
│  What's your vibe?  │
│                     │
│ ┌──────┐  ┌──────┐ │
│ │  🤗  │  │  🚀  │ │
│ │Comfort│  │ Try  │ │
│ └──────┘  │ New  │ │
│           └──────┘ │
│ ┌──────┐  ┌──────┐ │
│ │  🥗  │  │  🍖  │ │
│ │ Light │  │Hearty│ │
│ └──────┘  └──────┘ │
│                     │
│ How many? [1][2][3+]│
│                     │
│ [Get My Plan] →     │
└─────────────────────┘
```
**Components:** Vibe bubbles, party size selector, CTA
**Time to design:** 45 min

### 5. Order Plan Result
```
┌─────────────────────┐
│ Your Perfect Order  │
├─────────────────────┤
│ For 2 people        │
│                     │
│ 1. Pad Thai 🍜      │
│    Mild & comforting│
│    "Pad Thai, mild" │
│                     │
│ 2. Spring Rolls 🥟  │
│    Light starter    │
│    "Fresh rolls"    │
│                     │
│ 3. Mango Rice 🥭    │
│    Sweet ending     │
│    "Khao niao"      │
│                     │
│ Total: $28-32       │
│                     │
│ [Order Complete ✓]  │
└─────────────────────┘
```
**Components:** Order cards, reasoning, phrase helper
**Time to design:** 45 min

### 6. Feedback Screen (Modal)
```
┌─────────────────────┐
│   How was it?       │
│                     │
│   ⭐⭐⭐⭐⭐         │
│                     │
│ What worked?        │
│ [Perfect] [Too much]│
│ [Too spicy] [Loved] │
│                     │
│ [Save Feedback]     │
└─────────────────────┘
```
**Components:** Star rating, quick tags, submit
**Time to design:** 15 min

## 🎨 Visual Design System

### Color Palette
```css
/* Primary */
--primary: #FF6B6B;      /* Warm Coral - CTAs */
--primary-light: #FFE5E5; /* Light Pink - Backgrounds */

/* Neutrals */
--text-primary: #2D3436;  /* Dark Gray - Main text */
--text-secondary: #636E72; /* Gray - Secondary text */
--background: #FFFFFF;    /* White - Main bg */
--surface: #F5F5F5;      /* Light Gray - Cards */

/* Semantic */
--success: #00B894;      /* Green - Success states */
--warning: #FDCB6E;      /* Yellow - Warnings */
--info: #74B9FF;         /* Blue - Information */
```

### Typography
```javascript
const typography = {
  // Headers
  h1: {
    fontFamily: 'System',
    fontSize: 32,
    fontWeight: '700',
    lineHeight: 40
  },
  h2: {
    fontFamily: 'System',
    fontSize: 24,
    fontWeight: '600',
    lineHeight: 32
  },

  // Body
  body: {
    fontFamily: 'System',
    fontSize: 16,
    fontWeight: '400',
    lineHeight: 24
  },

  // Components
  button: {
    fontFamily: 'System',
    fontSize: 18,
    fontWeight: '600',
    letterSpacing: 0.5
  },

  caption: {
    fontFamily: 'System',
    fontSize: 14,
    fontWeight: '400',
    lineHeight: 20
  }
};
```

### Spacing System (8-point grid)
```javascript
const spacing = {
  xs: 4,   // Tiny gaps
  sm: 8,   // Small padding
  md: 16,  // Default spacing
  lg: 24,  // Section spacing
  xl: 32,  // Large gaps
  xxl: 48  // Page margins
};
```

### Component Library

#### Primary Button
```javascript
// Visual specs
{
  backgroundColor: '#FF6B6B',
  paddingVertical: 16,
  paddingHorizontal: 32,
  borderRadius: 12,
  fontSize: 18,
  fontWeight: '600',
  color: '#FFFFFF',
  shadow: {
    shadowColor: '#FF6B6B',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8
  }
}
```

#### Vibe Bubble
```javascript
// Visual specs
{
  width: '45%',
  aspectRatio: 1.2,
  backgroundColor: '#FFE5E5',
  borderRadius: 20,
  padding: 20,
  alignItems: 'center',
  justifyContent: 'center',
  // Selected state
  selected: {
    borderWidth: 3,
    borderColor: '#FF6B6B',
    transform: [{ scale: 0.95 }]
  }
}
```

#### Order Card
```javascript
// Visual specs
{
  backgroundColor: '#FFFFFF',
  borderRadius: 16,
  padding: 20,
  marginBottom: 16,
  borderLeftWidth: 4,
  borderLeftColor: '#FF6B6B',
  shadow: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 8
  }
}
```

## 🎬 Micro-interactions

### Touch Feedback
- **Buttons:** Scale to 0.95 on press
- **Cards:** Subtle shadow increase on press
- **Bubbles:** Bounce animation on select

### Transitions
- **Screen navigation:** Slide horizontal (300ms)
- **Modal appearance:** Slide up (250ms)
- **Loading states:** Pulse animation

### Feedback Animations
```javascript
// Success checkmark
Animated.sequence([
  Animated.spring(scale, { toValue: 1.2 }),
  Animated.spring(scale, { toValue: 1.0 })
]);

// Error shake
Animated.sequence([
  Animated.timing(translateX, { toValue: -10, duration: 50 }),
  Animated.timing(translateX, { toValue: 10, duration: 50 }),
  Animated.timing(translateX, { toValue: 0, duration: 50 })
]);
```

## 🚀 Figma Quick Setup

### 1. Create New File
- Mobile frame: iPhone 14 (390 × 844)
- Grid: 8pt with 16pt margins

### 2. Import UI Kit
- Search "iOS 17 UI Kit" in Community
- Or "Material 3 Design Kit"

### 3. Create Components
1. Button (3 variants: primary, secondary, text)
2. Vibe Bubble (2 states: default, selected)
3. Restaurant Card
4. Order Item Card
5. Navigation Bar

### 4. Build Screens
- Use components consistently
- Apply auto-layout everywhere
- Link screens with prototype connections

### 5. Export for Development
```
Settings:
- Format: PNG (2x for Retina)
- Include: Component specs
- Export: Design tokens as JSON
```

## 📏 Design Handoff Checklist

### For Developers
- [ ] Color hex values
- [ ] Font sizes and weights
- [ ] Spacing measurements
- [ ] Border radius values
- [ ] Shadow specifications
- [ ] Animation durations
- [ ] Touch target sizes (min 44pt)

### Assets to Export
- [ ] App icon (1024×1024)
- [ ] Splash screen (2732×2732)
- [ ] Tab bar icons (25×25 @2x, @3x)
- [ ] Empty state illustrations
- [ ] Success/error icons

## 🎯 Design Principles

### 1. Clarity Over Cleverness
- Clear CTAs
- Obvious navigation
- Predictable interactions

### 2. Speed is a Feature
- Instant feedback
- Skeleton screens
- Optimistic updates

### 3. Delight in Details
- Micro-animations
- Haptic feedback
- Celebration moments

### 4. Accessibility First
- High contrast ratios (4.5:1 minimum)
- Large touch targets (44×44pt)
- Clear focus states

## 🔗 Design Resources

### Free Tools
- **Figma:** figma.com (Free for 3 projects)
- **Excalidraw:** excalidraw.com (Open source)
- **Whimsical:** whimsical.com (Free tier)
- **Penpot:** penpot.app (Open source Figma alternative)

### Quick Mockup Tools
- **shots.so** - Beautiful mockups in seconds
- **mockuphone.com** - Device frames
- **ui8.net** - Free UI kits

### AI Design Assistants
- **v0.dev** - Generate React components from prompts
- **galileo-ai.com** - AI UI generation
- **uizard.io** - Sketch to design

---

## ⏱️ Time-Saving Tips

1. **Use a UI Kit** - Don't design from scratch
2. **Design at 1x** - Scale up later
3. **Grayscale First** - Add colors last
4. **Copy Successful Apps** - Thai food apps for inspiration
5. **Component Everything** - Reuse, don't rebuild

Remember: For MVP, "good enough" design that ships beats perfect design that doesn't!