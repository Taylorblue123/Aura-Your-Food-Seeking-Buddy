# Vibe Food App - 7-Day Implementation Guide (JavaScript)
**Your day-by-day roadmap to build the MVP**

## 🎯 Project Overview
Build a food ordering companion app in 7 days using JavaScript (React Native) for rapid development.

## 🏃 Quick Start (Do This Now!)

### Step 1: Initialize Project Structure
```bash
# Create main directory
mkdir vibe-food-app && cd vibe-food-app

# Initialize Expo app (JavaScript)
npx create-expo-app mobile --template blank
cd mobile

# Install essential packages
npm install expo-camera expo-location
npm install @react-native-async-storage/async-storage
npm install zustand
npm install @react-navigation/native @react-navigation/bottom-tabs
npm install react-native-screens react-native-safe-area-context
npm install native-base react-native-svg

# Go back and setup backend
cd ..
mkdir backend && cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv openai

# Create basic structure
cd ..
mkdir -p mobile/src/{screens,components,services,store,utils,styles}
mkdir -p backend/app/{routers,engines,models,schemas,mock_data}
```

### Step 2: Create Configuration Files

#### mobile/app.json
```json
{
  "expo": {
    "name": "Vibe Food",
    "slug": "vibe-food",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "light",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "plugins": [
      "expo-camera",
      "expo-location"
    ]
  }
}
```

#### backend/.env.example
```env
OPENAI_API_KEY=your_key_here
YELP_API_KEY=your_key_here
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your_secret_key_here
```

## 📅 Day-by-Day Implementation

### Day 0: Foundation Setup ✅

#### Mobile App Structure
```javascript
// mobile/App.js
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { NativeBaseProvider } from 'native-base';
import CaptureScreen from './src/screens/CaptureScreen';
import VibeScreen from './src/screens/VibeScreen';

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NativeBaseProvider>
      <NavigationContainer>
        <Tab.Navigator>
          <Tab.Screen name="Capture" component={CaptureScreen} />
          <Tab.Screen name="Vibe" component={VibeScreen} />
        </Tab.Navigator>
      </NavigationContainer>
    </NativeBaseProvider>
  );
}
```

#### Backend API Structure
```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Vibe Food API")

# Enable CORS for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/capture")
async def capture_menu(data: dict):
    # Mock response for now
    return {
        "menuContext": {
            "restaurant": "Thai House",
            "cuisine": "Thai",
            "priceLevel": "$$"
        }
    }
```

### Day 1: Camera & Navigation 📸

#### Camera Implementation
```javascript
// mobile/src/screens/CaptureScreen.js
import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Camera } from 'expo-camera';
import * as Location from 'expo-location';

export default function CaptureScreen({ navigation }) {
  const [hasPermission, setHasPermission] = useState(null);
  const [camera, setCamera] = useState(null);

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const takePicture = async () => {
    if (camera) {
      const photo = await camera.takePictureAsync();
      // Navigate to explain screen with photo
      navigation.navigate('Vibe', { photo: photo.uri });
    }
  };

  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  return (
    <View style={styles.container}>
      <Camera
        style={styles.camera}
        type={Camera.Constants.Type.back}
        ref={ref => setCamera(ref)}
      >
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.captureButton} onPress={takePicture}>
            <Text style={styles.text}>Capture Menu</Text>
          </TouchableOpacity>
        </View>
      </Camera>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  camera: { flex: 1 },
  buttonContainer: {
    flex: 1,
    backgroundColor: 'transparent',
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'flex-end',
    paddingBottom: 40
  },
  captureButton: {
    backgroundColor: '#FF6B6B',
    padding: 20,
    borderRadius: 40
  },
  text: {
    fontSize: 18,
    color: 'white',
    fontWeight: 'bold'
  }
});
```

### Day 2: Vibe UI & State Management 🎨

#### Bubble Selector Component
```javascript
// mobile/src/components/BubbleSelector.js
import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

const VIBES = [
  { id: 'comfort', label: '🤗 Comfort', color: '#FFE5B4' },
  { id: 'adventurous', label: '🚀 Try New', color: '#E6E6FA' },
  { id: 'light', label: '🥗 Light', color: '#90EE90' },
  { id: 'hearty', label: '🍖 Hearty', color: '#FFDAB9' },
  { id: 'quick', label: '⚡ Quick', color: '#87CEEB' },
  { id: 'social', label: '👥 Sharing', color: '#FFB6C1' }
];

export default function BubbleSelector({ selected, onSelect }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>What's your vibe?</Text>
      <View style={styles.bubbleContainer}>
        {VIBES.map(vibe => (
          <TouchableOpacity
            key={vibe.id}
            style={[
              styles.bubble,
              { backgroundColor: vibe.color },
              selected.includes(vibe.id) && styles.selected
            ]}
            onPress={() => onSelect(vibe.id)}
          >
            <Text style={styles.bubbleText}>{vibe.label}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  bubbleContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between'
  },
  bubble: {
    width: '45%',
    padding: 20,
    borderRadius: 20,
    marginBottom: 15,
    alignItems: 'center'
  },
  selected: {
    borderWidth: 3,
    borderColor: '#333'
  },
  bubbleText: { fontSize: 16 }
});
```

#### State Management
```javascript
// mobile/src/store/useStore.js
import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const useStore = create((set, get) => ({
  // State
  intent: {
    partySize: 2,
    hunger: 'normal',
    vibes: [],
    budget: '$'
  },
  orderPlan: null,
  userMemory: {
    allergies: [],
    preferences: [],
    lastOrders: []
  },

  // Actions
  setVibes: (vibes) => set(state => ({
    intent: { ...state.intent, vibes }
  })),

  generatePlan: async () => {
    const { intent, userMemory } = get();

    // Call API (mock for now)
    const mockPlan = {
      items: [
        { name: 'Pad Thai', reason: 'Mild and comforting' },
        { name: 'Spring Rolls', reason: 'Light appetizer to share' },
        { name: 'Mango Sticky Rice', reason: 'Sweet ending' }
      ]
    };

    set({ orderPlan: mockPlan });
  }
}));
```

### Day 3: Three Engines Implementation 🧠

#### Backend Engines
```python
# backend/app/engines/reasoning.py
class ReasoningEngine:
    def generate_plan(self, intent, menu_context, memory):
        """Generate order plan based on intent and context"""

        # Simple heuristic for MVP
        plan_items = []

        # Base on party size
        num_items = {
            1: 1,
            2: 3,
            3: 4,
            4: 5
        }.get(intent.get('partySize', 2), 3)

        # Match vibes to menu items
        if 'comfort' in intent.get('vibes', []):
            plan_items.append({
                'name': 'Pad Thai',
                'reason': 'Classic comfort dish',
                'orderPhrase': 'Pad Thai, mild please'
            })

        if 'adventurous' in intent.get('vibes', []):
            plan_items.append({
                'name': 'Som Tam',
                'reason': 'Bold flavors to explore',
                'orderPhrase': 'Green papaya salad'
            })

        return {
            'planType': 'share' if intent['partySize'] > 1 else 'solo',
            'items': plan_items,
            'totalItems': len(plan_items),
            'confidence': 0.8
        }

# backend/app/engines/reflection.py
class ReflectionEngine:
    def process_feedback(self, feedback, order_plan):
        """Convert feedback into memory updates"""

        memory_patch = {
            'updates': [],
            'confidence': 0.7
        }

        if feedback['rating'] >= 4:
            # Add to preferences
            for item in order_plan['items']:
                memory_patch['updates'].append({
                    'action': 'add_preference',
                    'value': item['name']
                })
        elif feedback['rating'] <= 2:
            # Add to avoid list
            for item in order_plan['items']:
                memory_patch['updates'].append({
                    'action': 'add_avoid',
                    'value': item['name']
                })

        return memory_patch

# backend/app/engines/memory.py
import json
from typing import Dict, List

class AdaptiveMemory:
    def __init__(self):
        self.storage = {}  # In-memory for MVP

    def get_memory(self, device_id: str) -> Dict:
        """Get user memory by device ID"""
        return self.storage.get(device_id, {
            'allergies': [],
            'preferences': [],
            'avoidList': []
        })

    def update_memory(self, device_id: str, patch: Dict):
        """Apply memory patch"""
        memory = self.get_memory(device_id)

        for update in patch.get('updates', []):
            if update['action'] == 'add_preference':
                memory['preferences'].append(update['value'])
            elif update['action'] == 'add_avoid':
                memory['avoidList'].append(update['value'])

        self.storage[device_id] = memory
        return memory
```

### Day 4: Restaurant Integration 🍽️

#### Mock Restaurant Data
```javascript
// mobile/src/utils/mockData.js
export const MOCK_RESTAURANTS = [
  {
    id: 'thai_house',
    name: 'Thai House',
    cuisine: 'Thai',
    distance: '0.3 mi',
    rating: 4.5,
    priceLevel: '$$',
    image: 'https://via.placeholder.com/300',
    menuHighlights: [
      { name: 'Pad Thai', price: '$12', tags: ['mild', 'noodles'] },
      { name: 'Green Curry', price: '$14', tags: ['spicy', 'coconut'] },
      { name: 'Som Tam', price: '$10', tags: ['fresh', 'spicy'] }
    ]
  },
  {
    id: 'burger_joint',
    name: 'Burger Joint',
    cuisine: 'American',
    distance: '0.5 mi',
    rating: 4.2,
    priceLevel: '$',
    image: 'https://via.placeholder.com/300',
    menuHighlights: [
      { name: 'Classic Burger', price: '$9', tags: ['comfort', 'hearty'] },
      { name: 'Veggie Burger', price: '$8', tags: ['vegetarian', 'light'] },
      { name: 'Fries', price: '$4', tags: ['side', 'crispy'] }
    ]
  },
  {
    id: 'sushi_spot',
    name: 'Sushi Spot',
    cuisine: 'Japanese',
    distance: '0.7 mi',
    rating: 4.7,
    priceLevel: '$$$',
    image: 'https://via.placeholder.com/300',
    menuHighlights: [
      { name: 'Salmon Roll', price: '$15', tags: ['fresh', 'light'] },
      { name: 'Tempura', price: '$12', tags: ['crispy', 'warm'] },
      { name: 'Miso Soup', price: '$4', tags: ['warm', 'light'] }
    ]
  }
];
```

### Day 5: LLM Integration 🤖

#### API Integration
```javascript
// mobile/src/services/api.js
const API_BASE = __DEV__ ? 'http://localhost:8000' : 'https://api.vibefood.app';

class ApiService {
  async generateRecommendation(intent, restaurantId, userMemory) {
    try {
      const response = await fetch(`${API_BASE}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          intent,
          restaurantId,
          memory: userMemory
        })
      });

      if (!response.ok) throw new Error('API Error');
      return await response.json();
    } catch (error) {
      // Fallback to mock
      return this.getMockRecommendation(intent);
    }
  }

  getMockRecommendation(intent) {
    // Smart mock based on vibes
    const plans = {
      comfort: [
        { name: 'Pad Thai', reason: 'Classic comfort' },
        { name: 'Spring Rolls', reason: 'Light starter' }
      ],
      adventurous: [
        { name: 'Som Tam', reason: 'Bold and spicy' },
        { name: 'Larb', reason: 'Unique flavors' }
      ],
      light: [
        { name: 'Tom Yum Soup', reason: 'Light and flavorful' },
        { name: 'Fresh Rolls', reason: 'Healthy option' }
      ]
    };

    const vibe = intent.vibes[0] || 'comfort';
    return {
      orderPlan: {
        items: plans[vibe] || plans.comfort,
        totalItems: 2,
        estimatedCost: '$25-30'
      }
    };
  }
}

export default new ApiService();
```

### Day 6: Polish & Memory 💫

#### Order Plan Display
```javascript
// mobile/src/components/OrderPlanCard.js
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

export default function OrderPlanCard({ plan, onFeedback }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Your Perfect Order</Text>

      {plan.items.map((item, index) => (
        <View key={index} style={styles.item}>
          <Text style={styles.itemName}>{item.name}</Text>
          <Text style={styles.reason}>{item.reason}</Text>
          <Text style={styles.orderPhrase}>
            Say: "{item.orderPhrase || item.name}"
          </Text>
        </View>
      ))}

      <View style={styles.summary}>
        <Text style={styles.summaryText}>
          {plan.totalItems} items • {plan.estimatedCost}
        </Text>
      </View>

      <TouchableOpacity style={styles.feedbackButton} onPress={onFeedback}>
        <Text style={styles.buttonText}>How was it?</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 20,
    margin: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    color: '#333'
  },
  item: {
    borderLeftWidth: 3,
    borderLeftColor: '#FF6B6B',
    paddingLeft: 15,
    marginBottom: 20
  },
  itemName: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 5
  },
  reason: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5
  },
  orderPhrase: {
    fontSize: 14,
    color: '#FF6B6B',
    fontStyle: 'italic'
  },
  summary: {
    borderTopWidth: 1,
    borderTopColor: '#eee',
    paddingTop: 15,
    marginTop: 15
  },
  summaryText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center'
  },
  feedbackButton: {
    backgroundColor: '#FF6B6B',
    padding: 15,
    borderRadius: 10,
    marginTop: 20
  },
  buttonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center'
  }
});
```

### Day 7: Testing & Demo 🚀

#### Testing Checklist
```javascript
// mobile/src/__tests__/testChecklist.js
const TEST_SCENARIOS = [
  {
    name: "Happy Path - Solo Diner",
    steps: [
      "Open app",
      "Take photo of menu",
      "Select 'Light' vibe",
      "Get 1-2 item recommendation",
      "Rate 5 stars"
    ]
  },
  {
    name: "Group Dining",
    steps: [
      "Select 3 people",
      "Choose 'Social' + 'Hearty' vibes",
      "Get 4-5 shareable items",
      "Verify sharing logic"
    ]
  },
  {
    name: "Memory Test",
    steps: [
      "Rate meal 2 stars",
      "Close app",
      "Reopen app",
      "Verify items avoided in next recommendation"
    ]
  }
];

// Run through each scenario manually
export function runTests() {
  console.log("=== Manual Test Scenarios ===");
  TEST_SCENARIOS.forEach(scenario => {
    console.log(`\n${scenario.name}:`);
    scenario.steps.forEach((step, i) => {
      console.log(`  ${i + 1}. ${step}`);
    });
  });
}
```

## 🎯 Success Metrics

### MVP Completion Criteria
- [ ] Camera captures photo
- [ ] 3 restaurants available
- [ ] 6 vibe bubbles working
- [ ] Order plans generate
- [ ] Memory persists
- [ ] No crashes in demo

## 🚨 Common Issues & Solutions

### Issue: Expo Camera not working
```javascript
// Fix: Ensure permissions in app.json
"plugins": [
  [
    "expo-camera",
    {
      "cameraPermission": "Allow $(PRODUCT_NAME) to access your camera."
    }
  ]
]
```

### Issue: API connection failed
```javascript
// Fix: Use ngrok for testing
// Terminal: ngrok http 8000
// Update API_BASE to ngrok URL
```

### Issue: State not persisting
```javascript
// Fix: Check AsyncStorage
const debugStorage = async () => {
  const keys = await AsyncStorage.getAllKeys();
  const items = await AsyncStorage.multiGet(keys);
  console.log('Storage:', items);
};
```

## 📱 Demo Script

```javascript
// Day 7 Demo Flow
1. "Hi! Let me show you Vibe Food - your personal food ordering assistant"
2. "First, I'll take a photo of this Thai menu" [CAPTURE]
3. "The app instantly understands this is Thai cuisine" [EXPLAIN]
4. "Now I'll tell it my vibe - I'm feeling comfort food today" [SELECT BUBBLES]
5. "And just like that, it recommends the perfect order for 2 people" [SHOW PLAN]
6. "It even tells me exactly how to order in a way the staff understands"
7. "After my meal, I rate it" [FEEDBACK]
8. "Next time, it remembers my preferences and gets even better"
9. "Built in just 7 days with JavaScript!"
```

## 🎉 Final Checklist

### Before Demo
- [ ] Test on real device
- [ ] Clear AsyncStorage
- [ ] Prepare 3 restaurant menus
- [ ] Practice demo flow 3x
- [ ] Backup APK/IPA ready
- [ ] Hotspot for API connection

### During Demo
- [ ] Start with problem statement
- [ ] Show real menu photo
- [ ] Emphasize speed (< 30 seconds)
- [ ] Show memory working
- [ ] End with technical achievements

---

**Remember:** This is a prototype to validate the concept. Focus on the magic moment when a photo becomes a personalized order plan. Everything else is secondary.

*Good luck! You've got this! 🚀*