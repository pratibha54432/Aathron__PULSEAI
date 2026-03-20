# Project File Guide

Complete reference for every file in the FitnessCoach MVP project.

## 📂 Root Directory Files

### Documentation
- **README.md** - Main project overview and quick start guide
  - Features list, tech stack, API overview
  - Quick start (3 steps to running)
  - Troubleshooting guide
  
- **SETUP.md** - Detailed step-by-step setup instructions
  - Environment setup
  - Google Gemini API configuration
  - Database options (Firebase, PostgreSQL)
  - Complete API endpoints reference
  - Troubleshooting section
  
- **ARCHITECTURE.md** - System design documentation
  - Full system architecture with diagrams
  - Data flow for each feature
  - API endpoints specifications
  - Database schema outline
  - Tech stack rationale
  
- **FRONTEND_SETUP.md** - React frontend setup guide
  - React project structure
  - Sample components (Onboarding, MoodTracker, Workout)
  - API integration examples
  - Styling tips and CSS helpers
  
- **HACKATHON_GUIDE.md** - Winning strategy for hackathon judges
  - What judges look for
  - Perfect 5-minute demo script
  - Key talking points
  - Common questions and answers
  - Day-by-day development timeline
  - Documentation checklist

### Configuration Files
- **.env.example** - Template for environment variables
  - GEMINI_API_KEY
  - DATABASE_URL options
  - Server configuration
  
- **.gitignore** - Files to exclude from version control
  - Python cache files
  - .env files (keep API keys secret!)
  - Virtual environments
  - IDE files
  - OS-specific files

### Build & Dependencies
- **requirements.txt** - Python package dependencies
  - FastAPI and Uvicorn
  - Pydantic for data validation
  - Google Generative AI SDK
  - Firebase Admin SDK
  - SQLAlchemy for databases
  - For PostgreSQL: psycopg2
  - Security: python-jose, passlib
  - Environment: python-dotenv
  
- **Makefile** - Convenient command shortcuts
  - `make install` - Install dependencies
  - `make setup` - Full project setup
  - `make run` - Start backend server
  - `make test` - Run test suite
  - `make clean` - Remove cache
  - `make deploy-backend` - Deployment instructions

### Testing & Validation
- **test_api.py** - Automated test suite
  - Tests user registration
  - Tests AI diet plan generation
  - Tests AI workout generation
  - Tests mood tracking
  - Tests progress statistics
  - Tests API documentation
  - Run with: `python test_api.py`

---

## 🗂️ Backend Directory (`/backend`)

### Core Application
- **main.py** - FastAPI application entry point
  - CORS configuration for frontend
  - Database initialization
  - Routes registration
  - Uvicorn server setup
  - Key routes:
    * `POST /api/auth/signup` - Register user
    * `POST /api/auth/login` - Login
    * `POST /api/coach/*` - AI coaching endpoints
    * `GET /api/progress/*` - Progress tracking
  
- **models.py** - Pydantic data models (schema definitions)
  - `UserRegister` - User signup data
  - `UserResponse` - User profile response
  - `UserProfile` - Complete user data
  - `MenstrualCycleData` - Women's health tracking
  - `ChatRequest/Response` - Chat messages
  - `DietPlan` - Diet plan response
  - `WorkoutPlan` - Workout response
  - `MoodData` - Mood logging
  - `ProgressTracker` - Progress statistics
  - `LeaderboardEntry` - Ranking data
  - All models have built-in validation

### Services Layer (Business Logic)
- **services/coach_service.py** - AI coaching logic
  - `CoachService` class with Gemini integration
  - Methods:
    * `generate_diet_plan()` - Creates personalized diets
    * `generate_workout()` - Creates exercise routines
    * `suggest_mood_workout()` - Adapts based on mood
    * `injury_prevention_check()` - Checks for overuse
    * `suggest_form_correction()` - Form feedback
  - Prompt engineering for consistent quality
  - Handles all Gemini API calls

- **services/user_service.py** (TODO)
  - User authentication
  - Password hashing
  - JWT token generation
  - Profile CRUD operations

- **services/progress_service.py** (TODO)
  - Progress calculation
  - Streak management
  - Analytics generation
  - Weight tracking

- **services/leaderboard_service.py** (TODO)
  - Rank calculation
  - Scoring logic
  - Leaderboard generation

### API Routers (Endpoints)
- **routers/auth.py** - Authentication endpoints
  - `POST /api/auth/signup` - Register new user
  - `POST /api/auth/login` - User login
  - `POST /api/auth/logout` - User logout
  - Mock database (needs real DB integration)

- **routers/coach.py** - AI coaching endpoints
  - `POST /api/coach/chat` - Real-time chat
  - `POST /api/coach/diet-plan` - Generate diet
  - `POST /api/coach/workout` - Generate workout
  - `POST /api/coach/mood-workout` - Mood-based workout
  - `POST /api/coach/injury-prevention` - Injury check
  - `GET /api/coach/history` - Chat history
  - Uses `CoachService` for AI generation

- **routers/progress.py** - Progress tracking endpoints
  - `POST /api/progress/log-mood` - Log mood/energy
  - `GET /api/progress/progress/{user_id}` - Get stats
  - `POST /api/progress/log-workout/{user_id}` - Log workout
  - `GET /api/progress/streak/{user_id}` - Get streak
  - `POST /api/progress/log-weight/{user_id}` - Track weight
  - Calculates averages and trends

- **routers/users.py** (TODO)
  - User profile management
  - User settings
  - Disability/disease tracking
  - Profile picture upload

### Database Layer (TODO)
- **database/db_init.py** (TODO)
  - Database connection setup
  - SQLAlchemy session management
  - Firebase Admin SDK initialization
  - Migration support

### Configuration
- **.env** (Create this file)
  - Copy from .env.example
  - Add your GEMINI_API_KEY
  - Set DATABASE_URL for your choice

---

## ⚛️ Frontend Directory (`/frontend`) - To Build

### Project Structure (Recommended)
```
frontend/
├── src/
│   ├── components/
│   │   ├── Onboarding.js - User signup form
│   │   ├── Dashboard.js - Main dashboard
│   │   ├── ChatCoach.js - AI chat interface
│   │   ├── DietPlanner.js - Diet display
│   │   ├── WorkoutPlanner.js - Workout display
│   │   ├── MoodTracker.js - Mood logging
│   │   ├── Progress.js - Analytics dashboard
│   │   ├── Leaderboard.js - Rankings
│   │   └── MenstrualCycle.js - Women's health
│   ├── services/
│   │   └── api.js - Backend API calls
│   ├── App.js - Main component
│   ├── App.css - Global styles
│   └── index.js - React entry point
├── public/
│   └── index.html
└── package.json
```

### To Create Frontend
```bash
npx create-react-app frontend
cd frontend
npm install axios react-router-dom
```

See **FRONTEND_SETUP.md** for detailed React examples and components.

---

## 📊 Documentation Directory (`/docs`)

- **ARCHITECTURE.md** - Complete system design (already in root)

Additional docs (to add):
- Deployment guide
- Database schema
- API authentication flow
- Error codes reference

---

## 🔄 Data Flow Examples

### User Registration
```
Frontend Form → POST /api/auth/signup → Backend receives data
→ main.py auth router → Validates with UserRegister model
→ Stores in users_db → Returns UserResponse with ID
```

### AI Workout Generation
```
User clicks "Get Workout" → Frontend: POST /api/coach/workout
→ coach.py receives request → Calls CoachService.generate_workout()
→ coach_service.py crafts prompt with user context
→ Sends to Google Gemini API → Returns AI-generated workout
→ coach.py formats response → Returns to frontend
→ Frontend displays workout to user
```

### Mood-Based Adaptation
```
User logs mood (stressed, low energy) → /api/progress/log-mood
→ progress_router stores mood data → Frontend requests mood workout
→ /api/coach/mood-workout includes mood context in prompt
→ CoachService generates stress-relieving workout (yoga, not HIIT)
→ User gets adaptive recommendation
```

---

## 📝 Key Design Patterns

### Pydantic Validation
All incoming data is validated by Pydantic models automatically:
- Type checking
- Required field enforcement
- Email validation
- Custom validators

### Service Layer Pattern
- `main.py` - Defines routes
- `routers/*.py` - Route handlers
- `services/*.py` - Business logic
- Separation of concerns = easier to test and maintain

### Environment Variables
- All secrets in `.env` file (not in code)
- `.gitignore` prevents accidental commits
- `.env.example` shows required variables

### Mock Database
- `users_db = {}` in auth.py
- `progress_db = {}` in progress.py
- **TODO:** Replace with Firebase or PostgreSQL

---

## 🚀 Development Workflow

### Make a Change
1. Edit files in `/backend`
2. Backend auto-reloads with `uvicorn main:app --reload`
3. Visit http://localhost:8000/docs to test
4. Check API responses

### Common Tasks

**Add New Endpoint**
```python
# 1. Add model to models.py (Pydantic)
class NewFeature(BaseModel):
    user_id: str
    data: str

# 2. Create service method in services/coach_service.py
async def new_feature(self, user_id: str, data: str):
    pass

# 3. Add router method in routers/feature.py
@router.post("/new-feature")
async def new_feature(request: NewFeature):
    pass

# 4. Register router in main.py
app.include_router(feature.router, prefix="/api/feature")
```

**Test New Feature**
```bash
# Visit http://localhost:8000/docs
# Click your new endpoint
# Fill in test data
# Click "Execute"
# See response
```

---

## 🔍 File Dependencies

```
main.py
  ├── models.py (imports all data models)
  ├── routers/auth.py
  ├── routers/coach.py
  ├── routers/progress.py
  │   └── services/coach_service.py
  │       └── google.generativeai (Gemini API)
  └── .env (GEMINI_API_KEY)
```

---

## 📦 What's Complete vs TODO

### ✅ Complete
- FastAPI framework setup
- Pydantic models for all entities
- AI coaching service with Gemini integration
- Auth, coach, and progress routers
- API documentation auto-generation
- Test suite

### 🔄 In Progress
- Backend server running
- API endpoints responding
- Gemini generating real responses

### ❌ TODO
- Database integration (Firebase/PostgreSQL)
- User authentication (JWT tokens)
- Complete user service
- Complete progress service
- Leaderboard service
- React frontend build
- Frontend-backend integration
- Deploy to production

---

## 🎯 Next Action Items

1. **Immediate (Now)**
   - Get GEMINI_API_KEY from makersuite.google.com
   - Create backend/.env with API key
   - Run `pip install -r requirements.txt`
   - Start backend: `uvicorn backend/main:app --reload`
   - Test API: `python test_api.py`

2. **Next (Day 1-2)**
   - Integrate database (Firebase or PostgreSQL)
   - Implement user authentication
   - Test authentication flow

3. **Then (Day 3-5)**
   - Build React frontend
   - Create components for each page
   - Connect frontend to backend APIs
   - Test end-to-end flow

4. **Finally (Day 6-8)**
   - Polish UI/UX
   - Optimize performance
   - Deploy to production
   - Prepare hackathon demo

---

## 🆘 Finding Things

Looking for: | Location
---|---
Database setup | SETUP.md or database/db_init.py (TODO)
User authentication | routers/auth.py
AI diet generation | services/coach_service.py
API endpoints | routers/*.py
Data models | models.py
Frontend examples | FRONTEND_SETUP.md
System design | ARCHITECTURE.md
Setup instructions | SETUP.md
Hackathon tips | HACKATHON_GUIDE.md
Quick start | README.md

---

**Need clarification?** Check the specific documentation file listed above!
