# 🏋️ Intelligent AI Fitness Coach - Complete Architecture

## 📐 SYSTEM ARCHITECTURE

```
┌────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Modern UI)                 │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Landing Page         Dashboard           Chat Coach            │
│  (Onboarding)         (Fitness Hub)        (AI Agent)            │
│      ↓                    ↓                    ↓                 │
│  - User Data          - Progress            - Chatbot           │
│  - Profile Pic        - Streaks            - Responses          │
│  - Goals              - Graphs             - Adapt Plans        │
│  - Health Info        - Music Player                            │
│                       - Leaderboard                             │
│                       - Cycle Tracking                          │
│                                                                  │
└────────────────────────────────────┬─────────────────────────────┘
                                     │ REST API Calls (JSON)
                                     ↓
┌────────────────────────────────────────────────────────────────┐
│              BACKEND (FastAPI + Python)                         │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐│
│  │  Auth Service    │  │  User Service    │  │  AI Coach       ││
│  │  - Signup/Login  │  │  - Profile Mgmt  │  │  - Chat         ││
│  │  - JWT Token     │  │  - Metrics       │  │  - Plan Gen     ││
│  │  - Validation    │  │  - Progress      │  │  - Adapt Logic  ││
│  └──────────────────┘  └──────────────────┘  └─────────────────┘│
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐│
│  │  Workout Service │  │  Diet Service    │  │  Agent Service  ││
│  │  - Gen Plans     │  │  - Gen Plans     │  │  - Track Daily  ││
│  │  - Mood-based    │  │  - Personalized  │  │  - Auto-adapt   ││
│  │  - Equipment     │  │  - Menstrual     │  │  - Notify       ││
│  │  - Form Links    │  │    tracking      │  │  - Recommend    ││
│  └──────────────────┘  └──────────────────┘  └─────────────────┘│
│                                                                  │
│  ┌──────────────────────────────────────────────────────────────┐│
│  │        AI LOGIC (Gemini/Claude Agent)                        ││
│  │  - Decision making                                          ││
│  │  - Personalization engine                                   ││
│  │  - Prompt optimization                                      ││
│  │  - Response generation                                      ││
│  └──────────────────────────────────────────────────────────────┘│
│                                                                  │
└────────────────────────────────────┬─────────────────────────────┘
                                     │ Database Queries
                                     ↓
┌────────────────────────────────────────────────────────────────┐
│              DATABASE (PostgreSQL / Firebase)                   │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Tables:                                                         │
│  • users (id, name, age, email, password_hash)                 │
│  • profiles (user_id, weight, height, goal, budget)            │
│  • fitness_data (daily metrics, mood, sleep, energy)           │
│  • diet_plans (generated plans, preferences)                   │
│  • workout_plans (routines, equipment, difficulty)             │
│  • menstrual_tracking (cycle status, mood impact)              │
│  • chat_history (conversations with AI)                        │
│  • progress (weight, activity, streaks)                        │
│  • settings (notifications, preferences)                       │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ COMPONENT ARCHITECTURE

### **Frontend Components (React)**

```
App/
├── pages/
│   ├── Landing.jsx (Onboarding Form)
│   ├── Dashboard.jsx (Main Hub)
│   ├── Coach.jsx (Chat Interface)
│   ├── Progress.jsx (Analytics)
│   ├── Profile.jsx (Settings)
│   └── Leaderboard.jsx (Competition)
│
├── components/
│   ├── Header.jsx
│   ├── Navigation.jsx
│   ├── StatsCard.jsx
│   ├── ProgressChart.jsx
│   ├── ChatMessage.jsx
│   ├── MenstrualTracker.jsx
│   ├── MusicPlayer.jsx
│   └── LeaderboardTable.jsx
│
├── services/
│   ├── api.js (API calls)
│   ├── auth.js (Authentication)
│   └── storage.js (Local storage)
│
├── context/
│   ├── UserContext.js
│   ├── CoachContext.js
│   └── DashboardContext.js
│
└── styles/
    ├── globals.css
    ├── components.css
    └── animations.css
```

---

## 🔌 API ENDPOINTS (FastAPI)

### **Authentication**
```
POST   /api/auth/signup          Create new user
POST   /api/auth/login           User login
POST   /api/auth/logout          User logout
GET    /api/auth/profile         Get current user
```

### **User Management**
```
GET    /api/user/profile         Get user profile
PUT    /api/user/profile         Update profile
POST   /api/user/health-data     Submit daily metrics (mood, sleep, energy)
GET    /api/user/progress        Get progress data
```

### **AI Coach (The Magic)**
```
POST   /api/coach/chat           Chat with AI coach
POST   /api/coach/generate-diet  Generate diet plan
POST   /api/coach/generate-workout  Generate workout plan
POST   /api/coach/mood-workout   Get mood-based workout
POST   /api/coach/get-video-link Get exercise form video
```

### **Women-Specific**
```
POST   /api/menstrual/update     Update cycle status
GET    /api/menstrual/status     Get current cycle phase
POST   /api/menstrual/recommendations  Get phase-based recommendations
```

### **Dashboard**
```
GET    /api/dashboard/summary    Get dashboard summary
GET    /api/dashboard/graphs     Get progress graphs
GET    /api/dashboard/streak     Get streak data
POST   /api/dashboard/proof      Upload workout proof
```

### **Leaderboard**
```
GET    /api/leaderboard          Get leaderboard standings
GET    /api/leaderboard/nearby   Get users at same fitness level
POST   /api/leaderboard/score    Update user score
```

---

## 📊 DATABASE SCHEMA

### **Users Table**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    age INT,
    gender VARCHAR(20),
    profession VARCHAR(100),
    goal VARCHAR(50),  -- 'fat_loss', 'muscle_gain', 'maintenance'
    budget VARCHAR(20),  -- 'low', 'medium', 'high'
    daily_time INT,  -- minutes
    diet_preference VARCHAR(50),  -- 'veg', 'non_veg', 'eggetarian'
    disabilities TEXT,
    diseases TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### **Fitness Metrics Table**
```sql
CREATE TABLE fitness_metrics (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    date DATE NOT NULL,
    weight FLOAT,
    mood VARCHAR(50),  -- 'excellent', 'good', 'average', 'stressed'
    sleep_hours FLOAT,
    energy_level INT,  -- 1-10
    steps INT,
    workout_completed BOOLEAN,
    workout_duration INT,  -- minutes
    created_at TIMESTAMP DEFAULT NOW()
);
```

### **Menstrual Cycle Table**
```sql
CREATE TABLE menstrual_tracking (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    cycle_start_date DATE,
    cycle_length INT,  -- days
    current_phase VARCHAR(50),  -- 'menstruation', 'follicular', 'ovulation', 'luteal'
    mood_impact VARCHAR(100),
    energy_impact VARCHAR(100),
    pain_level INT,  -- 1-10
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### **Diet Plans Table**
```sql
CREATE TABLE diet_plans (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    plan_text TEXT NOT NULL,
    calories INT,
    protein INT,
    carbs INT,
    fats INT,
    generated_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50),  -- 'active', 'archived'
    phase VARCHAR(50)  -- menstrual phase when generated
);
```

### **Workout Plans Table**
```sql
CREATE TABLE workout_plans (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    plan_text TEXT NOT NULL,
    duration INT,  -- minutes
    difficulty VARCHAR(50),  -- 'beginner', 'intermediate', 'advanced'
    equipment VARCHAR(200),
    mood_adapted VARCHAR(50),
    generated_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50)
);
```

### **Chat History Table**
```sql
CREATE TABLE chat_history (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    type VARCHAR(50),  -- 'chat', 'diet_request', 'workout_request'
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🤖 AI AGENT LOGIC FLOW

### **Agent Decision Tree**

```
USER INPUT
    ↓
┌─────────────────────────────┐
│ CONTEXT GATHERING           │
├─────────────────────────────┤
│ • User profile              │
│ • Current metrics           │
│ • Recent progress           │
│ • Menstrual cycle (if women)│
│ • Chat history              │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ REQUEST CLASSIFICATION      │
├─────────────────────────────┤
│ • Is it about diet?         │
│ • Is it about workout?      │
│ • Is it mood-based?         │
│ • Is it health advice?      │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────────────┐
│ PERSONALIZATION ENGINE              │
├─────────────────────────────────────┤
│ • Apply user's goal                 │
│ • Consider current mood              │
│ • Account for energy level           │
│ • Apply menstrual cycle factors (F)  │
│ • Check disabilities/injuries        │
│ • Consider available equipment       │
│ • Respect budget constraints         │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────┐
│ GENERATE WITH GEMINI API    │
├─────────────────────────────┤
│ • Create optimized prompt   │
│ • Call Gemini API           │
│ • Get AI response           │
│ • Parse response            │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ ENHANCEMENT                 │
├─────────────────────────────┤
│ • Add YouTube video links   │
│ • Add form tips             │
│ • Add nutrition info        │
│ • Add motivational message  │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ STORE & RETURN              │
├─────────────────────────────┤
│ • Save to chat history      │
│ • Update user context       │
│ • Return to frontend        │
└─────────────────────────────┘
```

### **Agentic Features**

```
AGENT RUNS DAILY (Async Task)
    ↓
├─ Check user's mood (if available)
├─ Check sleep quality
├─ Check energy level
├─ Evaluate recent progress
├─ Check menstrual cycle (if applicable)
│
└─ THEN:
   ├─ Auto-generate today's workout
   ├─ Auto-generate today's diet
   ├─ Send motivation notification
   ├─ Recommend exercise based on energy
   ├─ Send sleep reminder
   └─ Update AI coach context
```

---

## 💾 KEY FEATURES IMPLEMENTATION

### **1. Menstrual Cycle Tracking**
- Track cycle start date
- Calculate current phase
- Auto-adjust workout intensity
- Modify diet recommendations
- Adjust recovery suggestions

### **2. Mood-Based Adaptation**
```
MOOD: Stressed
  → Suggest yoga / stretching
  → Light cardio (30 min walks)
  → Calming diet (balanced nutrients)
  → Recovery focus

MOOD: Energetic
  → High-intensity training
  → Strength training
  → Higher protein diet
  → Challenge completion

MOOD: Tired
  → Light active recovery
  → Mobility work
  → Hydration + sleep focus
  → Nutrition optimization
```

### **3. Agentic Notifications**
```
7:00 AM   → "Good morning! Your energy level is high. 
             Ready for a challenging workout? ⚡"
             
6:00 PM   → "Your workout for today is ready! 💪
             Free 45 mins? Let's go!"
             
9:00 PM   → "Great workout today! Remember to hydrate 💧
             and rest well. Bedtime reminder: 11 PM"
             
Weekly    → "Weekly Progress: 4/7 days completed! 
             You're 57% there. One more day? 🔥"
```

### **4. Exercise Form Links**
```
For each exercise, provide:
- Exercise name
- Sets x Reps
- Form tips
- YouTube link (search optimized)
- Common mistakes
- Modification options
```

---

## 🎨 UI/UX DESIGN PRINCIPLES

### **Design System**
```
Colors:
- Primary: #6366F1 (Indigo)
- Secondary: #EC4899 (Pink)
- Success: #10B981 (Green)
- Warning: #F59E0B (Amber)
- Danger: #EF4444 (Red)
- Dark: #1F2937 (Gray)
- Light: #F9FAFB (White)

Typography:
- Headers: 'Inter Bold' (24px, 28px, 32px)
- Body: 'Inter Regular' (14px, 16px)
- Small: 'Inter Light' (12px)

Spacing: 8px grid system
Border Radius: 12px default
Shadows: Subtle elevation system
```

### **Dashboard Layout**
```
┌─────────────────────────────────────────────────┐
│  Logo    Navigation                   User Menu │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │ Welcome Back, [Name]!                      │ │
│  │ Your AI Coach is ready. Let's train!       │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐         │
│  │ Today's │  │ Streak  │  │ Energy  │         │
│  │  Mood   │  │   12    │  │  85%    │         │
│  └─────────┘  └─────────┘  └─────────┘         │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │  📋 Today's Plan (Top Priority)            │ │
│  │  ─────────────────────────────────────     │ │
│  │  Workout: 45m Full Body + Cardio           │ │
│  │  Diet: 2000 cal (High Protein)             │ │
│  │  Water: 3L target                          │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │  📊 Your Progress                          │ │
│  │  [Weight Graph] [Activity Graph]           │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │  🎵 Workout Playlist (Based on Mood)       │ │
│  │  [Music Player UI]                         │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 🚀 DEPLOYMENT ARCHITECTURE

```
Frontend:
- Build: npm run build
- Host: Vercel / Netlify (Automatic deploy)
- CDN: Cloudflare / AWS CloudFront

Backend:
- Container: Docker
- Platform: Railway / Render / AWS EC2
- Environment: Python 3.11 + FastAPI

Database:
- PostgreSQL on: Railway / AWS RDS
- OR Firebase: Firestore

AI/LLM:
- Google Gemini API (cloud-based)
- Run on backend (async tasks)

Monitoring:
- Sentry (error tracking)
- LogRocket (frontend monitoring)
- DataDog (performance)
```

---

## 📈 HACKATHON WINNING STRATEGY

### **What Makes This Win**

1. **Innovation** 🚀
   - Agentic AI (not just chatbot)
   - Women-specific personalization
   - Real-time adaptation

2. **Technical Depth** 💻
   - Full-stack modern architecture
   - Complex AI logic
   - Database optimization

3. **User Experience** ✨
   - Beautiful, modern UI
   - Intuitive interactions
   - Smooth animations

4. **Business Value** 💰
   - Solves real problem
   - Scalable architecture
   - Monetization potential

### **Demo Script (5 minutes)**
```
1. Show Landing Page (onboarding flow) - 30 sec
2. Show Dashboard (beautiful UI) - 1 min
3. Show Chat with AI (real responses) - 1.5 min
4. Show Mood-based Adaptation - 30 sec
5. Show Women's Cycle Tracking - 30 sec
6. Show Agent doing Autonomous Actions - 30 sec
```

---

## Next Steps

1. **Backend Implementation** (3-4 hours)
   - FastAPI setup
   - Database models
   - Gemini integration
   - Agent logic

2. **Frontend Implementation** (4-5 hours)
   - React setup
   - Component creation
   - API integration
   - Styling

3. **Testing & Polish** (2-3 hours)
   - End-to-end testing
   - Bug fixes
   - Performance optimization

4. **Deployment** (1-2 hours)
   - Docker setup
   - Deploy backend
   - Deploy frontend

**Total: 10-14 hours for complete MVP**

---
