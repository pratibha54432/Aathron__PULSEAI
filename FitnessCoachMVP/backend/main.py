"""
Flask Backend for PULSEAI AGENT - Simplified Version (No Menstrual Cycle)
"""

import os
import requests
import json
from datetime import datetime, timedelta

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load env variables
load_dotenv("/Users/lucky/Documents/FitnessCoachMVP/.env")

# ===== INIT APP =====
app = Flask(__name__)
CORS(app)

# Mock database
users_db = {}
moods_db = {}
weight_logs_db = {}

# Cache for responses (5 hour TTL to keep it simple)
response_cache = {}

# ===== ROUTES =====

@app.route("/", methods=["GET"])
def root():
    return {"message": "Fitness Coach API running", "status": "ok"}, 200

@app.route("/health", methods=["GET"])
def health_check():
    return {"status": "healthy"}, 200

@app.route("/api/auth/signup", methods=["POST"])
def signup():
    """Register new user"""
    data = request.get_json() or {}
    email = data.get("email")
    
    if email in users_db:
        return {"error": "User already exists"}, 400
    
    user_id = f"user_{len(users_db) + 1}"
    users_db[email] = {
        "id": user_id,
        "name": data.get("name"),
        "email": email,
        "age": data.get("age"),
        "weight": data.get("weight"),
        "height": data.get("height"),
        "goal": data.get("goal"),
        "daily_time": data.get("daily_time")
    }
    
    return {
        "id": user_id,
        "name": data.get("name"),
        "email": email,
        "message": "User registered successfully"
    }, 200

@app.route("/api/auth/login", methods=["POST"])
def login():
    """Login user"""
    data = request.get_json() or {}
    email = data.get("email")
    
    if email not in users_db:
        return {"error": "Invalid credentials"}, 401
    
    return {
        "success": True,
        "user_id": users_db[email]["id"],
        "token": f"token_{users_db[email]['id']}"
    }, 200

@app.route("/api/coach/diet-plan", methods=["POST"])
def get_diet_plan():
    """Generate diet plan with Ollama based on mood"""
    data = request.get_json() or {}
    goal = data.get("goal", "maintenance")
    mood = data.get("mood", "neutral")
    age = data.get("age", 30)
    weight = data.get("weight", 70)
    height = data.get("height", 170)
    
    # Quick macros without complex calculations
    macros = {
        "weight_loss": {"calories": 1800, "protein": 130, "carbs": 180, "fats": 60},
        "muscle_gain": {"calories": 2500, "protein": 160, "carbs": 300, "fats": 80},
        "maintenance": {"calories": 2200, "protein": 110, "carbs": 275, "fats": 73}
    }
    
    goal_specs = macros.get(goal, macros["maintenance"])
    
    # Mood-based guidance
    mood_guidance = {
        "happy": "You're in a great mood! Suggest meals that are enjoyable and celebratory.",
        "stressed": "You're stressed. Focus on stress-reducing foods like dark chocolate, nuts, berries.",
        "tired": "You're tired. Suggest energy-boosting foods with complex carbs and healthy fats.",
        "energetic": "You're energetic! Suggest high-protein, nutrient-dense meals for peak performance.",
        "neutral": "Create a balanced, standard meal plan."
    }
    
    current_mood_guidance = mood_guidance.get(mood, mood_guidance["neutral"])
    
    prompt = f"""Create a personalized {goal} diet plan for someone who is currently feeling {mood}.

{current_mood_guidance}

Your Details:
- Goal: {goal.replace('_', ' ')}
- Target Calories: {goal_specs['calories']}
- Protein Target: {goal_specs['protein']}g
- Carbs Target: {goal_specs['carbs']}g
- Fats Target: {goal_specs['fats']}g

Create a daily meal plan with:
1. Breakfast (with calories)
2. Mid-morning snack (with calories)
3. Lunch (with calories)
4. Pre-workout snack (with calories)
5. Dinner (with calories)
6. Post-workout meal or evening snack (with calories)

Make it practical, delicious, and tailored to their mood."""
    
    try:
        ollama_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        model_name = os.getenv("OLLAMA_MODEL", "neural-chat")
        
        try:
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                plan_text = result.get("response", "")
                return {
                    "diet_plan": plan_text,
                    "goal": goal,
                    "mood": mood,
                    "calories": goal_specs['calories'],
                    "protein_g": goal_specs['protein'],
                    "source": "ollama"
                }, 200
        except requests.exceptions.Timeout:
            pass  # Fall through to default response
        except Exception as e:
            pass  # Fall through to default response
    except Exception as e:
        pass  # Fall through to default response
    
    # Fallback response if Ollama fails
    return {
        "diet_plan": f"Quick {goal} meal plan for {mood} mood: Breakfast (eggs + toast), Lunch (grilled chicken + rice), Dinner (salmon + sweet potato). Target: {goal_specs['calories']} calories, {goal_specs['protein']}g protein.",
        "goal": goal,
        "mood": mood,
        "calories": goal_specs['calories'],
        "protein_g": goal_specs['protein'],
        "source": "fallback"
    }, 200

@app.route("/api/coach/workout", methods=["POST"])
def get_workout():
    """Generate personalized workout with Ollama based on mood"""
    data = request.get_json() or {}
    goal = data.get("goal", "fitness")
    mood = data.get("mood", "neutral")
    available_time = data.get("available_time", 45)
    
    # Mood-based workout guidance
    mood_guidance = {
        "happy": "Create an energetic, fun workout with upbeat exercises. Include music-friendly movements.",
        "stressed": "Create a calming, stress-relieving workout. Include yoga, stretching, light cardio. Focus on mindfulness.",
        "tired": "Create a gentle, energizing workout that boosts energy. Moderate intensity with recovery focus.",
        "energetic": "Create a high-intensity, challenging workout that matches their energy level. Push them hard!",
        "neutral": "Create a balanced workout routine."
    }
    
    current_mood_guidance = mood_guidance.get(mood, mood_guidance["neutral"])
    
    prompt = f"""Create a {available_time}-minute personalized {goal} workout for someone who is currently feeling {mood}.

{current_mood_guidance}

REQUIREMENTS:
- Duration: {available_time} minutes
- Goal: {goal.replace('_', ' ')}
- Current Mood: {mood}
- Include warm-up (5 min), main exercises (3-4 with sets/reps), cool-down (5 min)
- Provide modifications for different fitness levels
- Make it safe, practical, and effective

Format with clear exercise names, sets, reps, rest periods, and any special notes for this mood."""
    
    try:
        ollama_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        model_name = os.getenv("OLLAMA_MODEL", "neural-chat")
        
        try:
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                workout_text = result.get("response", "")
                return {
                    "workout_plan": workout_text,
                    "duration": available_time,
                    "goal": goal,
                    "mood": mood,
                    "source": "ollama"
                }, 200
        except requests.exceptions.Timeout:
            pass  # Fall through to default response
        except Exception as e:
            pass  # Fall through to default response
    except Exception as e:
        pass  # Fall through to default response
    
    # Fallback response if Ollama fails
    fallback_workouts = {
        "happy": "Happy Workout: 5 min warm-up. Circuit (3 sets): 10 burpees, 15 jumping jacks, 10 mountain climbers. 5 min cool-down.",
        "stressed": "Stress Relief: Gentle yoga sequence. 5 min breathing exercises, 20 min flowing poses, 5 min meditation.",
        "tired": "Energy Boost: 5 min light cardio. 3 sets: 12 squats, 10 push-ups, 8 rows. 5 min stretching.",
        "energetic": "HIIT Challenge: 5 min warm-up. 4 rounds: 30 sec sprints, 30 sec rest. Main circuit: squats, push-ups, rows.",
        "neutral": "Standard Workout: 5 min warm-up. 3 sets: 10 squats, 15 push-ups, 10 rows. 5 min cool-down."
    }
    
    fallback_text = fallback_workouts.get(mood, fallback_workouts["neutral"])
    
    return {
        "workout_plan": fallback_text,
        "duration": available_time,
        "goal": goal,
        "mood": mood,
        "source": "fallback"
    }, 200

@app.route("/api/coach/chat", methods=["POST"])
def chat():
    """Chat with AI coach"""
    data = request.get_json() or {}
    message = data.get("message", "").lower()
    
    # Quick response map for common questions (instant response)
    quick_responses = {
        "muscle": "To build muscle: eat 1.6-2.2g protein per kg body weight, do resistance training 3-4x weekly, sleep 7-9 hours, and maintain a caloric surplus.",
        "weight loss": "For weight loss: create a 300-500 cal deficit, eat more protein to preserve muscle, do 150+ min cardio weekly, and stay consistent.",
        "breakfast": "Good breakfast options: eggs + toast + fruit, oatmeal + protein + berries, yogurt + granola + nuts, or smoothie with protein powder.",
        "workout": "Aim for 3-4 resistance training sessions weekly, 150+ min moderate cardio, 2 rest days, and proper recovery.",
        "protein": "Protein targets: 1.6-2.2g per kg for muscle gain, 0.8-1.2g per kg for maintenance, 1.2-1.6g per kg for weight loss.",
        "water": "Drink 3-4 liters daily. More if you exercise heavily. Urine color is a good indicator - pale yellow is ideal.",
        "recovery": "Recovery tips: sleep 7-9 hours, foam roll, stretch daily, eat protein post-workout, stay hydrated, manage stress.",
        "cardio": "Cardio: 150 min moderate (walking, cycling) OR 75 min high intensity (HIIT, running) weekly. Best with strength training.",
        "diet": "Balanced diet: 40% carbs, 30% protein, 30% fat. Whole foods > processed. Track intake if serious about goals.",
        "energy": "Low energy? Check sleep quality, eat balanced meals, stay hydrated, reduce stress, and ensure adequate carbs pre-workout."
    }
    
    # Search for keywords in message and return matching response
    for keyword, response in quick_responses.items():
        if keyword in message:
            return {"response": response}, 200
    
    # Default response if no match
    return {
        "response": "Great question! I'm a fitness coach. Ask me about fitness, nutrition, workouts, or recovery tips. Common topics: muscle gain, weight loss, diet, workouts, protein, cardio, or energy levels."
    }, 200

@app.route("/api/progress/log-weight", methods=["POST"])
def log_weight():
    """Log weight"""
    data = request.get_json() or {}
    user_id = data.get("user_id")
    weight = data.get("weight")
    
    key = f"{user_id}_{datetime.now().isoformat()}"
    weight_logs_db[key] = {"weight": weight, "date": datetime.now().isoformat()}
    
    return {"success": True, "weight": weight}, 200

@app.route("/api/progress/progress/<user_id>", methods=["GET"])
def get_progress(user_id):
    """Get user progress"""
    weights = [v['weight'] for k, v in weight_logs_db.items() if k.startswith(user_id)]
    
    return {
        "user_id": user_id,
        "weights": weights,
        "total_logs": len(weights)
    }, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
