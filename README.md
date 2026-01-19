# 🍜 Vibe Food App

> **Your AI-powered food ordering companion** - Take a photo, share your vibe, get the perfect order!

[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)](https://www.javascript.com/)
[![React Native](https://img.shields.io/badge/React%20Native-Expo-blue.svg)](https://expo.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python-green.svg)](https://fastapi.tiangolo.com/)
[![Status](https://img.shields.io/badge/Status-MVP%20Development-orange.svg)]()

## 🎯 Problem We're Solving

Non-native speakers and newcomers struggle with:
- 📖 Understanding unfamiliar menus
- 😰 Menu decision paralysis
- 🗣️ Knowing how to order correctly
- 🎯 Finding dishes that match their mood

## ✨ Our Solution

**Vibe Food** makes ordering simple:
1. 📸 **Capture** - Take a photo of any menu
2. 🎭 **Vibe** - Select your mood with fun bubbles
3. 📝 **Plan** - Get a personalized order plan
4. 🧠 **Remember** - App learns your preferences

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- Python 3.8+
- Expo Go app on your phone
- 10 minutes to set up

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/vibe-food-app.git
cd vibe-food-app

# 2. Setup Mobile App (JavaScript/Expo)
cd mobile
npm install
npx expo start

# 3. Setup Backend (Python/FastAPI)
cd ../backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 4. Open Expo Go on your phone and scan the QR code!
```

## 📱 Features

### Current (MVP - Week 1)
- ✅ Camera menu capture
- ✅ Location-based restaurant selection
- ✅ Vibe bubble interface
- ✅ Smart order plan generation
- ✅ Basic preference memory
- ✅ Feedback system

### Coming Soon (Week 2+)
- 🔜 Real menu OCR
- 🔜 User accounts
- 🔜 Social sharing
- 🔜 Multi-language support
- 🔜 Payment integration

## 🏗️ Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Mobile     │────▶│   Backend    │────▶│     AI       │
│  React Native│ API │   FastAPI    │ LLM │   Engines    │
│  JavaScript  │◀────│   Python     │◀────│   GPT-3.5    │
└──────────────┘     └──────────────┘     └──────────────┘
```

### Tech Stack
- **Frontend:** React Native (Expo), JavaScript, Zustand, NativeBase
- **Backend:** FastAPI, Python, SQLite, SQLAlchemy
- **AI:** OpenAI GPT-3.5, Custom Reasoning Engine
- **APIs:** Yelp Fusion, Google Places (optional)

## 🎨 UI Preview

### Main Screens
| Capture | Vibe Selection | Order Plan |
|---------|---------------|------------|
| 📸 Camera view | 🎭 Mood bubbles | 📝 Smart recommendations |
| Select restaurant | Express preferences | See order details |
| Location-based | Fun & intuitive | With ordering phrases |

## 📂 Project Structure

```
vibe-food-app/
├── mobile/                 # React Native app
│   ├── App.js             # Entry point
│   ├── src/
│   │   ├── screens/       # App screens
│   │   ├── components/    # Reusable UI
│   │   ├── services/      # API calls
│   │   └── store/         # State management
│   └── package.json
│
├── backend/               # FastAPI server
│   ├── app/
│   │   ├── main.py       # API routes
│   │   ├── engines/      # AI engines
│   │   └── models/       # Data models
│   └── requirements.txt
│
└── docs/                  # Documentation
    ├── PRD.md
    ├── TECHNICAL_SPEC.md
    └── IMPLEMENTATION_GUIDE.md
```

## 🧠 Three-Engine System

### 1. Reasoning Engine
Generates personalized order plans based on:
- Party size & hunger level
- Selected vibes
- Restaurant menu
- User memory

### 2. Reflection Engine
Learns from feedback:
- Processes ratings
- Updates preferences
- Improves future recommendations

### 3. Adaptive Memory
Remembers your preferences:
- Dietary restrictions
- Favorite dishes
- Ordering patterns

## 📊 Development Progress

### 7-Day Sprint Timeline

| Day | Focus | Status |
|-----|-------|--------|
| Day 0 | Project setup | ⏳ In Progress |
| Day 1 | Camera & Navigation | 🔜 Pending |
| Day 2 | Vibe UI | 🔜 Pending |
| Day 3 | AI Engines | 🔜 Pending |
| Day 4 | Restaurant Data | 🔜 Pending |
| Day 5 | LLM Integration | 🔜 Pending |
| Day 6 | Polish & Memory | 🔜 Pending |
| Day 7 | Testing & Demo | 🔜 Pending |

## 🧪 Testing

### Quick Test Flow
```bash
# Mobile
npm test

# Backend
pytest

# Manual Testing
# 1. Open app
# 2. Take photo of menu
# 3. Select vibes
# 4. Get recommendation
# 5. Rate experience
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
# Install pre-commit hooks
npm run setup-hooks

# Run linters
npm run lint

# Format code
npm run format
```

## 📝 API Documentation

### Core Endpoints

#### POST /capture
```javascript
// Request
{
  "image": "base64_string",
  "restaurantId": "thai_house"
}

// Response
{
  "menuContext": {
    "restaurant": "Thai House",
    "cuisine": "Thai",
    "priceLevel": "$$"
  }
}
```

#### POST /recommend
```javascript
// Request
{
  "intent": {
    "partySize": 2,
    "vibes": ["comfort", "mild"],
    "hunger": "normal"
  },
  "menuContext": {...},
  "memory": {...}
}

// Response
{
  "orderPlan": {
    "items": [...],
    "totalItems": 3,
    "estimatedCost": "$25-30"
  }
}
```

## 🐛 Known Issues

- Camera permission prompt may appear twice on iOS
- Mock data only includes 3 restaurants
- Memory resets on app reinstall (use cloud storage in v2)

## 🚀 Deployment

### Mobile (Expo)
```bash
# Build for iOS
expo build:ios

# Build for Android
expo build:android

# Publish to Expo Go
expo publish
```

### Backend (Production)
```bash
# Using Docker
docker build -t vibe-food-api .
docker run -p 8000:8000 vibe-food-api

# Using Heroku
heroku create vibe-food-api
git push heroku main
```

## 📚 Resources

- [Product Requirements Document](./PRD.md)
- [Technical Specification](./TECHNICAL_SPEC.md)
- [Implementation Guide](./IMPLEMENTATION_GUIDE.md)
- [API Documentation](./docs/API.md)
- [Design System](./docs/DESIGN.md)

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- OpenAI for GPT-3.5 API
- Expo team for amazing mobile tools
- FastAPI for blazing fast backend
- You, for trying out our app!

## 📞 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/vibe-food-app/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/vibe-food-app/discussions)
- **Email:** team@vibefood.app

---

<div align="center">

**Built with ❤️ in 7 days using JavaScript**

*Making food ordering delightful for everyone, everywhere*

[Demo](https://vibefood.app) | [Documentation](./docs) | [Contribute](CONTRIBUTING.md)

</div>