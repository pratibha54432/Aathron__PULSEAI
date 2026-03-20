# FitnessCoach MVP - Setup Guide

## Quick Start (5 minutes)

### 1. Install Python Dependencies
```bash
cd /Users/lucky/Documents/FitnessCoachMVP
pip install -r requirements.txt
```

### 2. Set Up Google Gemini API
```bash
# Get your API key from https://makersuite.google.com/app/apikey
# No credit card needed - free tier includes 50 req/min

# Create .env file in backend folder
echo "GEMINI_API_KEY=your_api_key_here" > backend/.env
```

### 3. Run Backend Server
```bash
cd backend
uvicorn main:app --reload --port 8000
```

Server runs at: http://localhost:8000
API Docs: http://localhost:8000/docs (interactive Swagger UI)

---

## Complete Setup Steps

### Step 1: Environment Setup
```bash
# Navigate to project
cd /Users/lucky/Documents/FitnessCoachMVP

# Create Python virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Verify installation
python -c "import fastapi; import google.generativeai; print('✅ All imports successful')"
```

### Step 2: Configure Google Gemini API
```bash
# 1. Visit https://makersuite.google.com/app/apikey
# 2. Click "Create API Key" (no credit card needed!)
# 3. Copy the key
# 4. Create backend/.env file with:

GEMINI_API_KEY=your_actual_api_key_here
DATABASE_URL=sqlite:///fitness.db  # For development
```

### Step 3: Start Backend Server
```bash
cd backend
uvicorn main:app --reload --port 8000

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

### Step 4: Test API Endpoints
Use the interactive docs at: http://localhost:8000/docs

Or test via curl:
```bash
# Test 1: Register user
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 25,
    "gender": "male",
    "weight": 75,
    "height": 180,
    "goal": "weight_loss",
    "budget": "low",
    "daily_time": 30,
    "profession": "Software Engineer",
    "diet_preference": "vegetarian",
    "disabilities": [],
    "diseases": []
  }'

# Test 2: Get AI Diet Plan
curl -X POST "http://localhost:8000/api/coach/diet-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_1",
    "goal": "weight_loss",
    "diet_preference": "vegetarian"
  }'

# Test 3: Get AI Workout
curl -X POST "http://localhost:8000/api/coach/workout" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_1",
    "goal": "muscle_gain",
    "available_time": 45
  }'

# Test 4: Log Mood
curl -X POST "http://localhost:8000/api/progress/log-mood" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_1",
    "mood_score": 7,
    "energy_level": 8,
    "sleep_hours": 8,
    "stress_level": 3
  }'
```

---

## Project Structure

```
FitnessCoachMVP/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── models.py               # Pydantic data models
│   ├── .env                    # Environment variables (create this)
│   ├── services/
│   │   ├── coach_service.py    # Gemini AI integration
│   │   └── user_service.py     # User management (TODO)
│   ├── routers/
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── coach.py            # Coaching AI endpoints
│   │   └── progress.py         # Progress tracking endpoints
│   └── database/
│       └── db_init.py          # Database setup (TODO)
├── frontend/                   # React app (TODO)
├── docs/
│   └── ARCHITECTURE.md         # System design documentation
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```

---

## API Endpoints Reference

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user

### AI Coaching
- `POST /api/coach/chat` - Real-time coaching chat
- `POST /api/coach/diet-plan` - Generate personalized diet plan
- `POST /api/coach/workout` - Generate workout routine
- `POST /api/coach/mood-workout` - Get mood-based workout suggestions
- `POST /api/coach/injury-prevention` - Check injury prevention recommendations
- `GET /api/coach/history` - Get coaching interaction history

### Progress Tracking
- `POST /api/progress/log-mood` - Log mood and energy data
- `GET /api/progress/progress/{user_id}` - Get progress statistics
- `POST /api/progress/log-workout/{user_id}` - Log completed workout
- `GET /api/progress/streak/{user_id}` - Get workout streak
- `POST /api/progress/log-weight/{user_id}` - Log weight update

---

## Database Integration (Next Steps)

### Option A: Firebase (Recommended for hackathon - fastest setup)
```bash
# 1. Go to https://console.firebase.google.com
# 2. Create new project
# 3. Download service account key JSON
# 4. Save as backend/firebase-key.json
# 5. Update main.py to use Firebase Admin SDK

pip install firebase-admin
```

### Option B: PostgreSQL (Recommended for production)
```bash
# 1. Install PostgreSQL locally or use cloud provider
# 2. Create database: createdb fitness_coach
# 3. Update .env file:

DATABASE_URL=postgresql://user:password@localhost/fitness_coach

# 4. Run migrations (TODO)
```

---

## Frontend Setup (Next Steps)

```bash
# Create React app in frontend directory
cd frontend
npx create-react-app .

# Install API client
npm install axios react-query

# Copy frontend files from /Users/lucky/Documents/FitnessCoach/
# Convert HTML to React components

# Run frontend
npm start
```

---

## Testing the AI Features

### Test Prompt: Diet Plan Generation
```json
{
  "user_id": "test_user",
  "goal": "weight_loss",
  "age": 25,
  "weight": 80,
  "height": 180,
  "diet_preference": "vegetarian"
}
```

**Expected Response:**
```json
{
  "diet_plan": "Day 1:\n- Breakfast: Oatmeal with berries and almonds (400 cal)\n- Lunch: Quinoa salad with chickpeas (450 cal)\n- Dinner: Lentil curry with brown rice (500 cal)\n- Snacks: Greek yogurt, apple (200 cal)\nTotal: 1550 calories",
  "macros": {"protein": 120, "carbs": 175, "fats": 45},
  "duration": "4 weeks"
}
```

### Test Prompt: Mood-Based Workout
```json
{
  "user_id": "test_user",
  "current_mood": "stressed",
  "energy_level": 4,
  "available_time": 30
}
```

**Expected Response:**
```json
{
  "suggested_workout": "Yoga Flow - 30 minutes\n1. Cat-Cow Stretch (5 min)\n2. Downward Dog (3 min)\n3. Child's Pose (5 min)\n4. Savasana (10 min)\n\nFocus: Stress relief and relaxation",
  "intensity": "low",
  "reason": "Your stress levels are high. Light, mindful exercise will help reduce anxiety."
}
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"
**Solution:**
```bash
pip install -r requirements.txt
# Or specifically: pip install fastapi uvicorn
```

### Issue: "GEMINI_API_KEY not found"
**Solution:**
1. Go to https://makersuite.google.com/app/apikey
2. Create backend/.env file with your API key
3. Restart the server

### Issue: Port 8000 already in use
**Solution:**
```bash
# Use different port
uvicorn main:app --reload --port 8001
```

### Issue: CORS errors from frontend
**Fix in main.py already included:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Deployment Checklist

- [ ] Create backend/.env with GEMINI_API_KEY
- [ ] Test all API endpoints via http://localhost:8000/docs
- [ ] Connect to Firebase or PostgreSQL database
- [ ] Build React frontend
- [ ] Connect frontend to backend APIs
- [ ] Test authentication flow end-to-end
- [ ] Test AI features with real Gemini API
- [ ] Add unit tests
- [ ] Deploy backend to Render/Railway/Heroku
- [ ] Deploy frontend to Vercel/Netlify
- [ ] Monitor logs and user feedback

---

## For Hackathon Success

1. **MVP Features** (Must-have):
   - ✅ User onboarding form (already in main.py)
   - ✅ AI diet plan generation (Gemini integration done)
   - ✅ AI workout generation (Gemini integration done)
   - ✅ Mood tracking (endpoints created)
   - ✅ Streak tracking (endpoints created)

2. **Wow Features** (Nice-to-have):
   - Women's menstrual cycle tracking (model created, UI needed)
   - Injury prevention logic (CoachService method ready)
   - Mood-based workout adaptation (implemented)
   - Real-time chat with AI coach

3. **Demo Tips**:
   - Show the interactive API docs (http://localhost:8000/docs)
   - Demonstrate Gemini generating a diet plan in real-time
   - Show mood tracking affecting workout recommendations
   - Highlight the women-specific menstrual cycle tracking feature
   - Explain the agentic behavior (system adapts to user mood/energy)

---

## Next Actions

1. **Get Google Gemini API Key** (2 min)
   - Visit https://makersuite.google.com/app/apikey
   - Create .env file with the key

2. **Test Backend** (5 min)
   - Run `uvicorn backend:main --reload`
   - Visit http://localhost:8000/docs
   - Try API endpoints

3. **Set Up Database** (15 min)
   - Choose Firebase or PostgreSQL
   - Configure connection in .env
   - Update main.py with DB initialization

4. **Build React Frontend** (1-2 hours)
   - Create React project in frontend/
   - Copy UI from /Users/lucky/Documents/FitnessCoach/
   - Connect to backend APIs using axios

5. **Advanced Features** (2-3 hours)
   - Women's menstrual cycle tracking UI
   - Injury prevention alerts
   - Leaderboard system

---

**Questions?** Check ARCHITECTURE.md for detailed system design.
