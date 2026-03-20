# ⚡ Quick Reference Cheat Sheet

## 🚀 Getting Started (5 Minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file with API key
echo "GEMINI_API_KEY=your_key_here" > backend/.env

# 3. Start backend
cd backend
uvicorn main:app --reload

# 4. Test API
# Open http://localhost:8000/docs
```

---

## 🔗 Important URLs

| URL | Purpose |
|-----|---------|
| http://localhost:8000 | API root |
| http://localhost:8000/docs | Interactive API docs |
| http://localhost:8000/redoc | Alternative API docs |
| http://localhost:3000 | Frontend (when running) |
| https://makersuite.google.com/app/apikey | Get Gemini API key |

---

## 📡 API Endpoints Quick Reference

### Authentication
| Method | Endpoint | What It Does |
|--------|----------|-------------|
| POST | /api/auth/signup | Register new user |
| POST | /api/auth/login | Login user |
| POST | /api/auth/logout | Logout user |

### AI Coaching
| Method | Endpoint | What It Does |
|--------|----------|-------------|
| POST | /api/coach/chat | Chat with AI coach |
| POST | /api/coach/diet-plan | Generate diet plan |
| POST | /api/coach/workout | Generate workout |
| POST | /api/coach/mood-workout | Mood-based workout |
| POST | /api/coach/injury-prevention | Check injury risk |
| GET | /api/coach/history | Get chat history |

### Progress Tracking
| Method | Endpoint | What It Does |
|--------|----------|-------------|
| POST | /api/progress/log-mood | Log mood/energy |
| POST | /api/progress/log-workout | Log workout |
| POST | /api/progress/log-weight | Log weight |
| GET | /api/progress/progress/{id} | Get stats |
| GET | /api/progress/streak/{id} | Get streak |

---

## 💻 Common Commands

```bash
# Backend setup
pip install -r requirements.txt           # Install packages
cd backend && uvicorn main:app --reload   # Start server
python test_api.py                        # Run full test suite

# Makefile shortcuts
make install                              # Install dependencies
make setup                                # Full setup
make run                                  # Start server
make test                                 # Test API
make clean                                # Clean cache

# Database
python -m sqlite3 fitness.db              # Access SQLite
createdb fitness_coach                    # Create PostgreSQL DB
firebase-admin init                       # Initialize Firebase

# Frontend
npx create-react-app frontend             # Create React app
cd frontend && npm start                  # Start React dev server
npm install axios react-router-dom        # Frontend dependencies
```

---

## 📝 Common Code Patterns

### Create New Endpoint
```python
# 1. Add to models.py
class NewRequest(BaseModel):
    user_id: str
    data: str

# 2. Add to routers/
@router.post("/new-endpoint")
async def new_endpoint(request: NewRequest):
    return {"success": True, "data": request.data}

# 3. Register in main.py
app.include_router(router_name, prefix="/api/name")
```

### Call Backend from Frontend
```javascript
// In services/api.js
export const newFeature = (userId, data) => 
  api.post('/feature/new-endpoint', { user_id: userId, data });

// In React component
const response = await newFeature(userId, data);
console.log(response.data);
```

### Use Gemini AI
```python
# Already in coach_service.py
response = self.model.generate_content(prompt)
return response.text
```

---

## 🐛 Debugging Checklist

**API not responding?**
- [ ] Backend running? (`uvicorn main:app --reload`)
- [ ] Port 8000 available? (`lsof -i :8000`)
- [ ] Check terminal for error messages

**Gemini API errors?**
- [ ] API key in backend/.env? (`echo $GEMINI_API_KEY`)
- [ ] Key is valid? (Check makersuite.google.com)
- [ ] Internet connection? 
- [ ] Rate limit? (50 req/min)

**Import errors?**
- [ ] Dependencies installed? (`pip install -r requirements.txt`)
- [ ] Virtual environment activated? (`source venv/bin/activate`)
- [ ] Python 3.8+? (`python --version`)

**Database errors?**
- [ ] .env file exists? (`ls backend/.env`)
- [ ] DATABASE_URL set? (`echo $DATABASE_URL`)
- [ ] Database exists?

---

## 📊 Project Structure at a Glance

```
FitnessCoachMVP/
├── backend/
│   ├── main.py              ← Start here
│   ├── models.py            ← Data structures
│   ├── services/
│   │   └── coach_service.py ← AI logic
│   └── routers/
│       ├── auth.py
│       ├── coach.py
│       └── progress.py
├── frontend/                ← React app
├── docs/
│   ├── README.md
│   ├── SETUP.md
│   ├── ARCHITECTURE.md
│   └── HACKATHON_GUIDE.md
├── test_api.py              ← Run tests
├── requirements.txt
├── .env                     ← Create this
├── .env.example
├── Makefile
└── FILE_GUIDE.md
```

---

## 🎯 File to Edit for Different Tasks

| Need to... | Edit file... |
|-----------|-------------|
| Add new API endpoint | `routers/*.py` |
| Add new data model | `models.py` |
| Change AI behavior | `services/coach_service.py` |
| Fix validation error | `models.py` |
| Change database config | `.env` |
| Add new dependency | `requirements.txt` |
| Change frontend URL | `frontend/src/services/api.js` |

---

## 🔑 Key Variables to Remember

```python
# Backend
GEMINI_API_KEY = "from_makersuite"
DATABASE_URL = "firebase:// or postgresql://"
USER_ID = "user_123"  # Auto-generated on signup

# Frontend
API_BASE_URL = "http://localhost:8000/api"
userId = localStorage.getItem('userId')
```

---

## 📈 Progress Checklist

### Week 1
- [ ] Backend running
- [ ] API endpoints working
- [ ] Test suite passing
- [ ] Database connected

### Week 2
- [ ] User authentication working
- [ ] Frontend scaffolding done
- [ ] Basic pages created
- [ ] API integration started

### Week 3
- [ ] All pages built
- [ ] Full end-to-end flow
- [ ] UI polished
- [ ] Performance optimized

### Week 4
- [ ] Deploy backend
- [ ] Deploy frontend
- [ ] User testing
- [ ] Bug fixes

### Hackathon Day
- [ ] Demo perfected
- [ ] Backup ready
- [ ] Presentation prepared
- [ ] Ship it! 🚀

---

## 💡 Pro Tips

1. **Always test locally first** - Use /docs endpoint
2. **Commit often** - Small, meaningful commits
3. **Keep .env secret** - Add to .gitignore
4. **Mock before real** - Build UI with fake data first
5. **Document as you go** - Future you will thank you
6. **Ask for help** - Hackathons are collaborative!

---

## 📚 Documentation Quick Links

Best for... | Read this
---|---
Getting started | README.md
Setup instructions | SETUP.md
System design | ARCHITECTURE.md
Frontend help | FRONTEND_SETUP.md
Winning tips | HACKATHON_GUIDE.md
File reference | FILE_GUIDE.md
This cheat sheet | QUICK_REFERENCE.md

---

## 🎬 Your First 30 Minutes

```bash
# 1. Get API key (5 min)
# Visit https://makersuite.google.com/app/apikey
# Click "Create API Key"

# 2. Clone/download project (1 min)
cd /Users/lucky/Documents/FitnessCoachMVP

# 3. Set up environment (5 min)
pip install -r requirements.txt
echo "GEMINI_API_KEY=your_key" > backend/.env

# 4. Start backend (2 min)
cd backend
uvicorn main:app --reload

# 5. Test everything (10 min)
# In new terminal:
python test_api.py

# 6. Celebrate ✅ (2 min)
# All tests passing? You're ready to build!
```

---

## 🆘 Emergency Commands

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null

# Kill process on port 8000
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Reset database
rm backend/fitness.db

# Start fresh
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

**Bookmark this file!** Save the URL or print it out. 📌

You've got this! Let's build something amazing! 🚀
