# Product Requirements Document (PRD) - Evidence-Safe MVP Edition

## Aura: Mood-Based Food Recommendation MVP

### 🎯 Purpose & Core Hypothesis

**H1: Users will trust AI food recommendations based on their mood/context enough to follow at least one suggested dish.**

This is our riskiest assumption because:
- Users must map abstract moods to concrete food choices
- Trust in algorithm over personal menu browsing is unproven
- Real-time decision-making at restaurants adds pressure

**Why this matters:** Research shows mood correlates with food preferences, and AI personalization can enhance decision confidence when properly calibrated with user trust signals.

### 👤 Target User & Scenarios

**Primary User**: International students and young professionals (22-35) navigating unfamiliar menus

**Concrete Scenarios**:
1. **Lunch Rush**: Alex at Thai restaurant, 10 minutes to order, overwhelmed by 50+ unfamiliar items
2. **Group Dinner**: Sam coordinating for 4 friends with different preferences and dietary needs
3. **First Visit**: User new to cuisine type, doesn't recognize most dish names

**Assumptions to Validate**:
- Users experience decision fatigue with unfamiliar menus → Validate via user interviews pre-MVP
- Mood correlates with food preferences → Validate via MVP swipe data analysis
- 90-second decision time improves satisfaction → Track via timestamps + post-order NPS

### 📦 MVP Scope (7-Day Sprint)

#### IN SCOPE ✅

**Core Flow**:
- 3 screens: Capture+Vibe → Plan → Success
- Camera menu capture (real integration)
- 6-8 vibe bubbles for mood selection
- 3-5 swipeable dish cards with reasoning
- Binary feedback (picked/skipped)
- Success celebration and learning summary

**Frontend MVP**:
- React Native + TypeScript
- Camera call to scan menu (system camera integration)
- Logical flow between screens and states
- Data flow (image upload → vibe options → dish options)
- Component implementation (cards, bubbles, progress indicators)
- Basic animations (swipe, tap, transitions)

**Backend MVP**:
- FastAPI routers and endpoints for:
  - Image upload and processing (Google Vision OCR API)
  - Vibe option generation (static for v1.0, contextual for v1.1)
  - Dish recommendation endpoint (GPT-4 with structured output)
  - Feedback collection and preference updates

**LLM Engine MVP**:
- Basic prompt engineering for dish recommendations
- Structured JSON input/output
- Reasoning generation for each recommendation

**Technical**:
- Real menu capture via Google Cloud Vision OCR
- LLM reasoning engine (GPT-4) for recommendations
- Local storage for basic preferences (SQLite)
- 10 test users for validation

**Team**:
- UIUX/Frontend: Wenxuan
- Backend/LLM: Kai
- Daily standups at 11am
- Integration test: Saturday 9pm

#### OUT OF SCOPE ❌
- User accounts/authentication
- Real restaurant APIs
- Payment processing
- Delivery logistics
- Social features
- Multi-language support
- Complex dietary restrictions beyond basic allergies
- Restaurant partnerships
- Performance optimization (Redis, caching)
- Advanced analytics

### 🔄 Core UX Flow (MVP)

```
1. CAPTURE (10s)
   Input: Camera photo of menu
   Output: Menu items extracted via OCR
   Error Path: OCR fail → ERROR RECOVERY SCREEN

1.1 ERROR RECOVERY SCREEN (When OCR fails)
   Display: "Oops! We couldn't read that menu 😅"
   Message: "The lighting or angle might be tricky. Let's try again!"
   Options:
   - [Try Another Photo] → Return to camera (primary action)
   - [Get Help] → Tips screen showing good photo examples
   Success: User retakes photo with better quality

2. VIBE SELECTION (15s)
   Input: Tap 1-3 vibe bubbles + party size
   Output: Intent object {vibes, size, constraints}
   Error: No selection → Show "Pick your mood" nudge

3. RECOMMENDATION (5s)
   Input: Intent + Menu items from OCR
   Output: 3-5 dish cards with reasoning from LLM
   Error: Low confidence → Show top dishes + "Explore menu"

4. CONFIRMATION (10s)
   Input: Swipe right (pick) or left (skip) on cards
   Output: "I'll order these" list
   Completion: At least 1 dish selected

5. FEEDBACK (5s)
   Input: Quick rating + optional issue tags
   Output: Stored preference update
   Learning: Collected for future adaptive memory (v1.1)
```

### 🗺️ User Journey (Comprehensive)

#### High-Level Journey Architecture

```
User Journey Phases:
├─ Discovery & Installation (Pre-Launch)
├─ First-Time Experience (Onboarding)
├─ Core Experience Loop (Main Flow)
├─ Return Experiences (Retention)
├─ Error Recovery (Resilience)
└─ Advanced Usage (Power Features)
```

#### The 90-Second Promise Flow

```
CAPTURE (30 sec) → VIBE (30 sec) → PLAN (30 sec)
     ↓                  ↓               ↓
"I see a menu"   "This is my mood"  "Perfect order!"
     ↓                  ↓               ↓
   [Success: 70%]   [Success: 85%]   [Success: 75%]
```

#### Complete User State Map

```javascript
// Comprehensive State Decision Logic
function determineUserJourney(user, context, device) {
  // Pre-Launch States
  if (!user.appInstalled) {
    if (context.referralSource === 'friend') return 'SOCIAL_LANDING';
    if (context.searchIntent === 'menu_help') return 'PROBLEM_AWARE_LANDING';
    return 'DISCOVERY_LANDING';
  }

  // First Launch Decision Tree
  if (user.isFirstLaunch) {
    if (context.hasNotificationPermission === false) return 'PERMISSION_REQUEST';
    if (user.skippedOnboarding) return 'SIMPLIFIED_CAPTURE';
    return 'WELCOME_ONBOARDING';
  }

  // Return User States
  if (user.lastSessionAbandoned) {
    if (user.abandonPoint === 'onboarding') return 'ONBOARDING_RECOVERY';
    if (user.abandonPoint === 'vibe_selection') return 'SIMPLIFIED_FLOW';
    return 'WIN_BACK_FLOW';
  }

  // Contextual Quick Actions
  if (user.lastOrderTime < 4_HOURS &&
      (context.sameRestaurant || context.nearbyRestaurant)) {
    return 'QUICK_REORDER';
  }

  // Time-Based Returns
  const hoursSinceLastUse = Date.now() - user.lastActiveTime;
  if (hoursSinceLastUse < 24) return 'SAME_DAY_RETURN';
  if (hoursSinceLastUse < 168) return 'WEEKLY_RETURN';  // 7 days
  if (hoursSinceLastUse < 720) return 'MONTHLY_RETURN'; // 30 days
  if (hoursSinceLastUse > 720) return 'REACTIVATION';

  // Power User Recognition
  if (user.totalOrders >= 10) return 'EXPERT_MODE';
  if (user.totalOrders >= 5) return 'POWER_DASHBOARD';
  if (user.totalOrders >= 3) return 'EMERGING_POWER_USER';

  // Default States
  return 'SMART_CAPTURE_HUB';
}
```

#### Detailed Journey Maps

**Journey A: First-Time User**

```
Phase 1: Welcome Onboarding (20 seconds)
├─ Screen 1: Value Promise (5 sec)
│  ├─ Animated logo "Never eat alone in confusion"
│  ├─ 90-second promise badge
│  └─ Continue
│
└─ Screen 2: Quick Setup (15 sec)
   ├─ Spice tolerance (None/Mild/Hot)
   ├─ Allergies (optional), offer some common allergies option
   └─ Cuisine Preference
   └─ "Let's eat!" → Smart Capture Hub
```

**Journey B: Returning User (Default)**

```
Phase 1: Smart Capture Hub (Immediate)
├─ Personalized greeting (time-aware, weather-aware, and location-aware)
├─ Camera card (primary action)
├─ Nearby restaurants (if location on)
├─ Recent order journy (collapsed), empahize historical "taste mood" and meal choices
└─ One-tap to capture or select
```

**Journey C: Quick Reorder (Contextual)**

```
Triggers: Recent order (<4hr) + Same/nearby restaurant
Phase 1: Instant Reorder (5 seconds)
├─ Location-aware greeting ("You're at Thai House again!")
├─ Last order preview card
├─ One-tap reorder button
└─ Alternatives: New vibes or different restaurant
```

**Phase 2: Core Flow (All Users)**

```
This is a vitial part that needs further examination by A/B tests and discussion
Vibe Selection (30 seconds)
├─ 9 contextual bubbles (emoji-based)
├─ bubbles content generated by contextual and persona information (time, location, weather, historical preference)
├─ Time-aware options (lunch = quick)
├─ Party size selector
├─ Auto-proceeds at 3 selections
└─ Generates intent in <500ms

Order Plan (30 seconds)
├─ Header to provide brief summary of order plan
├─ 3-5 swipeable dish cards
├─ Story-driven presentation
├─ Swipe right to love (green glow)
├─ Swipe left to reject (red fade)
├─ Reasoning for each choice
└─ Brief Summary and Celebration on completion
└─ Tolerance mechanism for giving feedback (contextual option) and plan regeneration
└─ Automatically adapts feedback to memory
```

### 🎭 Vibe System v1

**8 Core Vibes** (based on mood-food correlation research):

| Vibe | Emoji | Intent | Dish Attributes | Example Dishes |
|------|-------|---------|-----------------|----------------|
| **Comfort** | 😌 | Familiar, warm | Creamy, carbs, mild | Pad Thai, Margherita Pizza |
| **Adventure** | 🔥 | Try new things | Unique, authentic, bold | Tom Yum, Mole Negro |
| **Light** | 🥗 | Not heavy | Fresh, vegetables, grilled | Som Tam, Caprese Salad |
| **Quick** | ⚡ | Fast eating | Single dish, handheld | Tacos, Panini |
| **Sharing** | 👥 | Group friendly | Platters, appetizers | Nachos, Antipasto |
| **Budget** | 💰 | Cost conscious | Under $15, filling | Rice bowls, Pasta |
| **Healthy** | 💪 | Nutritious | Protein, whole grains | Grilled chicken, Quinoa bowl |
| **Indulgent** | 🎉 | Treat yourself | Rich, desserts, fried | Lasagna, Churros |

**Disambiguation Rules**:
- Max 3 vibes selected
- Conflicts resolved by selection order (first = primary)
- Time context auto-suggests (lunch → Quick)
- Party size affects suggestions (>2 → Sharing appears)

### 📊 Feedback System v1

**Immediate Feedback** (post-order):
```javascript
{
  orderId: "uuid",
  pickedDishes: ["Pad Thai", "Spring Rolls"],
  skippedDishes: ["Tom Yum"],
  issues: ["too_spicy", "portion_small"], // optional
  wouldOrderAgain: true // simple yes/no
}
```

**Preference Updates**:
- Picked → Increase vibe-dish correlation weight (+0.2)
- Skipped → Decrease weight (-0.1)
- Issues → Add constraints (e.g., "too_spicy" → reduce spice tolerance)
- Stored locally in UserPreference object

### 📈 Success Metrics & Experiment Plan

**Primary Metric**:
- **Recommendation Acceptance Rate**: ≥40% pick at least 1 suggested dish

**Secondary Metrics**:
- Time to decision: <90 seconds (track via timestamps)
- Completion rate: >60% reach confirmation screen
- Return usage: >30% use app twice in 7 days
- Trust indicator: >50% select ≥2 recommended dishes

**MVP Experiment Design** (10 test users, 7 days):
- Day 1-2: Onboarding + first order
- Day 3-5: Return usage tracking
- Day 6-7: Exit interviews
- Success criteria: 4/10 users order recommended dish

**Instrumentation Events**:

| Event Name | When Fired | Properties |
|------------|------------|------------|
| `app_opened` | App launch | `{timestamp, returning_user}` |
| `menu_captured` | Photo taken/restaurant selected | `{method: "camera"/"manual", restaurant_id}` |
| `vibe_selected` | Vibe bubble tapped | `{vibe_type, selection_order, total_selected}` |
| `recommendation_generated` | API returns dishes | `{latency_ms, num_dishes, confidence_score}` |
| `dish_swiped` | Card swiped | `{dish_name, direction: "right"/"left", time_to_swipe}` |
| `order_confirmed` | User confirms selection | `{num_picked, num_skipped, total_time_seconds}` |
| `feedback_submitted` | Post-order rating | `{rating, issues[], would_order_again}` |

### 🏗️ Technical Specification (MVP)

#### Architecture
```
┌─────────────────────────┐
│   React Native App      │
│   (Expo + TypeScript)   │
└───────────┬─────────────┘
            │ HTTPS
┌───────────▼─────────────┐
│   FastAPI Backend       │
│   /api/v1/*             │
└───────────┬─────────────┘
            │
┌───────────▼─────────────┐
│   Services Layer        │
├─────────────────────────┤
│ • OCR Service (Google)  │
│ • LLM Service (OpenAI)  │
│ • Storage (SQLite)      │
└─────────────────────────┘
```

#### Data Models

```typescript
// Core entities
interface MenuItem {
  id: string;
  name: string;
  description?: string;
  price?: number;
  ingredients?: string[]; // for allergen checking
  tags?: string[]; // "spicy", "vegetarian", etc.
}

interface VibeIntent {
  vibes: string[]; // ["comfort", "budget"]
  partySize: number;
  constraints: {
    allergies: string[]; // ["nuts", "dairy"]
    maxSpice: number; // 1-3 scale
  };
  context: {
    timeOfDay: string; // "lunch", "dinner"
    restaurant: string;
  };
}

interface Recommendation {
  dishId: string;
  dishName: string;
  reasoning: string; // "Mild and shareable, perfect for your group"
  confidence: number; // 0-1
  rank: number;
}

interface UserFeedback {
  sessionId: string;
  timestamp: number;
  picked: string[];
  skipped: string[];
  issues?: string[];
  wouldOrderAgain?: boolean;
}

interface UserPreference {
  userId: string; // device ID for MVP
  vibeWeights: Record<string, Record<string, number>>; // vibe -> dish -> weight
  allergyList: string[];
  spiceTolerance: number;
  orderHistory: Array<{dishId: string; timestamp: number; liked: boolean}>;
}
```

#### API Contracts

**POST /api/v1/capture**
```javascript
// Request
{
  "image_base64"?: string,  // menu photo
  "restaurant_id"?: string   // if manual selection
}

// Response
{
  "restaurant": {
    "id": string,
    "name": string,
    "cuisine": string
  },
  "menu_items": MenuItem[],
  "parse_confidence": number
}
```

**POST /api/v1/recommend**
```javascript
// Request
{
  "intent": VibeIntent,
  "menu_items": MenuItem[],
  "user_preferences"?: UserPreference
}

// Response
{
  "recommendations": Recommendation[],
  "session_id": string,
  "generated_in_ms": number
}
```

**POST /api/v1/feedback**
```javascript
// Request
{
  "feedback": UserFeedback
}

// Response
{
  "success": boolean,
  "preference_updated": boolean
}
```

#### Storage Strategy (MVP)

**SQLite for structured data**:
- User preferences (allergies, spice tolerance)
- Session history (vibes selected, dishes recommended)
- Feedback logs (picked/skipped dishes)
- OCR cache (recent menu extractions)

**JSON files for static data**:
- Vibe definitions (8 core vibes)
- Example prompts for LLM
- Photo tips for users

**Rationale**: Simple, no external dependencies, sufficient for 10-100 test users

#### LLM Usage Boundaries

**LLM DOES**:
- Generate dish recommendations based on vibe+menu
- Create reasoning explanations
- Output structured JSON only

**LLM DOES NOT**:
- Store user data
- Make health/medical claims
- Generate prices or nutritional info
- Handle payments or orders

**Structured Output Requirement**:
```python
# Using OpenAI function calling for reliable JSON
response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[...],
  functions=[{
    "name": "recommend_dishes",
    "parameters": {
      "type": "object",
      "properties": {
        "recommendations": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "dish_name": {"type": "string"},
              "reasoning": {"type": "string"},
              "confidence": {"type": "number", "minimum": 0, "maximum": 1}
            },
            "required": ["dish_name", "reasoning", "confidence"]
          }
        }
      },
      "required": ["recommendations"]
    }
  }],
  function_call={"name": "recommend_dishes"}
)
```

### 🍽️ Food-Specific Requirements

#### Allergen Handling (MVP)
- **Basic allergen list**: Nuts, dairy, gluten, shellfish (collected during onboarding)
- **Text matching**: Simple string matching against OCR-extracted menu text
- **User warning**: "Always verify allergens with restaurant staff"
- **Disclaimer**: Shown on every recommendation screen

#### Menu Data Processing (MVP v1.0)
**Real Menu Capture Flow**:
1. User takes photo of physical menu
2. Image uploaded to server (base64 encoding)
3. Google Cloud Vision OCR API extracts text
4. Text parsed into menu items (name + description)
5. LLM reasoning engine generates recommendations based on:
   - Extracted menu items
   - User's vibe selections
   - Basic constraints (allergies, spice level)

**Fallback Options**:
- If OCR fails → Error recovery screen with retry
- If parsing confidence <50% → Show photo tips

#### Memory System Roadmap
**MVP v1.0** (This Sprint):
- No adaptive memory
- Static vibe → dish mappings in LLM prompt
- Basic preference storage (allergies, spice tolerance only)
- Feedback collected but not used for adaptation yet

**v1.1** (Post-MVP):
- Simple preference tracking (liked/disliked dishes)
- Vibe weight adjustments based on feedback
- Session-to-session learning

**v2.0** (Future):
- Full adaptive memory system
- Contradiction handling
- Cross-restaurant preference transfer

#### Scope Boundaries
- **Dine-in recommendations only** (no delivery logistics)
- **No order placement** (recommendation only)
- **No real-time inventory** (static menus from photos)
- **English menus only** for MVP

### 🚨 Risks & Mitigations (MVP)

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Allergen Hallucination** | High - health risk | Medium | Never generate allergen info; use only menu text + disclaimer |
| **Wrong Spice Level** | Medium - bad experience | High | Conservative defaults; clear "mild/medium/hot" in reasoning |
| **OCR Failure** | High - can't proceed | Medium | Error recovery screen with photo tips; good lighting guidance |
| **Trust Failure** | High - abandonment | Medium | Show reasoning for each dish; transparent about AI |
| **LLM Latency** | Medium - user drops | Low | 5-second timeout; loading animation with tips |
| **No Dishes Match Vibe** | Low - confusion | Low | Always return top 3 dishes with exploration framing |
| **Data Privacy** | High - trust loss | Low | Device ID only, local storage, clear privacy policy |

### ❓ Open Questions (Blocking)

1. **OCR API choice**: Google Vision confirmed? AWS Textract as backup?
2. **Confidence threshold**: Below what OCR confidence do we show error?
3. **LLM prompt engineering**: Who owns prompt iteration during sprint?
4. **Feedback timing**: Immediate after order vs. next app open?
5. **Photo size limit**: Max upload size for menu photos?

### 🎨 Design System

#### Visual Identity

```css
/* Emotion-Driven Color Palette */
--coral-primary: #ff6b6b; /* Energy, CTAs */
--mint-fresh: #a8e6cf; /* Success, positive */
--golden-joy: #ffd93d; /* Celebrations */
--warm-white: #fafaf8; /* Base background */
--soft-black: #2c3e50; /* Primary text */

/* Semantic Colors */
--love-green: #4caf50; /* Swipe right */
--nope-red: #f44336; /* Swipe left */
```

#### Typography

```
Display: Poppins 700 (Headers, personality)
Body: System Font (Performance, readability)
Accent: Comfortaa 600 (Buttons, playfulness)
```

#### Gesture Vocabulary

| Gesture     | Action        | Feedback                    |
| ----------- | ------------- | --------------------------- |
| Tap         | Select/Expand | Scale + Haptic              |
| Swipe Right | Approve       | Green glow + Success haptic |
| Swipe Left  | Reject        | Red fade + Light haptic     |
| Long Press  | Preview       | Card expansion              |
| Pull Down   | Refresh       | Elastic bounce              |

### 📱 Platform Requirements

#### Mobile Specifications

- **OS Support:** iOS 13+, Android 10+
- **Screen Sizes:** 5.5" - 6.7" (portrait only)
- **Performance:** 60fps animations, <2s cold start
- **Offline:** Cached restaurants and last session
- **Accessibility:** WCAG 2.1 AA compliant

#### API Requirements

- **Response Time:** <500ms p95
- **Availability:** 99.9% uptime
- **Rate Limiting:** 1000 req/min per user
- **Security:** JWT auth, TLS 1.3

### 🧪 Testing & Quality

#### Testing Strategy

1. **Unit Tests:** 80% code coverage
2. **Integration Tests:** API contract testing
3. **E2E Tests:** Critical user journeys
4. **Performance Tests:** Load and stress testing
5. **Usability Tests:** 5-user sessions per sprint

#### Quality Gates

- No critical bugs in production
- <0.5% crash rate
- <3s response time for all operations
- > 4.5 App Store rating

### 📈 Go-to-Market Strategy

#### Launch Phases

**Phase 0: Alpha (Week 1-2)**

- Internal team testing
- 10 friendly users
- Core flow validation

**Phase 1: Beta (Week 3-6)**

- 100 invited users
- University campus pilot
- Feedback iteration

**Phase 2: Soft Launch (Week 7-10)**

- Single city launch
- 1,000 target users
- Marketing validation

**Phase 3: Scale (Week 11+)**

- Multi-city expansion
- 10,000+ users
- Partnership development

#### Growth Strategies

1. **Campus Ambassadors:** Student influencers
2. **Referral Program:** Free month for 3 invites
3. **Restaurant Partnerships:** Featured recommendations
4. **Content Marketing:** Food anxiety blog
5. **Community Marketing:** Food community for sharing and connecting
6. **Social Proof:** Share your orders

### 💰 Business Model

#### Revenue Streams

1. **Freemium Subscription:**

   - Free: 5 orders/month
   - Pro ($4.99/month): Unlimited + advanced features

2. **Restaurant Partnerships:**

   - Featured placements
   - Analytics dashboard
   - Promotional campaigns

3. **Data Insights:**
   - Anonymized preference trends
   - Market research reports

#### Unit Economics

- **CAC:** $5 (target)
- **LTV:** $50 (10-month average retention)
- **Gross Margin:** 70%
- **Payback Period:** 3 months

### 🚨 Risk Analysis

| Risk            | Probability | Impact | Mitigation                                             |
| --------------- | ----------- | ------ | ------------------------------------------------------ |
| LLM API Costs   | High        | High   | Implement caching, use cheaper models for simple tasks |
| User Adoption   | Medium      | High   | Strong onboarding, viral features                      |
| Restaurant Data | Medium      | Medium | Multiple data sources, user-generated content          |
| Competition     | Low         | Medium | Fast execution, unique UX                              |
| Technical Debt  | Medium      | Low    | Regular refactoring sprints                            |

### 🎯 Success Definition

#### Year 1 Goals

- 100K MAU across 5 cities
- 4.5+ App Store rating
- 40% MAU/DAU ratio
- $500K ARR
- 3 restaurant chain partnerships

#### Long-term Vision (3 Years)

- 1M+ MAU globally
- Multi-language support
- AI-powered meal planning
- Integration with delivery platforms
- $10M ARR

### 📚 Appendices

#### A. Assumptions to Validate
- Menu anxiety exists for international users → User interviews needed
- Mood correlates with food preferences → Track via swipe patterns
- 90-second decision improves satisfaction → Measure via timestamps

#### B. Technical Dependencies
- OpenAI API key and credits
- Google Cloud Vision API
- Apple Developer Account
- Google Play Console

#### C. Legal & Compliance
- GDPR/CCPA compliance for data handling
- Terms of Service and Privacy Policy
- Allergen disclaimer requirements
- App Store guidelines adherence

---

_Last Updated: January 2025_
_Version: 3.0 - Evidence-Safe MVP Edition_
_Status: Ready for 7-Day Sprint_

**Document Approval:**
- Product Manager: ✓
- Engineering Lead: Pending
- UX Designer: Pending
