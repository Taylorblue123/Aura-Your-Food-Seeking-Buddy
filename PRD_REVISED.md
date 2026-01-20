# Product Requirements Document (PRD) - REVISED
## Vibe Food App: Your Local Food Friend

### 🎯 Product Vision
**"Your local food friend who remembers your taste and speaks your language"**

We're building a smart companion that makes ordering food as easy as asking a local friend for recommendations - one who knows your preferences, understands your mood, and speaks your language.

### 🎨 Design Principles

#### Core Principles
1. **Single-Page Simplicity** - Everything happens on one page with expandable cards
2. **Warm Minimalism** - Clean but not cold, simple but not sparse
3. **Gesture-Native** - Swipe, tap, expand - use familiar mobile patterns
4. **Progressive Disclosure** - Show only what's needed, when it's needed
5. **Memory with Consent** - Remember preferences but let users control

#### Visual Identity
- **Color Palette**: Warm pastels with vibrant accents
  - Primary: Coral (#FF6B6B) - energetic but approachable
  - Secondary: Sage (#95E1D3) - fresh and calming
  - Background: Cream (#FFF5E4) - warm and inviting
- **Typography**: Modern sans-serif with personality (e.g., Inter, Poppins)
- **Shapes**: Rounded corners everywhere - friendly and approachable
- **Animations**: Subtle bounces and smooth transitions

### 👥 User Personas

#### Primary: "Alex the Explorer" (70% of users)
- **Age**: 22-28, international student or young professional
- **Context**: New to the city, open to technology
- **Pain Points**: Menu anxiety, FOMO on good dishes, language barriers
- **Goal**: Feel confident ordering, discover local favorites
- **Tech Comfort**: High - uses Instagram, TikTok, food apps daily

#### Secondary: "Sam the Social" (30% of users)
- **Age**: 25-35, social connector
- **Context**: Organizes group dinners, dates, team outings
- **Pain Points**: Accommodating diverse preferences, decision fatigue
- **Goal**: Quick consensus, happy group, smooth experience

### 🗺️ User Journey (Single-Page Architecture)

#### Page 0: Smart Onboarding (First Use Only)
**Outcome**: Collect minimal viable preferences in 30 seconds

```
┌─────────────────────────┐
│   Welcome! I'm Vibe 🍜  │
│   Your food friend       │
│                         │
│ Quick setup (30 sec):   │
│                         │
│ Allergies?              │
│ [None][Nuts][Dairy][+]  │
│                         │
│ Spice tolerance?        │
│ [None][Mild][Hot]       │
│                         │
│ Eating style?           │
│ [Healthy][Comfort][Mix] │
│                         │
│ [Start] or [Skip]       │
└─────────────────────────┘
```

**Success Metrics**:
- Completion rate >80%
- Time to complete <30 seconds
- Skip rate <20%

#### Page 1: Capture Hub (Main Landing)
**Outcome**: Seamless transition from "I'm hungry" to "I have a menu/restaurant"

```
┌─────────────────────────┐
│    Vibe Food 🍜         │
│   "Hey, hungry?"        │
├─────────────────────────┤
│ ┌─────────────────────┐ │
│ │   📸 Camera View    │ │ ← Tappable card (expands to 70%)
│ │   Tap to scan menu  │ │
│ └─────────────────────┘ │
│ ┌─────────────────────┐ │
│ │   📍 Thai House     │ │ ← Tappable card (expands to show 5)
│ │   0.3 mi • $$       │ │
│ └─────────────────────┘ │
│                         │
│ Your recent spots ↓     │
└─────────────────────────┘
```

**Interaction Design**:
- Cards have subtle shadows and hover states
- Tap animates smooth expansion
- Other card minimizes elegantly
- Recent spots appear after 3+ uses

#### Page 2: Vibe Expression (Single Page)
**Outcome**: Capture dining context in <15 seconds

```
┌─────────────────────────┐
│ ┌─────────────────────┐ │
│ │ Thai House: Authen- │ │ ← Collapsed info card
│ │ tic, spicy, casual  │ │
│ └─────────────────────┘ │
│                         │
│  What's your vibe?      │
│                         │
│  ⭕ ⭕ ⭕               │ ← Animated bubbles
│  [😌] [🔥] [👥]        │    appear contextually
│  Comfort Adventure Share│
│                         │
│  ⭕ ⭕                  │
│  [⚡] [💰]              │
│  Quick  Budget          │
│                         │
│  How many eating? [2] ↕ │
│                         │
│  [Get my order →]       │
└─────────────────────────┘
```

**Smart Bubble Logic**:
- Time-aware (lunch = quick options)
- Party-size aware (group = sharing options)
- History-aware (shows previously selected first)

#### Page 3: Order Plan Reveal
**Outcome**: Delightful reveal with natural feedback mechanism

```
┌─────────────────────────┐
│ "Perfect for you two" 💕 │ ← Contextual, warm header
├─────────────────────────┤
│                         │
│   [Swipeable Card]      │
│   ┌─────────────────┐   │
│   │   Pad Thai 🍜    │   │
│   │                 │   │
│   │ "Mild & sharing │   │ ← Card 1 of 3
│   │  size perfect   │   │
│   │  for two"       │   │
│   │                 │   │
│   │ ← 👎    👍 →    │   │ ← Swipe indicators
│   └─────────────────┘   │
│                         │
│   • • ○               │ ← Progress dots
│                         │
└─────────────────────────┘
```

**Swipe Interaction**:
- Left swipe (👎): Removes and learns
- Right swipe (👍): Confirms and learns
- Haptic feedback on swipe
- After all cards: "Happy?" or "Try again?"

#### Page 4: Continuous Learning
**Outcome**: Seamless return to home with improved future experience

```
┌─────────────────────────┐
│   Thanks! Saved ✓       │
│                         │
│ ┌─────────────────────┐ │
│ │ You liked: Mild,    │ │
│ │ shareable dishes    │ │
│ └─────────────────────┘ │
│                         │
│ [Back home] [New place] │
└─────────────────────────┘
```

### 🎯 Success Metrics

#### User Engagement KPIs
- **Activation**: 60% complete first order plan within 5 minutes
- **Retention**: 40% return within 7 days
- **Satisfaction**: >4.5 app store rating
- **Virality**: 20% share with friends

#### Product Health Metrics
- **Time to Value**: <2 minutes from open to order plan
- **Swipe Completion**: >80% swipe through all cards
- **Feedback Rate**: >60% provide swipe feedback
- **Memory Accuracy**: 75% positive swipes on return visits

### 🔧 Core Features (Outcome-Focused)

#### Feature 1: Smart Capture
**User Need**: "I want to understand this menu instantly"
**Outcome**: Menu comprehension in <10 seconds
**Success Metric**: 90% successful capture → explanation

#### Feature 2: Vibe Expression
**User Need**: "The app should understand what I want right now"
**Outcome**: Contextual preference capture in <15 seconds
**Success Metric**: 80% of users select 2+ vibes

#### Feature 3: Intelligent Order Plans
**User Need**: "Tell me exactly what to order"
**Outcome**: Actionable order plan with reasoning
**Success Metric**: 70% plan acceptance rate

#### Feature 4: Gesture-Based Feedback
**User Need**: "Let me quickly train the app"
**Outcome**: Natural preference learning through swipes
**Success Metric**: 60% swipe completion rate

#### Feature 5: Progressive Memory
**User Need**: "Remember me but don't be creepy"
**Outcome**: Improved recommendations over time
**Success Metric**: 20% increase in acceptance rate by session 5

### 📱 Platform Requirements

#### Mobile-First Design
- **Primary**: iOS and Android via React Native
- **Screen Sizes**: Optimized for 5.5" - 6.7" phones
- **Orientation**: Portrait only for MVP
- **Offline**: Graceful degradation with cached data

#### Performance Targets
- **App Launch**: <2 seconds
- **Camera Ready**: <1 second
- **Order Plan Generation**: <3 seconds
- **Animation FPS**: 60fps for all transitions

### 🚀 MVP Scope (7-Day Sprint)

#### IN SCOPE
✅ Single-page architecture with expandable cards
✅ Camera capture + 3 mock restaurants
✅ 6 contextual vibe bubbles
✅ Swipeable order plan cards (3-5 items)
✅ Swipe-based feedback
✅ Basic memory (device-local)

#### OUT OF SCOPE (v2)
❌ User accounts
❌ Real restaurant API integration (use mock)
❌ Social sharing
❌ Payment integration
❌ Multi-language (English only)
❌ Dietary restriction complexity

### 🎨 Component Library

#### Reusable Components
1. **ExpandableCard**
   - Collapsed height: 80px
   - Expanded height: 60-70% screen
   - Animation: Spring physics

2. **VibeBubble**
   - Size: 80x80px
   - States: Default, Pressed, Selected
   - Animation: Scale bounce on tap

3. **SwipeableCard**
   - Width: 90% screen
   - Height: Dynamic content
   - Swipe threshold: 30% width
   - Visual feedback: Tilt on drag

4. **ProgressDots**
   - Size: 8px inactive, 12px active
   - Animation: Smooth transition

### 🧪 Validation Plan

#### Week 1 Success Criteria
1. **Technical**: Complete flow works with mock data
2. **Usability**: 5 test users complete flow in <3 minutes
3. **Delight**: 3/5 users say "wow" or smile
4. **Learning**: Memory improves recommendations in session 2

### 📈 Future Vision (Post-MVP)

#### Phase 2 (Week 2-4)
- Real restaurant integration (Yelp/Google)
- Complex dietary restrictions
- Group ordering coordination
- Price optimization

#### Phase 3 (Month 2-3)
- Social features ("Order like your friends")
- Restaurant partnerships
- Reservation integration
- Multi-language support

#### Phase 4 (Month 4-6)
- Predictive ordering ("Your usual?")
- Meal planning
- Nutrition tracking
- Voice ordering

### 🎯 Why This Will Succeed

1. **Single-Page Simplicity** reduces cognitive load
2. **Gesture-Native** interactions feel natural
3. **Progressive Disclosure** prevents overwhelm
4. **Warm Design** creates emotional connection
5. **Smart Defaults** reduce decision fatigue

The app doesn't just solve menu anxiety - it makes ordering food delightful and personal, like having a local friend who knows your taste.

---

*"Simple enough for your grandma, smart enough for a foodie, fast enough for lunch break"*