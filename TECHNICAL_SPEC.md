# Vibe Food App - Technical Specification (JavaScript)
**Stack:** React Native (Expo) + FastAPI + SQLite
**Language:** JavaScript (Frontend) + Python (Backend)
**Timeline:** 7-Day MVP Sprint

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────┐
│                  Mobile App                      │
│              Expo/React Native/JS                │
│    ┌────────────────────────────────────┐       │
│    │          Presentation Layer        │       │
│    │    Screens, Components, Navigation │       │
│    └────────────────────────────────────┘       │
│    ┌────────────────────────────────────┐       │
│    │           State Layer              │       │
│    │        Zustand Store, Hooks        │       │
│    └────────────────────────────────────┘       │
│    ┌────────────────────────────────────┐       │
│    │          Service Layer             │       │
│    │      API Client, AsyncStorage      │       │
│    └────────────────────────────────────┘       │
└─────────────────────────────────────────────────┘
                         ↕ HTTP/JSON
┌─────────────────────────────────────────────────┐
│                  Backend API                     │
│                FastAPI/Python                    │
│    ┌────────────────────────────────────┐       │
│    │           API Layer                │       │
│    │      Routers, Request Handlers     │       │
│    └────────────────────────────────────┘       │
│    ┌────────────────────────────────────┐       │
│    │          Engine Layer              │       │
│    │   Reasoning, Reflection, Memory    │       │
│    └────────────────────────────────────┘       │
│    ┌────────────────────────────────────┐       │
│    │           Data Layer               │       │
│    │      SQLite, External APIs         │       │
│    └────────────────────────────────────┘       │
└─────────────────────────────────────────────────┘
```

## 📱 Frontend Architecture (JavaScript/Expo)

### Directory Structure
```
mobile/
├── App.js                      // Entry point, navigation setup
├── app.json                    // Expo configuration
├── babel.config.js             // Babel configuration
├── package.json                // Dependencies
├── assets/                     // Images, fonts
│   ├── images/
│   └── fonts/
├── src/
│   ├── screens/               // Screen components
│   │   ├── OnboardingScreen.js
│   │   ├── CaptureScreen.js
│   │   ├── ExplainScreen.js
│   │   ├── VibeScreen.js
│   │   ├── PlanScreen.js
│   │   └── FeedbackScreen.js
│   ├── components/            // Reusable components
│   │   ├── common/
│   │   │   ├── Button.js
│   │   │   ├── Card.js
│   │   │   └── LoadingSpinner.js
│   │   ├── capture/
│   │   │   ├── CameraView.js
│   │   │   └── RestaurantPicker.js
│   │   ├── vibe/
│   │   │   ├── BubbleSelector.js
│   │   │   ├── ChatInput.js
│   │   │   └── VibeButton.js
│   │   └── plan/
│   │       ├── OrderPlanCard.js
│   │       ├── DishItem.js
│   │       └── FeedbackModal.js
│   ├── navigation/            // Navigation configuration
│   │   └── AppNavigator.js
│   ├── services/              // API and external services
│   │   ├── api.js            // API client
│   │   ├── storage.js        // AsyncStorage wrapper
│   │   └── location.js       // Location services
│   ├── store/                // State management
│   │   ├── useStore.js       // Zustand store
│   │   └── slices/
│   │       ├── userSlice.js
│   │       ├── restaurantSlice.js
│   │       └── orderSlice.js
│   ├── utils/                // Utilities
│   │   ├── constants.js
│   │   ├── helpers.js
│   │   └── mockData.js
│   └── styles/               // Styling
│       ├── colors.js
│       ├── typography.js
│       └── spacing.js
```

### Key JavaScript Components

#### Main App Entry (App.js)
```javascript
import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { NativeBaseProvider } from 'native-base';
import AppNavigator from './src/navigation/AppNavigator';
import { useStore } from './src/store/useStore';

export default function App() {
  const initializeApp = useStore(state => state.initializeApp);

  useEffect(() => {
    initializeApp();
  }, []);

  return (
    <NativeBaseProvider>
      <NavigationContainer>
        <AppNavigator />
      </NavigationContainer>
    </NativeBaseProvider>
  );
}
```

#### State Management (Zustand)
```javascript
// src/store/useStore.js
import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

const useStore = create((set, get) => ({
  // User state
  user: {
    deviceId: null,
    memory: {
      allergies: [],
      preferences: [],
      avoidList: []
    }
  },

  // Restaurant state
  currentRestaurant: null,
  menuContext: null,

  // Order state
  intent: {
    partySize: 1,
    hunger: 'normal',
    vibes: [],
    budget: '$'
  },
  orderPlan: null,

  // Actions
  setIntent: (intent) => set({ intent }),
  setOrderPlan: (plan) => set({ orderPlan: plan }),
  updateMemory: async (memory) => {
    set(state => ({
      user: { ...state.user, memory }
    }));
    await AsyncStorage.setItem('userMemory', JSON.stringify(memory));
  },

  initializeApp: async () => {
    const deviceId = await AsyncStorage.getItem('deviceId');
    const memory = await AsyncStorage.getItem('userMemory');
    set({
      user: {
        deviceId: deviceId || `device_${Date.now()}`,
        memory: memory ? JSON.parse(memory) : get().user.memory
      }
    });
  }
}));

export { useStore };
```

#### API Service Layer
```javascript
// src/services/api.js
const API_BASE = 'http://localhost:8000';

class ApiService {
  async post(endpoint, data) {
    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API call failed:', error);
      // Return mock data as fallback
      return this.getMockResponse(endpoint);
    }
  }

  getMockResponse(endpoint) {
    // Fallback mock responses for development
    const mocks = {
      '/capture': { status: 'success', menuContext: mockMenuData },
      '/recommend': { orderPlan: mockOrderPlan },
      '/feedback': { status: 'recorded' }
    };
    return mocks[endpoint] || {};
  }

  // API Methods
  async captureMenu(imageBase64, restaurantId) {
    return this.post('/capture', { image: imageBase64, restaurantId });
  }

  async generateRecommendation(intent, menuContext, memory) {
    return this.post('/recommend', { intent, menuContext, memory });
  }

  async submitFeedback(feedback, orderPlan) {
    return this.post('/feedback', { feedback, orderPlan });
  }
}

export default new ApiService();
```

## 🔧 Backend Architecture (FastAPI/Python)

### Directory Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configuration
│   ├── database.py             # Database setup
│   ├── routers/                # API endpoints
│   │   ├── __init__.py
│   │   ├── capture.py
│   │   ├── recommend.py
│   │   └── feedback.py
│   ├── engines/                # Three AI engines
│   │   ├── __init__.py
│   │   ├── reasoning.py
│   │   ├── reflection.py
│   │   └── memory.py
│   ├── models/                 # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── order.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── intent.py
│   │   └── order_plan.py
│   └── mock_data/              # Test data
│       ├── restaurants.json
│       └── menus.json
├── requirements.txt
├── .env.example
└── run.py                      # Development server
```

### API Endpoints

```python
# Endpoint specifications
POST /capture
  Request: { image: string, restaurantId?: string }
  Response: { menuContext: MenuContext }

POST /recommend
  Request: { intent: Intent, menuContext: MenuContext, memory: Memory }
  Response: { orderPlan: OrderPlan }

POST /feedback
  Request: { feedback: Feedback, orderPlan: OrderPlan }
  Response: { status: string, memoryUpdate?: MemoryPatch }

GET /restaurants/nearby
  Request: { lat: number, lng: number }
  Response: { restaurants: Restaurant[] }
```

## 💾 Data Models

### JavaScript Models (Frontend)
```javascript
// Intent Model
const Intent = {
  partySize: 1,        // 1-5+
  hunger: "normal",    // "light" | "normal" | "very_hungry"
  vibes: [],          // Array of strings
  budget: "$",        // "$" | "$$" | "$$$"
  constraints: {
    allergies: [],    // Array of strings
    avoidList: [],    // Array of strings
    spiceMax: 2       // 0-3 scale
  },
  diningStyle: "solo" // "solo" | "share" | "combo"
};

// Order Plan Model
const OrderPlan = {
  planId: "plan_123",
  planType: "share",
  items: [
    {
      name: "Pad Thai",
      category: "main",
      reason: "Mild and comfort food",
      orderPhrase: "Pad Thai, mild spice please",
      alternatives: ["Pad See Ew"]
    }
  ],
  servingLogic: "Good for sharing between 2 people",
  totalItems: 3,
  estimatedCost: "$25-30",
  confidence: 0.85
};

// Memory Model
const Memory = {
  deviceId: "device_123",
  hardConstraints: [],     // Allergies, strict avoids
  softPreferences: [],     // Cuisine preferences
  contextualHabits: [],    // Dining patterns
  lastUpdated: Date.now()
};
```

### Python Models (Backend)
```python
# Pydantic schemas for validation
from pydantic import BaseModel
from typing import List, Optional

class Intent(BaseModel):
    party_size: int
    hunger: str
    vibes: List[str]
    budget: str
    constraints: dict

class OrderPlan(BaseModel):
    plan_id: str
    plan_type: str
    items: List[dict]
    serving_logic: str
    total_items: int
    estimated_cost: str
    confidence: float
```

## 🚀 Development Workflow

### Day 0 Setup Commands
```bash
# 1. Frontend Setup (JavaScript/Expo)
npx create-expo-app mobile --template blank
cd mobile
npm install expo-camera expo-location @react-native-async-storage/async-storage
npm install zustand react-native-safe-area-context
npm install @react-navigation/native @react-navigation/bottom-tabs
npm install native-base react-native-svg react-native-safe-area-context

# 2. Backend Setup (Python/FastAPI)
cd ..
mkdir backend && cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv
pip install openai requests

# 3. Run Development Servers
# Terminal 1 - Backend
cd backend && uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd mobile && npx expo start
```

### Mock Data Structure
```javascript
// src/utils/mockData.js
export const mockRestaurants = [
  {
    id: "thai_house",
    name: "Thai House",
    cuisine: "Thai",
    priceLevel: "$$",
    distance: "0.3 mi",
    rating: 4.5,
    menuItems: [
      {
        id: "pad_thai",
        name: "Pad Thai",
        category: "noodles",
        price: 12.95,
        spiceLevel: 1,
        tags: ["popular", "mild", "sweet"],
        description: "Stir-fried rice noodles with egg, bean sprouts"
      }
      // ... more items
    ]
  }
  // ... more restaurants
];

export const mockVibes = [
  { id: "comfort", label: "Comfort", emoji: "🤗" },
  { id: "adventurous", label: "Adventurous", emoji: "🚀" },
  { id: "light", label: "Light", emoji: "🥗" },
  { id: "hearty", label: "Hearty", emoji: "🍖" },
  { id: "quick", label: "Quick", emoji: "⚡" },
  { id: "social", label: "Social", emoji: "👥" }
];
```

## 🎯 Performance Requirements

- App launch: < 2 seconds
- Camera capture: < 1 second
- API response: < 3 seconds
- Navigation transitions: 60 fps
- Memory usage: < 200MB

## 🔒 Security Considerations

1. **API Keys**: Store in `.env`, never in JavaScript code
2. **Device ID**: Use expo-secure-store for sensitive data
3. **Input Validation**: Sanitize all user inputs
4. **HTTPS**: Use HTTPS in production (HTTP ok for local dev)
5. **Rate Limiting**: Implement basic rate limiting on backend

## 📋 Testing Strategy (Simplified for MVP)

### Manual Testing Checklist
- [ ] Camera permission request works
- [ ] Location permission request works
- [ ] Can capture photo
- [ ] Can select restaurant
- [ ] Bubble selection updates state
- [ ] Order plan displays correctly
- [ ] Feedback saves to memory
- [ ] App works offline with cached data
- [ ] No crashes in 10 consecutive runs

## 🚢 Deployment (Day 7)

### Mobile App
```bash
# Build for Expo Go (easiest for demo)
expo publish

# Share via QR code or Expo link
# No app store submission needed for MVP
```

### Backend
```bash
# Option 1: Local demo (easiest)
# Just run on laptop during demo

# Option 2: Deploy to Render/Railway (free tier)
# Push to GitHub and connect to service
```

---

*This technical spec prioritizes simplicity and speed. JavaScript on frontend allows rapid iteration. Focus on getting features working, optimize later.*