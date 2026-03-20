# ✅ PRE-DEMO CHECKLIST (Do This NOW)

**Time remaining: ~8 hours. Follow this checklist in order.**

---

## 🔧 SETUP VERIFICATION (Next 30 minutes)

### Check Backend is Running
```bash
# Terminal 1 - Start backend
cd /Users/lucky/Documents/FitnessCoachMVP/backend
uvicorn main:app --reload

# Should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# ✅ If you see this, backend is ready
```

### Check Frontend is Running
```bash
# Terminal 2 - Check if React is running
# If NOT running yet, start it:
cd /Users/lucky/Documents/FitnessCoachMVP/frontend
npm start

# Should see:
# Compiled successfully!
# ✅ If you see this, frontend is ready
```

### Verify API Works
```bash
# Terminal 3 - Test API
cd /Users/lucky/Documents/FitnessCoachMVP
python test_api.py

# Should see green ✅ checkmarks for:
# ✅ PASS | User Registration
# ✅ PASS | Diet Plan Generation
# ✅ PASS | Workout Generation
# ✅ PASS | Mood Tracking
# ✅ PASS | Mood-Based Workout
# ✅ PASS | Progress Tracking
```

**If anything FAILS:**
- Check SETUP.md troubleshooting
- Make sure .env has GEMINI_API_KEY
- Restart all terminals
- Call me immediately if stuck

---

## 📋 PRE-DEMO SETUP (2 hours before 4 AM = 2 AM)

### Prepare Your Laptop

- [ ] Plug laptop into power (don't rely on battery!)
- [ ] Close ALL unnecessary apps (especially Slack, Discord, Zoom)
- [ ] Close all browser tabs except what you need
- [ ] Restart your computer (clear RAM, fresh start)
- [ ] Disable all notifications (system-wide)
- [ ] Turn off auto-updates

### Arrange Your Screen

**Arrange like this:**
```
┌─────────────────────────────────┐
│   Chrome Browser (full screen)   │
│   http://localhost:3000          │
│   (Your React app)              │
└─────────────────────────────────┘
```

Have as side windows:
- [ ] Terminal showing `npm start` running
- [ ] Terminal showing `uvicorn` running
- [ ] This demo script open somewhere

### Pre-Load Test Data

**Before judges arrive, have already:**

1. **Run through the ENTIRE demo once locally** (no judges watching)
   - Fill signup form
   - Generate diet plan
   - Log mood
   - Get mood workout
   - Check progress

2. **Screenshot each "wow moment":**
   - Save screenshot of generated diet plan
   - Save screenshot of mood-adapted workout
   - Save screenshot of progress chart
   - Save these somewhere accessible as backup

3. **Pre-fill the form with sample data:**
   - Either use browser DevTools to pre-fill
   - Or have notepad ready with: Name: "Alex", Age: 25, Goal: "Muscle Gain", etc.
   - Goal: Minimize typing during live demo

### Test the "Wow Moments"

Run these exact sequences and verify they work:

**Sequence 1: Diet Generation**
```
1. Click "Generate Diet Plan"
2. Should return within 5 seconds
3. Should show calories and macros
4. Should be vegetarian (NOT meat)
✅ PASS: Take screenshot
```

**Sequence 2: Mood Adaptation**
```
1. Log mood as: 3/10, Energy: 2/10, Stress: 8/10
2. Click "Get Mood Workout"
3. Should return yoga/stretching (NOT HIIT)
4. Should mention stress relief
✅ PASS: Take screenshot
```

**Sequence 3: Different Mood Different Result**
```
1. Log mood as: 9/10, Energy: 9/10, Stress: 2/10
2. Click "Get Mood Workout"
3. Should return high-intensity (cardio/strength)
4. Should be totally different from sequence 2
✅ PASS: This proves it's real AI, not hardcoded!
```

---

## 🎯 JUDGE ROOM SETUP (45 minutes before 4 AM = 3:15 AM)

### Arrange Your Physical Setup

- [ ] Position laptop so judges can see screen clearly
- [ ] Laptop screen should be at eye level (don't sit too low)
- [ ] Have mouse/trackpad ready (no clunky typing)
- [ ] Water bottle nearby (you might get dry mouth)
- [ ] Have printed script as backup reference (but don't look at it much)

### Screen Display Settings

```bash
# Go to System Preferences > Displays
# Set:
# - Resolution: Default
# - Brightness: 100%
# - Font size: Large (judges need to see)

# In Chrome:
# - Zoom: 120% (easier for judges to read)
# - Full screen preferred
```

### Have Backup Demo Ready

**In case something crashes, have:**
- [ ] Screenshots of each screen ready to show
- [ ] Pre-recorded 2-minute demo video on USB drive
- [ ] URL to http://localhost:8000/docs (interactive API docs)
- [ ] Code open in VSCode showing the architecture

---

## 🕐 FINAL HOUR (3 AM - 4 AM)

### 3:00 AM
- [ ] Already ate breakfast
- [ ] Already slept (or at minimum, rested)
- [ ] Back at your laptop
- [ ] Terminals all running (backend, frontend)
- [ ] Browser showing your app on localhost:3000

### 3:15 AM
- [ ] Do ONE more full demo run (practice)
- [ ] Check all "wow moments" work
- [ ] Verify screenshots are available
- [ ] Check your internet connection is stable

### 3:30 AM
- [ ] Read through DEMO_SCRIPT_5MIN.md one more time
- [ ] Practice key phrases out loud:
  - "How are you feeling?"
  - "This is real AI, not hardcoded"
  - "Notice this workout changed completely"
  - "The future of fitness is empathetic AI"

### 3:45 AM
- [ ] Close all unnecessary apps
- [ ] Position laptop for judges to see
- [ ] Take 3 deep breaths
- [ ] Smile
- [ ] You're ready

### 3:55 AM
- [ ] Judges should be arriving
- [ ] Greet them warmly
- [ ] Don't explain too much yet
- [ ] Just say: "Let me show you something cool"

---

## 🚨 EMERGENCY BACKUP PLANS

### If Backend Server Crashes
```
Plan A: Restart it
$ cd backend
$ uvicorn main:app --reload

Plan B: Show the API docs instead
Go to http://localhost:8000/docs
"Let me show you the production-ready API design"
Test endpoints directly in Swagger UI
```

### If Frontend Won't Load
```
Plan A: Hard refresh
Cmd + Shift + R (clears cache and reloads)

Plan B: Show frontend code
Open VSCode → frontend/src/components
"Here's the React code that makes this work"
Show component structure
```

### If Gemini API Doesn't Respond
```
Plan A: Check internet connection
Make sure WiFi is working

Plan B: Use backup screenshots
Show pre-captured screenshots of responses
"This is what the AI generated — I can show you the code"

Plan C: Show the code architecture
Open coach_service.py
Explain the prompt engineering
```

### If You Forget What to Say Next
```
✅ Just pause silently for 2 seconds
✅ Take a sip of water
✅ Look back at your printed demo script
✅ Continue calmly
✅ Judges will respect you for staying composed
```

---

## 📊 TIMING VERIFICATION

**Before demo, practice with a timer:**

```bash
# In terminal:
time bash << 'EOF'
# Go through entire demo:
# 1. Open app
# 2. Signup
# 3. Generate diet
# 4. Log mood
# 5. Get mood workout
# 6. Show progress
EOF

# Should take approximately 5-6 minutes total
# If longer, identify what to speed up
```

---

## 🎤 VOICE & DELIVERY CHECK

Do this 30 minutes before demo:

- [ ] Read DEMO_SCRIPT_5MIN.md out loud (2 times)
- [ ] Time yourself (should be ~5 minutes)
- [ ] Check you're not rushing
- [ ] Check you're pronouncing technical terms correctly
- [ ] Record yourself on phone and listen back
- [ ] Did you sound confident? Adjust tone if needed.

---

## ✨ FINAL VISUAL POLISH

**Your appearance matters:**

- [ ] Get a good night's sleep before (or at least 2-3 hours)
- [ ] Wear clean, professional-looking clothes
- [ ] Light breakfast (not too heavy, not empty stomach)
- [ ] Brush teeth
- [ ] No distracting t-shirts (keep it professional)
- [ ] Neat hair/appearance

**Judges remember first impression. You want them thinking "this is a real product team" not "these are college kids juggling code."**

---

## 🏁 YOU'RE READY CHECKLIST

Before judges arrive, verify:

- [ ] Backend running
- [ ] Frontend running
- [ ] API endpoints working
- [ ] All "wow moments" tested
- [ ] Screenshots saved as backup
- [ ] Demo script printed nearby
- [ ] Laptop on power
- [ ] All other apps closed
- [ ] Notifications silenced
- [ ] You slept 2+ hours
- [ ] You ate breakfast
- [ ] You feel confident

**If everything above has a checkmark, you're going to crush this.** 🚀

---

## 🎯 ABSOLUTE FINAL CHECKLIST (15 Min Before)

```
1. Is backend server running? YES/NO
2. Is frontend running? YES/NO
3. Can you see the app at localhost:3000? YES/NO
4. Did you practice the demo once already? YES/NO
5. Do you have screenshots of failures as backup? YES/NO
6. Are judges arriving soon? YES/NO
7. Do you feel ready? YES/NO

If ANY NO → Fix it now. Don't start demo until all YES.
```

---

**Print this checklist. Check off each item. Execute.**

**You've built something real. Now show it confidently.** 💪

**See you at 4 AM. You've got this.** 🏆
