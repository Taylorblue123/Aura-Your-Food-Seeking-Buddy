# Vibe Food App - Product Requirements Document (JavaScript MVP)
**Version:** 1.0
**Timeline:** 7-Day Sprint
**Tech Stack:** JavaScript (React Native/Expo + Node.js/FastAPI)

## 🎯 Executive Summary

A warm, minimal food ordering companion that helps non-native/non-local residents overcome menu anxiety through photo capture, vibe-based preferences, and adaptive memory - all built in JavaScript for rapid prototyping.

## 📱 Product Overview

### Vision
"Take a photo, share your vibe, get a smart order plan that remembers you."

### Target Users
- International students
- Young professionals new to the area
- Non-native speakers
- Anyone facing menu decision paralysis

### Core Value Proposition
1. **10-second understanding** - Photo to explanation instantly
2. **30-second personalization** - Vibe bubbles to order plan
3. **Improving experience** - Each use makes recommendations better

## 🔄 User Journey (MVP)

```
┌─────────────┐     ┌──────────┐     ┌────────┐     ┌───────────┐     ┌──────────┐
│   Capture   │ --> │  Explain │ --> │  Ask   │ --> │ Recommend │ --> │ Feedback │
│Photo/Select │     │Restaurant│     │  Vibe  │     │Order Plan │     │  Rating  │
└─────────────┘     └──────────┘     └────────┘     └───────────┘     └──────────┘
```

## 🎨 UI/UX Design

### Two-Tab Architecture

**Tab A: Capture**
- Camera button (primary CTA)
- "Select Nearby" (secondary option)
- Recent restaurants (optional for v1)

**Tab B: Vibe**
- Bubble selection interface
- Chat input (fallback)
- Order plan cards
- Feedback stars

### Design Principles
- **Warm**: Friendly colors, rounded corners, encouraging copy
- **Minimal**: No more than 3 actions per screen
- **Fast**: Every interaction < 2 seconds response

## 💻 Technical Architecture (JavaScript)

### Frontend Stack
```javascript
// Mobile App Structure
mobile/
├── App.js                 // Main app entry
├── src/
│   ├── screens/          // Screen components
│   │   ├── CaptureScreen.js
│   │   ├── VibeScreen.js
│   │   └── PlanScreen.js
│   ├── components/       // Reusable components
│   │   ├── BubbleSelector.js
│   │   ├── OrderPlanCard.js
│   │   └── CameraView.js
│   ├── services/         // API calls
│   │   └── api.js
│   ├── store/           // Zustand state
│   │   └── useStore.js
│   └── utils/           // Helper functions
│       └── constants.js
```

### Backend Stack
```python
# FastAPI Backend (Python remains for backend)
backend/
├── app/
│   ├── main.py          # FastAPI application
│   ├── routers/         # API endpoints
│   ├── engines/         # Three AI engines
│   ├── models/          # Database models
│   └── mock_data/       # Test restaurant data
```

### API Contracts (Simplified JavaScript-friendly)

```javascript
// Intent Structure
const intent = {
  partySize: 2,
  hunger: "normal", // "light" | "normal" | "very_hungry"
  vibes: ["comfort", "warm"],
  budget: "$",
  constraints: {
    allergies: [],
    spiceMax: 2
  }
}

// Order Plan Response
const orderPlan = {
  planType: "share",
  items: [
    {
      name: "Pad Thai",
      reason: "Comfort favorite, mild spice",
      orderPhrase: "Pad Thai, mild please"
    }
  ],
  totalItems: 3,
  estimatedCost: "$25-30"
}
```

## 🚀 Features Scope

### IN SCOPE (Week 1)
| Feature | Implementation | JavaScript Approach |
|---------|---------------|-------------------|
| Camera Capture | Expo Camera API | `expo-camera` package |
| Location Services | Expo Location | `expo-location` |
| Bubble UI | Native Base components | Pre-built React Native UI |
| Mock Restaurants | 3 hardcoded | JSON files |
| Basic Memory | Device storage | AsyncStorage |
| Simple Feedback | Star rating | React Native elements |

### OUT OF SCOPE
- User authentication (use device ID)
- Real OCR (mock menu data)
- Payment processing
- Social features
- Complex animations
- TypeScript types
- Unit tests (week 2)

## 🔧 Three-Engine System (Simplified for JS)

### 1. Reasoning Engine
```javascript
// Simple template-based reasoning
function generateOrderPlan(intent, menuContext, memory) {
  const template = selectTemplate(intent.vibes);
  const items = matchMenuItems(template, menuContext);
  return formatOrderPlan(items, intent.partySize);
}
```

### 2. Reflection Engine
```javascript
// Basic feedback processor
function processFeeback(rating, orderedItems, memory) {
  if (rating >= 4) {
    memory.preferences.push(...orderedItems);
  }
  return updateMemory(memory);
}
```

### 3. Adaptive Memory
```javascript
// Simple JSON storage
const memory = {
  userId: "device_123",
  allergies: [],
  lovedDishes: [],
  avoidList: [],
  lastOrders: []
}
```

## 📊 Success Metrics

### Day 7 Acceptance Criteria
- [ ] Complete flow in under 2 minutes
- [ ] 3 restaurants with mock menus working
- [ ] Vibe bubbles generating plans
- [ ] Memory persists between sessions
- [ ] No crashes in 10 test runs
- [ ] Deployable to Expo Go

### Quality Bar
- Response time < 3 seconds
- UI renders at 60 fps
- Error messages user-friendly
- Offline fallback for cached data

## 🗓️ Development Milestones

### Day 0-1: Foundation
- Expo app with navigation
- Camera component
- Basic API structure

### Day 2-3: Core Features
- Bubble selector UI
- Order plan display
- Mock data integration

### Day 4-5: Intelligence
- Connect to restaurant API
- Add LLM for plans
- Basic memory system

### Day 6-7: Polish
- Error handling
- Loading states
- Demo preparation

## 📝 JavaScript-Specific Benefits

1. **Faster Development**: No compilation step, immediate feedback
2. **Easier Debugging**: Chrome DevTools, React Native Debugger
3. **Flexible Iteration**: Change logic without type refactoring
4. **Lower Barrier**: More developers can contribute
5. **Rapid Prototyping**: Perfect for 7-day sprint

## ⚡ Quick Start Commands

```bash
# Frontend (JavaScript/Expo)
npx create-expo-app mobile --template blank
cd mobile
npm install expo-camera expo-location zustand
npm install react-native-safe-area-context
npm install @react-navigation/native @react-navigation/bottom-tabs

# Run development
npx expo start
```

## 🎬 Demo Script (Day 7)

1. Open app, see warm onboarding
2. Take photo of Thai menu
3. See "Thai cuisine, usually spicy" explanation
4. Select "Comfort + Not Spicy" bubbles
5. Get 3-item order plan for 2 people
6. Rate 4 stars
7. Close app, reopen
8. System remembers "prefers mild"

## 🚨 Risk Mitigations

| Risk | Mitigation |
|------|------------|
| JS runtime errors | Extensive try-catch blocks |
| No type safety | JSDoc comments, consistent naming |
| API failures | Mock data fallbacks |
| Performance | Memoization, lazy loading |

---

*This PRD is optimized for JavaScript rapid development. Focus on working features over perfect code. Polish comes in week 2.*