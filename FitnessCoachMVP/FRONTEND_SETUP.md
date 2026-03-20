# Frontend Setup Guide - React

## Quick Create React App

```bash
# Navigate to project root
cd /Users/lucky/Documents/FitnessCoachMVP

# Create React app (if not already created)
npx create-react-app frontend

# Install dependencies
cd frontend
npm install axios react-router-dom

# Start dev server
npm start
```

## Recommended Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Onboarding.js         # User signup form
│   │   ├── Dashboard.js          # Main dashboard
│   │   ├── ChatCoach.js          # AI chat interface
│   │   ├── DietPlanner.js        # Diet plan display
│   │   ├── WorkoutPlanner.js     # Workout display
│   │   ├── MoodTracker.js        # Mood logging
│   │   ├── Progress.js           # Progress analytics
│   │   ├── Leaderboard.js        # Rankings
│   │   └── MenstrualCycle.js    # Women's health tracking
│   ├── pages/
│   │   ├── LoginPage.js
│   │   ├── DashboardPage.js
│   │   └── SettingsPage.js
│   ├── services/
│   │   └── api.js                # Axios backend calls
│   ├── App.js                    # Main app component
│   ├── index.js                  # React entry point
│   └── App.css                   # Styles
├── public/
│   └── index.html
└── package.json
```

## API Integration Service

Create `frontend/src/services/api.js`:

```javascript
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Authentication
export const auth = {
  signup: (userData) => api.post('/auth/signup', userData),
  login: (email, password) => api.post('/auth/login', { email, password }),
  logout: (userId) => api.post('/auth/logout', { user_id: userId })
};

// AI Coaching
export const coach = {
  chat: (userId, message) => 
    api.post('/coach/chat', { user_id: userId, message }),
  
  getDiet: (userId, goal, preferences) => 
    api.post('/coach/diet-plan', { 
      user_id: userId, 
      goal, 
      diet_preference: preferences 
    }),
  
  getWorkout: (userId, goal, time) => 
    api.post('/coach/workout', { 
      user_id: userId, 
      goal, 
      available_time: time 
    }),
  
  getMoodWorkout: (userId, mood, energy) => 
    api.post('/coach/mood-workout', { 
      user_id: userId, 
      mood, 
      energy_level: energy 
    }),
  
  getHistory: (userId) => 
    api.get(`/coach/history/${userId}`)
};

// Progress Tracking
export const progress = {
  logMood: (userId, moodData) => 
    api.post('/progress/log-mood', { 
      user_id: userId, 
      ...moodData 
    }),
  
  logWorkout: (userId, workoutData) => 
    api.post(`/progress/log-workout/${userId}`, workoutData),
  
  logWeight: (userId, weight) => 
    api.post(`/progress/log-weight/${userId}`, { weight }),
  
  getProgress: (userId) => 
    api.get(`/progress/progress/${userId}`),
  
  getStreak: (userId) => 
    api.get(`/progress/streak/${userId}`)
};

export default api;
```

## Sample Components

### Onboarding Component

```javascript
import React, { useState } from 'react';
import { auth } from '../services/api';

function Onboarding() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    age: '',
    gender: 'male',
    weight: '',
    height: '',
    goal: 'weight_loss',
    budget: 'low',
    daily_time: 30,
    profession: '',
    diet_preference: 'balanced',
    disabilities: [],
    diseases: []
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await auth.signup(formData);
      localStorage.setItem('userId', response.data.id);
      // Redirect to dashboard
      window.location.href = '/dashboard';
    } catch (error) {
      alert('Error: ' + error.response.data.detail);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Join FitnessCoach</h2>
      
      <input
        type="text"
        name="name"
        placeholder="Full Name"
        value={formData.name}
        onChange={handleChange}
        required
      />
      
      <input
        type="email"
        name="email"
        placeholder="Email"
        value={formData.email}
        onChange={handleChange}
        required
      />
      
      <input
        type="number"
        name="age"
        placeholder="Age"
        value={formData.age}
        onChange={handleChange}
        required
      />
      
      <select name="goal" value={formData.goal} onChange={handleChange}>
        <option value="weight_loss">Weight Loss</option>
        <option value="muscle_gain">Muscle Gain</option>
        <option value="fitness">Get Fit</option>
        <option value="endurance">Build Endurance</option>
      </select>
      
      <select name="diet_preference" value={formData.diet_preference} onChange={handleChange}>
        <option value="balanced">Balanced</option>
        <option value="vegetarian">Vegetarian</option>
        <option value="vegan">Vegan</option>
        <option value="keto">Keto</option>
      </select>
      
      <button type="submit">Start Your Journey</button>
    </form>
  );
}

export default Onboarding;
```

### Mood Tracker Component

```javascript
import React, { useState } from 'react';
import { progress } from '../services/api';

function MoodTracker() {
  const userId = localStorage.getItem('userId');
  const [moodData, setMoodData] = useState({
    mood_score: 5,
    energy_level: 5,
    sleep_hours: 7,
    stress_level: 5
  });

  const handleSlider = (e) => {
    const { name, value } = e.target;
    setMoodData(prev => ({
      ...prev,
      [name]: parseFloat(value)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await progress.logMood(userId, moodData);
      alert('Mood logged! Getting personalized workout...');
      // Could trigger mood-based workout here
    } catch (error) {
      alert('Error logging mood');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>How are you feeling?</h3>
      
      <label>
        Mood: {moodData.mood_score}/10
        <input
          type="range"
          name="mood_score"
          min="1"
          max="10"
          value={moodData.mood_score}
          onChange={handleSlider}
        />
      </label>
      
      <label>
        Energy: {moodData.energy_level}/10
        <input
          type="range"
          name="energy_level"
          min="1"
          max="10"
          value={moodData.energy_level}
          onChange={handleSlider}
        />
      </label>
      
      <label>
        Sleep: {moodData.sleep_hours}h
        <input
          type="range"
          name="sleep_hours"
          min="0"
          max="12"
          step="0.5"
          value={moodData.sleep_hours}
          onChange={handleSlider}
        />
      </label>
      
      <label>
        Stress: {moodData.stress_level}/10
        <input
          type="range"
          name="stress_level"
          min="1"
          max="10"
          value={moodData.stress_level}
          onChange={handleSlider}
        />
      </label>
      
      <button type="submit">Log & Get Recommendation</button>
    </form>
  );
}

export default MoodTracker;
```

### AI Workout Planner Component

```javascript
import React, { useState } from 'react';
import { coach } from '../services/api';

function WorkoutPlanner() {
  const userId = localStorage.getItem('userId');
  const [workout, setWorkout] = useState(null);
  const [loading, setLoading] = useState(false);
  const [goal, setGoal] = useState('muscle_gain');
  const [time, setTime] = useState(45);

  const getWorkout = async () => {
    setLoading(true);
    try {
      const response = await coach.getWorkout(userId, goal, time);
      setWorkout(response.data);
    } catch (error) {
      alert('Error getting workout');
    }
    setLoading(false);
  };

  return (
    <div>
      <h3>Your Personal Workout</h3>
      
      <select value={goal} onChange={(e) => setGoal(e.target.value)}>
        <option value="muscle_gain">Muscle Gain</option>
        <option value="weight_loss">Weight Loss</option>
        <option value="endurance">Endurance</option>
      </select>
      
      <input
        type="number"
        value={time}
        onChange={(e) => setTime(parseInt(e.target.value))}
        placeholder="Time available (minutes)"
      />
      
      <button onClick={getWorkout} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Workout'}
      </button>
      
      {workout && (
        <div className="workout-display">
          <h4>{workout.workout_plan}</h4>
          <p>Duration: {workout.duration} minutes</p>
          <p>Intensity: {workout.intensity}</p>
        </div>
      )}
    </div>
  );
}

export default WorkoutPlanner;
```

## Styling Tips

Use a CSS-in-JS solution or create App.css with:

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  color: #333;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

form {
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.1);
  max-width: 500px;
  margin: 20px auto;
}

input, select, textarea {
  width: 100%;
  padding: 12px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
}

button {
  width: 100%;
  padding: 12px;
  margin: 10px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s;
}

button:hover {
  transform: translateY(-2px);
}

.dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

.progress-chart {
  height: 300px;
  margin: 20px 0;
}
```

## Connect to Backend

Update `frontend/src/services/api.js` to match your backend URL:

```javascript
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
```

Then create `.env` file in frontend:

```
REACT_APP_API_URL=http://localhost:8000/api
```

## Running Frontend + Backend Together

Terminal 1:
```bash
cd /Users/lucky/Documents/FitnessCoachMVP/backend
uvicorn main:app --reload
```

Terminal 2:
```bash
cd /Users/lucky/Documents/FitnessCoachMVP/frontend
npm start
```

Frontend will run on http://localhost:3000
Backend will run on http://localhost:8000

---

## Next: Deploy Frontend

Once working locally:

1. **To Vercel:**
   - Push to GitHub
   - Import repo to vercel.com
   - Set `REACT_APP_API_URL` to your deployed backend URL

2. **To Netlify:**
   - Build: `npm run build`
   - Deploy `build/` folder to Netlify

---

For tips on specific components or styling, check the original frontend at `/Users/lucky/Documents/FitnessCoach/`
