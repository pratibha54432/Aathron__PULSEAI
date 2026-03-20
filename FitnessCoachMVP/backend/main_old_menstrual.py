"""
Flask Backend for Fitness Coach MVP
Using Hugging Face Inference API for AI responses
"""

import os
import requests
import json
from datetime import datetime, timedelta

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load env variables from absolute path
load_dotenv("/Users/lucky/Documents/FitnessCoachMVP/.env")

# ===== INIT APP =====
app = Flask(__name__)
CORS(app)

# Mock database
users_db = {}
moods_db = {}
weight_logs_db = {}  # Track weight progress towards target

# Simple response cache (24hr TTL)
response_cache = {}
cache_ttl = 86400  # 24 hours

# ===== HELPER FUNCTIONS =====
def get_cache_key(endpoint, params):
    """Generate cache key from endpoint and parameters"""
    import hashlib
    params_str = json.dumps(params, sort_keys=True)
    return f"{endpoint}:{hashlib.md5(params_str.encode()).hexdigest()}"

def get_cached_response(cache_key):
    """Get response from cache if available and not expired"""
    if cache_key in response_cache:
        cached_data = response_cache[cache_key]
        if datetime.now() < cached_data['expires']:
            return cached_data['response']
        else:
            del response_cache[cache_key]
    return None

def cache_response(cache_key, response):
    """Cache response with TTL"""
    response_cache[cache_key] = {
        'response': response,
        'expires': datetime.now() + timedelta(seconds=cache_ttl)
    }

def require_json(*fields):
    """Decorator to validate required JSON fields"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return {"error": "Content-Type must be application/json"}, 400
            data = request.get_json()
            for field in fields:
                if field not in data:
                    return {"error": f"Missing required field: {field}"}, 400
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

# ===== ROUTES =====

@app.route("/", methods=["GET"])
def root():
    return {"message": "Fitness Coach API running", "status": "ok"}, 200

@app.route("/health", methods=["GET"])
def health_check():
    return {"status": "healthy"}, 200

@app.route("/api/auth/signup", methods=["POST"])
@require_json("name", "email", "age", "gender", "weight", "target_weight", "height", "goal", "daily_time", "diet_preference")
def signup():
    """Register new user"""
    data = request.get_json()
    email = data.get("email")
    
    if email in users_db:
        return {"error": "User already exists"}, 400
    
    user_id = f"user_{len(users_db) + 1}"
    users_db[email] = {
        "id": user_id,
        "name": data.get("name"),
        "email": email,
        "age": data.get("age"),
        "gender": data.get("gender"),
        "weight": data.get("weight"),
        "target_weight": data.get("target_weight"),
        "height": data.get("height"),
        "goal": data.get("goal"),
        "diet_preference": data.get("diet_preference"),
        "daily_time": data.get("daily_time")
    }
    
    return {
        "id": user_id,
        "name": data.get("name"),
        "email": email,
        "age": data.get("age"),
        "weight": data.get("weight"),
        "target_weight": data.get("target_weight"),
        "goal": data.get("goal"),
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
    """Generate AI diet plan using Ollama API considering menstrual phase and mood"""
    data = request.get_json() or {}
    user_id = data.get("user_id")
    goal = data.get("goal", "maintenance")
    diet_preference = data.get("diet_preference", "balanced")
    age = data.get("age", 30)
    weight = data.get("weight", 70)
    height = data.get("height", 170)
    menstrual_phase = data.get("menstrual_phase")
    mood = data.get("mood")
    
    # Check cache first
    cache_key = get_cache_key("diet-plan", {
        "goal": goal,
        "diet_preference": diet_preference,
        "age": age,
        "weight": weight,
        "height": height,
        "menstrual_phase": menstrual_phase,
        "mood": mood
    })
    cached = get_cached_response(cache_key)
    if cached:
        cached['cached'] = True
        return cached, 200
    
    try:
        # Call Ollama API for diet plan generation
        ollama_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        model_name = os.getenv("OLLAMA_MODEL", "neural-chat")
        
        # Calculate macro targets based on goal
        goal_specs = calculate_macro_targets(goal, weight, age, menstrual_phase)
        
        # Build phase-specific guidance
        phase_guidance = ""
        if menstrual_phase:
            phase_guidance = get_menstrual_phase_guidance(menstrual_phase)
        
        # Build mood-specific guidance
        mood_guidance = ""
        if mood:
            mood_guidance = get_mood_nutrition_guidance(mood)
        
        prompt = f"""You are an expert nutritionist and fitness coach.

GOAL: {goal.upper().replace('_', ' ')}
Weight: {weight} kg
Age: {age} years
Height: {height} cm
Diet Preference: {diet_preference}
{"Menstrual Phase: " + menstrual_phase.upper().replace('_', ' ') if menstrual_phase else ""}
{"Current Mood: " + mood.upper() if mood else ""}

TARGET MACROS FOR {goal.upper().replace('_', ' ')}:
- Daily Calories: {goal_specs['calories']}
- Protein: {goal_specs['protein']}g ({goal_specs['protein_percent']}%)
- Carbs: {goal_specs['carbs']}g ({goal_specs['carbs_percent']}%)
- Fats: {goal_specs['fats']}g ({goal_specs['fats_percent']}%)

{phase_guidance if phase_guidance else ""}

{mood_guidance if mood_guidance else ""}

CREATE A PERSONALIZED DAILY DIET PLAN including:
1. Daily calorie target: {goal_specs['calories']} calories (for {goal.replace('_', ' ')})
2. Macro breakdown: Protein {goal_specs['protein']}g, Carbs {goal_specs['carbs']}g, Fats {goal_specs['fats']}g
3. Specific meal suggestions with calories:
   - Breakfast (with calories)
   - Mid-morning snack (with calories)
   - Lunch (with calories)
   - Pre-workout snack (with calories)
   - Dinner (with calories)
   - Post-workout meal (with calories)
4. Hydration recommendations
5. Supplements recommendations (if needed for {goal.replace('_', ' ')})
6. Meal prep tips for {diet_preference} diet
{phase_guidance if phase_guidance else ""}
{mood_guidance if mood_guidance else ""}

Format: Use clear sections with meal names, food items, and calorie counts."""
        
        try:
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7,
                    "top_p": 0.9
                },
                timeout=15
            )
        except requests.exceptions.Timeout:
            return {
                "diet_plan": f"Quick tip: For {goal}, eat plenty of protein, whole grains, and vegetables. Aim for {goal_specs['calories']} calories daily.",
                "goal": goal,
                "message": "AI is busy, here's a quick tip"
            }, 200
        
        if response.status_code == 200:
            result = response.json()
            plan_text = result.get("response", "")
            response_data = {
                "diet_plan": plan_text,
                "goal": goal,
                "menstrual_phase": menstrual_phase,
                "mood": mood,
                "target_calories": goal_specs['calories'],
                "macros": {
                    "protein": f"{goal_specs['protein']}g",
                    "carbs": f"{goal_specs['carbs']}g",
                    "fats": f"{goal_specs['fats']}g"
                }
            }
            # Cache successful response
            cache_response(cache_key, response_data)
            return response_data, 200
        else:
            return {
                "error": f"Ollama API error: {response.status_code}",
                "diet_plan": "Failed to generate diet plan. Make sure Ollama is running."
            }, 500
    except requests.exceptions.ConnectionError:
        return {
            "error": "Cannot connect to Ollama",
            "diet_plan": "Failed to connect to Ollama API. Make sure Ollama is running with: ollama serve",
            "note": "Check OLLAMA_API_URL in .env"
        }, 500
    except Exception as e:
        return {
            "error": str(e),
            "diet_plan": f"Error generating diet plan: {str(e)}"
        }, 500

def calculate_macro_targets(goal: str, weight: float, age: int, menstrual_phase: str = None) -> dict:
    """Calculate calorie and macro targets based on goal and menstrual phase"""
    # Base metabolic rate approximation
    if age < 18:
        bmr = (13.871 * weight) + 660
    else:
        bmr = (10 * weight) + 625
    
    # Adjust for activity level (assuming moderate)
    tdee = bmr * 1.55
    
    # Adjust calories for menstrual phase
    phase_multiplier = 1.0
    if menstrual_phase == "menstruation":
        phase_multiplier = 1.05  # Slight calorie increase during menstruation
    elif menstrual_phase == "ovulation":
        phase_multiplier = 1.03  # Slight increase during ovulation
    
    tdee = tdee * phase_multiplier
    
    if goal == "fat_loss":
        calories = int(tdee * 0.85)  # 15% deficit
        return {
            "calories": calories,
            "protein": int(weight * 2.2),
            "carbs": int((calories * 0.40) / 4),
            "fats": int((calories * 0.25) / 9),
            "protein_percent": 35,
            "carbs_percent": 40,
            "fats_percent": 25
        }
    elif goal == "muscle_gain":
        calories = int(tdee * 1.15)  # 15% surplus
        return {
            "calories": calories,
            "protein": int(weight * 2.2),
            "carbs": int((calories * 0.50) / 4),
            "fats": int((calories * 0.25) / 9),
            "protein_percent": 25,
            "carbs_percent": 50,
            "fats_percent": 25
        }
    else:  # maintenance
        calories = int(tdee)
        return {
            "calories": calories,
            "protein": int(weight * 1.6),
            "carbs": int((calories * 0.45) / 4),
            "fats": int((calories * 0.30) / 9),
            "protein_percent": 30,
            "carbs_percent": 45,
            "fats_percent": 25
        }

def get_menstrual_phase_guidance(phase: str) -> str:
    """Get nutrition and training guidance for menstrual phase"""
    guidance = {
        "menstruation": """
MENSTRUATION PHASE GUIDANCE:
- Increase iron-rich foods (spinach, red meat, legumes) due to blood loss
- Prioritize magnesium sources (dark chocolate, almonds, spinach)
- Stay hydrated: drink at least 12-14 glasses of water daily
- Reduce high-impact exercises, focus on lighter cardio and stretching
- Increase carb intake slightly for energy support
- Consider iron supplementation if needed
- Avoid excessive caffeine which may increase cramping""",
        
        "follicular": """
FOLLICULAR PHASE GUIDANCE:
- Rising estrogen levels increase energy and strength capacity
- Good time for high-intensity workouts and heavy lifting
- Focus on protein to support muscle building
- Carbs are well-tolerated during this phase
- Include plenty of B vitamins from whole grains and vegetables
- This phase supports better sleep quality
- Good time for compound movements and challenging workouts""",
        
        "ovulation": """
OVULATION PHASE GUIDANCE:
- Peak energy and strength levels (best time for max efforts)
- Testosterone levels are elevated - ideal for strength training
- Calorie expenditure is naturally higher (can eat slightly more)
- Focus on challenging workouts and heavy compound lifts
- Maintain good hydration as body temperature increases slightly
- High-intensity interval training is very effective now
- Energy levels are optimal this week""",
        
        "luteal": """
LUTEAL PHASE GUIDANCE:
- Energy levels naturally decrease, adjust training accordingly
- Slightly increase calorie intake (200-300 extra calories)
- Increase complex carbs and serotonin-boosting foods
- Focus on strength training over high-intensity cardio
- Include magnesium-rich foods to support mood and energy
- Reduce stress through yoga, pilates, and lighter exercises
- Sleep may be more variable - prioritize sleep duration
- Lower intensity workouts are more sustainable this phase"""
    }
    return guidance.get(phase, "")

def get_mood_nutrition_guidance(mood: str) -> str:
    """Get nutrition guidance based on current mood"""
    guidance = {
        "happy": """
HAPPY MOOD - NUTRITION TIPS:
- Maintain regular meal timing to sustain energy
- Include mood-supporting foods: dark chocolate, berries, nuts
- Stay hydrated with water and herbal teas
- Good time to try new healthy recipes
- Focus on balanced macros to maintain positive state""",
        
        "stressed": """
STRESSED MOOD - NUTRITION TIPS:
- Avoid excessive caffeine which increases cortisol
- Include calming foods: nuts, seeds, dark chocolate, chamomile tea
- Increase magnesium-rich foods (spinach, almonds, pumpkin seeds)
- Eat regular meals to maintain stable blood sugar
- Include omega-3 rich foods (salmon, flax, walnuts)
- Reduce processed and high-sugar foods
- Focus on whole foods that are easier to digest""",
        
        "energetic": """
ENERGETIC MOOD - NUTRITION TIPS:
- Fuel this energy with challenging strength training sessions
- Focus on protein to support muscle building
- Include complex carbs for sustained energy
- Time carbs around workout for optimal performance
- Stay well-hydrated to maintain this energy level
- Consider a pre-workout meal about 1-2 hours before training
- Capitalize on this state for intense training blocks""",
        
        "tired": """
TIRED MOOD - NUTRITION TIPS:
- Eat more frequent, smaller meals to maintain energy
- Include iron-rich foods (spinach, lentils, beef)
- Increase complex carbs for steady energy release
- Add B-vitamin sources (eggs, whole grains, yogurt)
- Ensure adequate protein for sustained fullness
- Include energy-boosting snacks: nuts, dates, Greek yogurt
- Check calorie intake - may need more food
- Focus on sleep-supporting foods: tart cherry juice, kiwi""",
        
        "neutral": """
NEUTRAL MOOD - NUTRITION TIPS:
- Continue consistent healthy eating patterns
- Maintain balanced macronutrient distribution
- Stay hydrated throughout the day
- Include variety in your meals for all micronutrients
- Focus on whole, unprocessed foods
- Time meals around training sessions optimally
- Maintain consistent meal timing patterns"""
    }
    return guidance.get(mood, "")

@app.route("/api/coach/workout", methods=["POST"])
def get_workout():
    """Generate AI workout using Ollama API considering menstrual phase and mood"""
    data = request.get_json() or {}
    user_id = data.get("user_id")
    goal = data.get("goal", "fitness")
    available_time = data.get("available_time", 45)
    menstrual_phase = data.get("menstrual_phase")
    mood = data.get("mood")
    
    # Check cache first
    cache_key = get_cache_key("workout", {
        "goal": goal,
        "available_time": available_time,
        "menstrual_phase": menstrual_phase,
        "mood": mood
    })
    cached = get_cached_response(cache_key)
    if cached:
        cached['cached'] = True
        return cached, 200
    
    try:
        ollama_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        model_name = os.getenv("OLLAMA_MODEL", "neural-chat")
        
        # Get phase and mood-specific workout guidance
        phase_workout_guidance = get_menstrual_phase_workout_guidance(menstrual_phase) if menstrual_phase else ""
        mood_workout_guidance = get_mood_workout_guidance(mood) if mood else ""
        
        prompt = f"""You are a professional fitness trainer with expertise in female health and mood-based training.

WORKOUT REQUIREMENTS:
- Duration: {available_time} minutes
- Goal: {goal.replace('_', ' ')}
{f"- Menstrual Phase: {menstrual_phase.upper().replace('_', ' ')}" if menstrual_phase else ""}
{f"- Current Mood: {mood.upper()}" if mood else ""}

{phase_workout_guidance if phase_workout_guidance else ""}

{mood_workout_guidance if mood_workout_guidance else ""}

CREATE A {available_time}-MINUTE WORKOUT ROUTINE including:
- Warm-up (5 minutes) - light and progressive
- Main exercises (ideally 3-4):
  - Exercise name
  - Sets and reps (adjust intensity based on phase/mood)
  - Form tips and safety notes
  - Rest periods
  - Easier modification (if energy is low)
  - Harder progression (if energy is high)
- Cool-down and stretching (5 minutes)

Make it practical, safe, achievable in {available_time} minutes, and tailored to the current phase and mood."""
        
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7,
                "top_p": 0.9
            },
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            workout_text = result.get("response", "")
            
            # Determine intensity based on phase and mood
            intensity = get_workout_intensity(menstrual_phase, mood)
            
            response_data = {
                "workout_plan": workout_text,
                "duration": available_time,
                "goal": goal,
                "menstrual_phase": menstrual_phase,
                "mood": mood,
                "intensity": intensity
            }
            # Cache successful response
            cache_response(cache_key, response_data)
            return response_data, 200
        else:
            return {
                "error": f"Ollama API error: {response.status_code}",
                "workout_plan": "Failed to generate workout plan."
            }, 500
    except requests.exceptions.ConnectionError:
        return {
            "error": "Cannot connect to Ollama",
            "workout_plan": "Failed to connect to Ollama API. Make sure Ollama is running.",
            "duration": available_time
        }, 500
    except Exception as e:
        return {
            "error": str(e),
            "workout_plan": f"Error generating workout: {str(e)}",
            "duration": available_time
        }, 500

def get_menstrual_phase_workout_guidance(phase: str) -> str:
    """Get workout guidance for menstrual phase"""
    guidance = {
        "menstruation": """
MENSTRUATION PHASE WORKOUT GUIDANCE:
- Focus on low-impact activities: yoga, pilates, light walking, swimming
- Reduce high-intensity training and heavy lifting
- Prioritize recovery and gentle stretching
- Listen to your body - energy may be lower
- Stay well hydrated
- Reduce volume and intensity by 20-30%
- Consider restorative yoga or mobility work""",
        
        "follicular": """
FOLLICULAR PHASE WORKOUT GUIDANCE:
- Excellent time for progressive overload and challenging workouts
- Energy levels are rising - take advantage!
- Great for learning new skills and techniques
- Include varied workout types: strength, cardio, mobility
- This is your best week for performance improvements
- Can handle higher volume and intensity
- Good for setting PRs in lifts or cardio""",
        
        "ovulation": """
OVULATION PHASE WORKOUT GUIDANCE:
- PEAK PERFORMANCE WEEK - your strongest phase!
- This is the optimal time for maximum intensity training
- Push hard on compound lifts and challenging workouts
- High-intensity interval training (HIIT) is very effective now
- Testosterone levels support strength and muscle building
- Can lift heavier weights and handle more volume
- Great week for setting personal records""",
        
        "luteal": """
LUTEAL PHASE WORKOUT GUIDANCE:
- Energy naturally decreases - adjust training accordingly
- Focus on moderate-intensity strength training
- Reduce high-intensity cardio, prefer steady-state or strength
- Include stress-relieving workouts: yoga, pilates, walking
- Carb-loading becomes more important for energy
- Slightly lower strength capacity - don't push maximum efforts
- Prioritize consistency over intensity this week"""
    }
    return guidance.get(phase, "")

def get_mood_workout_guidance(mood: str) -> str:
    """Get workout guidance based on mood"""
    guidance = {
        "happy": """
HAPPY MOOD WORKOUT GUIDANCE:
- Perfect energy for challenging workouts
- Maintain high intensity and push yourself
- Great time for group classes or challenging sessions
- Can handle higher volume without overtraining risk
- Mood supports good form and focus
- Leverage this positive state for progress""",
        
        "stressed": """
STRESSED MOOD WORKOUT GUIDANCE:
- Use exercise for stress relief but keep intensity moderate
- Avoid very high-intensity training that could increase cortisol
- Focus on cardio, running, or rhythmic activities for stress relief
- Include mindful movement: yoga, tai chi, walking
- Use this as a mental health tool
- Aim for 30-45 minutes of sustained moderate cardio
- Keep form and technique controlled""",
        
        "energetic": """
ENERGETIC MOOD WORKOUT GUIDANCE:
- OPTIMAL TIME FOR INTENSE TRAINING!
- Push hard on strength training and conditioning
- Include high-intensity interval training (HIIT)
- Can handle higher volume and intensity
- Great time for challenging workouts or competitions
- Use this energy for maximum performance
- Challenge yourself with new PRs""",
        
        "tired": """
TIRED MOOD WORKOUT GUIDANCE:
- Keep intensity light to moderate
- Focus on movement rather than heavy lifting
- Walking, easy cycling, or low-impact cardio
- Include mobility and stretching
- Just 20-30 minutes of gentle activity
- Focus on moving rather than pushing
- Recovery and rest are priorities today
- Consider whether you need rest instead""",
        
        "neutral": """
NEUTRAL MOOD WORKOUT GUIDANCE:
- Maintain regular training intensity
- Stick to your planned workout program
- Mix moderate and challenging sessions
- Good day for technique work and skill development
- Balanced approach to training and recovery
- Maintain consistency in your routine"""
    }
    return guidance.get(mood, "")

def get_workout_intensity(menstrual_phase: str = None, mood: str = None) -> str:
    """Determine workout intensity based on menstrual phase and mood"""
    # Start with base intensity
    intensity_score = 5  # 1-10 scale
    
    if menstrual_phase:
        phase_intensity = {
            "menstruation": 2,
            "follicular": 7,
            "ovulation": 9,
            "luteal": 4
        }
        intensity_score = phase_intensity.get(menstrual_phase, 5)
    
    if mood:
        mood_intensity = {
            "happy": 8,
            "stressed": 4,
            "energetic": 9,
            "tired": 2,
            "neutral": 5
        }
        # Average the mood effect with phase
        mood_score = mood_intensity.get(mood, 5)
        intensity_score = (intensity_score + mood_score) // 2
    
    # Convert score to intensity level
    if intensity_score >= 8:
        return "high"
    elif intensity_score >= 6:
        return "moderate-high"
    elif intensity_score >= 4:
        return "moderate"
    elif intensity_score >= 2:
        return "light"
    else:
        return "very-light"

@app.route("/api/coach/mood-workout", methods=["POST"])
def get_mood_workout():
    """Get mood-based workout using Ollama API"""
    data = request.get_json() or {}
    user_id = data.get("user_id")
    mood = data.get("mood", "happy")
    energy_level = data.get("energy_level", 5)
    available_time = data.get("available_time", 30)
    
    # Check cache first
    cache_key = get_cache_key("mood-workout", {
        "mood": mood,
        "energy_level": energy_level,
        "available_time": available_time
    })
    cached = get_cached_response(cache_key)
    if cached:
        cached['cached'] = True
        return cached, 200
    
    try:
        ollama_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        model_name = os.getenv("OLLAMA_MODEL", "neural-chat")
        
        mood_adjustments = {
            "excellent": "High-intensity, challenging, strength-focused",
            "good": "Balanced workout with cardio and strength",
            "average": "Moderate intensity, consistent pace",
            "stressed": "Low-intensity, calming, yoga/stretching focused",
            "happy": "Energetic, fun, music-based exercises"
        }
        
        adjustment = mood_adjustments.get(mood.lower(), "Moderate intensity workout")
        
        prompt = f"""You are a fitness trainer who specializes in mood-based workouts.

CURRENT MOOD: {mood}
ENERGY LEVEL: {energy_level}/10
AVAILABLE TIME: {available_time} minutes
MOOD ADJUSTMENT: {adjustment}

Create a {available_time}-minute mood-matched workout that:
1. Matches the mood adjustment style: {adjustment}
2. Is appropriate for energy level {energy_level}/10
3. Includes warm-up (3-5 min), main workout, and cool-down
4. Has specific exercises with reps and sets
5. Provides modifications for different fitness levels

Make it achievable, motivating, and tailored to their current emotional/energy state."""
        
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7,
                "top_p": 0.9
            },
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            workout_text = result.get("response", "")
            response_data = {
                "workout_plan": workout_text,
                "mood": mood,
                "mood_match": "Matched to your mood and energy level",
                "energy_level": energy_level
            }
            # Cache successful response
            cache_response(cache_key, response_data)
            return response_data, 200
        else:
            return {
                "error": f"Ollama API error: {response.status_code}",
                "workout_plan": "Failed to generate mood-matched workout."
            }, 500
    except requests.exceptions.ConnectionError:
        return {
            "error": "Cannot connect to Ollama",
            "workout_plan": "Failed to connect to Ollama API. Make sure Ollama is running.",
            "energy_level": energy_level
        }, 500
    except Exception as e:
        return {
            "error": str(e),
            "workout_plan": f"Error generating mood-matched workout: {str(e)}",
            "energy_level": energy_level
        }, 500

@app.route("/api/progress/log-mood", methods=["POST"])
def log_mood():
    """Log mood and health data"""
    data = request.get_json() or {}
    user_id = data.get("user_id")
    
    key = f"{user_id}_{len(moods_db)}"
    moods_db[key] = {
        "user_id": user_id,
        "mood_score": data.get("mood_score", 5),
        "energy_level": data.get("energy_level", 5),
        "sleep_hours": data.get("sleep_hours", 8),
        "stress_level": data.get("stress_level", 3)
    }
    return {
        "success": True,
        "message": "Mood logged successfully",
        "id": key
    }, 200

@app.route("/api/progress/log-weight", methods=["POST"])
def log_weight():
    """Log weight progress towards target"""
    data = request.get_json() or {}
    user_id = data.get("user_id")
    current_weight = data.get("weight")
    menstrual_phase = data.get("menstrual_phase")
    
    if not user_id or current_weight is None:
        return {"error": "Missing user_id or weight"}, 400
    
    # Get user's target weight
    user_data = None
    for email, user_info in users_db.items():
        if user_info["id"] == user_id:
            user_data = user_info
            break
    
    if not user_data:
        return {"error": "User not found"}, 404
    
    target_weight = user_data.get("target_weight")
    initial_weight = user_data.get("weight")
    goal = user_data.get("goal")
    
    # Calculate progress towards target
    if goal == "fat_loss":
        weight_to_lose = initial_weight - target_weight
        weight_lost = initial_weight - current_weight
        progress_percent = (weight_lost / weight_to_lose * 100) if weight_to_lose > 0 else 0
    elif goal == "muscle_gain":
        weight_to_gain = target_weight - initial_weight
        weight_gained = current_weight - initial_weight
        progress_percent = (weight_gained / weight_to_gain * 100) if weight_to_gain > 0 else 0
    else:  # General fitness
        weight_diff = abs(target_weight - initial_weight)
        current_diff = abs(target_weight - current_weight)
        progress_percent = (1 - (current_diff / weight_diff) * 100) if weight_diff > 0 else 0
    
    key = f"{user_id}_{len(weight_logs_db)}"
    weight_logs_db[key] = {
        "user_id": user_id,
        "current_weight": current_weight,
        "target_weight": target_weight,
        "initial_weight": initial_weight,
        "goal": goal,
        "menstrual_phase": menstrual_phase,
        "progress_percent": max(0, min(100, progress_percent)),
        "timestamp": datetime.now().isoformat()
    }
    
    return {
        "success": True,
        "message": "Weight logged successfully",
        "current_weight": current_weight,
        "target_weight": target_weight,
        "initial_weight": initial_weight,
        "goal": goal,
        "menstrual_phase": menstrual_phase,
        "progress_percent": round(max(0, min(100, progress_percent)), 1),
        "id": key
    }, 200

@app.route("/api/progress/progress/<user_id>", methods=["GET"])
def get_progress(user_id):
    """Get user progress including mood and weight tracking"""
    user_moods = [m for k, m in moods_db.items() if k.startswith(user_id)]
    user_weights = [w for k, w in weight_logs_db.items() if k.startswith(user_id)]
    
    # Get user data for goal info
    user_data = None
    for email, user_info in users_db.items():
        if user_info["id"] == user_id:
            user_data = user_info
            break
    
    result = {
        "user_id": user_id,
        "total_mood_logs": len(user_moods),
        "total_weight_logs": len(user_weights),
        "goal": user_data.get("goal") if user_data else None,
        "initial_weight": user_data.get("weight") if user_data else None,
        "target_weight": user_data.get("target_weight") if user_data else None
    }
    
    # Mood statistics
    if user_moods:
        avg_mood = sum(m["mood_score"] for m in user_moods) / len(user_moods)
        avg_sleep = sum(m["sleep_hours"] for m in user_moods) / len(user_moods)
        result["avg_mood"] = round(avg_mood, 1)
        result["avg_sleep"] = round(avg_sleep, 1)
        result["mood_progress"] = "Great consistency!"
    else:
        result["avg_mood"] = 0
        result["avg_sleep"] = 0
        result["mood_progress"] = "No mood data yet"
    
    # Weight statistics
    if user_weights:
        latest_weight = user_weights[-1]
        result["current_weight"] = latest_weight.get("current_weight")
        result["weight_progress_percent"] = latest_weight.get("progress_percent", 0)
        result["weight_logs"] = user_weights
        
        # Calculate weight change
        first_weight = user_weights[0].get("current_weight")
        latest_weight_value = user_weights[-1].get("current_weight")
        weight_change = latest_weight_value - first_weight
        result["total_weight_change"] = round(weight_change, 1)
        
        if user_data and user_data.get("goal") == "fat_loss":
            result["weight_status"] = f"Lost {abs(weight_change):.1f} kg so far"
        elif user_data and user_data.get("goal") == "muscle_gain":
            result["weight_status"] = f"Gained {weight_change:.1f} kg so far"
        else:
            result["weight_status"] = f"Weight change: {weight_change:+.1f} kg"
    else:
        result["current_weight"] = None
        result["weight_progress_percent"] = 0
        result["weight_logs"] = []
        result["weight_status"] = "No weight data logged yet"
    
    return result, 200

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    """Get leaderboard ranked by goal, streak, and weight progress"""
    leaderboard_data = {}
    
    # Process each user
    for email, user_data in users_db.items():
        user_id = user_data.get("id")
        goal = user_data.get("goal", "general")
        
        # Get user's weight logs
        user_weights = [w for k, w in weight_logs_db.items() if k.startswith(user_id)]
        user_moods = [m for k, m in moods_db.items() if k.startswith(user_id)]
        
        if not user_weights and not user_moods:
            continue  # Skip users with no activity
        
        # Calculate weight progress
        if user_weights:
            first_weight = user_weights[0].get("current_weight", 0)
            latest_weight = user_weights[-1].get("current_weight", 0)
            weight_change = latest_weight - first_weight
        else:
            first_weight = user_data.get("weight", 0)
            latest_weight = user_data.get("weight", 0)
            weight_change = 0
        
        # Calculate streak (consecutive days with logs)
        streak = 0
        if user_weights:
            # Parse timestamps and count consecutive days
            today = datetime.now().date()
            
            dates_logged = set()
            for weight_log in user_weights:
                timestamp_str = weight_log.get("timestamp", "")
                if timestamp_str:
                    try:
                        log_date = datetime.fromisoformat(timestamp_str).date()
                        dates_logged.add(log_date)
                    except:
                        pass
            
            if dates_logged:
                # Count consecutive days backwards from today
                current_date = today
                for i in range(365):
                    if current_date in dates_logged:
                        streak += 1
                        current_date -= timedelta(days=1)
                    else:
                        break
        
        # Calculate score based on goal
        if goal == "fat_loss":
            # Lower weight is better -> negative weight_change is positive
            weight_progress = abs(weight_change) if weight_change < 0 else 0
            score = (weight_progress * 100) + (streak * 10)
        elif goal == "muscle_gain":
            # Higher weight is better -> positive weight_change is positive
            weight_progress = weight_change if weight_change > 0 else 0
            score = (weight_progress * 100) + (streak * 10)
        else:  # General fitness
            weight_progress = abs(weight_change)
            score = (weight_progress * 50) + (streak * 10)
        
        # Organize by goal
        if goal not in leaderboard_data:
            leaderboard_data[goal] = []
        
        leaderboard_data[goal].append({
            "rank": 0,  # Will be set after sorting
            "user_id": user_id,
            "name": user_data.get("name", "Unknown"),
            "score": round(score, 1),
            "streak": streak,
            "weight_progress": round(weight_progress, 1),
            "weight_change": round(weight_change, 1),
            "current_weight": round(latest_weight, 1),
            "target_weight": user_data.get("target_weight", 0),
            "num_logs": len(user_weights)
        })
    
    # Sort each goal category and assign ranks
    for goal in leaderboard_data:
        leaderboard_data[goal].sort(key=lambda x: (-x["score"], -x["streak"]))
        for idx, user in enumerate(leaderboard_data[goal], 1):
            user["rank"] = idx
    
    # Return organized leaderboard
    return {
        "leaderboard": leaderboard_data,
        "goals": list(leaderboard_data.keys()),
        "timestamp": datetime.now().isoformat()
    }, 200

@app.route("/api/coach/chat", methods=["POST"])
def coach_chat():
    """AI Coach chatbot using LOCAL Ollama AI (with graceful fallback)"""
    data = request.get_json() or {}
    user_id = data.get("user_id")
    message = data.get("message", "").lower().strip()
    mood = data.get("mood", "neutral")
    energy_level = data.get("energy_level", 5)
    
    # Get user info if available
    user_info = None
    for email, user in users_db.items():
        if user.get("id") == user_id:
            user_info = user
            break
    
    # Try Local Ollama AI first
    try:
        # Build context from user's fitness profile
        context = f"""You are an intelligent AI Fitness Coach. Respond in a friendly, motivating way. Keep responses to 2-3 sentences with practical fitness advice.

User Context:
- Current Mood: {mood}
- Energy Level: {energy_level}/10
"""
        
        if user_info:
            context += f"- Goal: {user_info.get('goal', 'fitness').replace('_', ' ')}\n"
            context += f"- Diet Preference: {user_info.get('diet_preference', 'balanced')}\n"
        
        full_prompt = f"""{context}
User Question: {message}

Coach Response: """
        
        # Call Local Ollama API (runs on localhost:11434)
        ollama_api_url = "http://localhost:11434/api/generate"
        payload = {
            "model": "neural-chat",
            "prompt": full_prompt,
            "stream": False,
            "temperature": 0.7
        }
        
        response = requests.post(ollama_api_url, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        generated_text = result.get("response", "").strip()
        
        if generated_text:
            return {
                "response": f"🤖 Coach: {generated_text}",
                "suggestions": ["📊 Log your workout", "🎯 Track your mood", "💧 Stay hydrated"],
                "source": "ollama-local"
            }, 200
    except requests.exceptions.Timeout:
        print("⏱️ Ollama timeout - using fallback")
    except requests.exceptions.ConnectionError:
        print("❌ Ollama not running on localhost:11434 - using fallback")
    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama Error: {str(e)}")
    except (ValueError, KeyError) as e:
        print(f"❌ Error parsing Ollama response: {str(e)}")
    
    # SMART FALLBACK RESPONSES - Context-aware coaching without API
    # ORDER MATTERS: Check RECOVERY first (most urgent), then SPECIFIC topics, then GENERAL
    fallback_responses = {
        # RECOVERY & HEALTH - Check first because these are critical
        "injury": "⚠️ Injuries need respect! Rest, ice, compress, elevate. See a doctor if pain persists. Modify workouts to work around it. Prevention > cure!",
        "sore": "😣 DOMS (muscle soreness) is normal! It means you worked hard. Use foam rolling, stretch, eat protein, stay hydrated. It'll pass in 3-5 days!",
        "pain": "⚠️ Don't push through pain! Assess the injury, rest if needed, and consult a doctor if severe. Focus on other body parts. Health comes first!",
        "tired": "😴 Low energy days happen! Do lighter workouts, prioritize sleep (7-9 hrs), hydrate, and eat nutrient-dense foods. Recovery is training too!",
        "tired": "😴 Low energy days happen! Do lighter workouts, prioritize sleep (7-9 hrs), hydrate, and eat nutrient-dense foods. Recovery is training too!",
        "recover": "🔄 Recovery = growth! Sleep 7-9 hrs, eat enough calories, stretch daily, take rest days. Active recovery (light walk, yoga) helps too!",
        "sleep": "😴 Sleep 7-9 hours nightly - it's when your body recovers and builds muscle! Consistent bedtime, dark room, no screens 1 hour before bed. Sleep is free gains!",
        "rest": "😴 Rest is crucial! Sleep 7-9 hours nightly. Take 1-2 rest days weekly. Muscles grow during recovery, not in the gym!",
        
        # SPECIFIC MINDSET & MOTIVATION
        "stuck": "💡 Hit a plateau? Change routine: new exercises, rep ranges, training split. Deload (lighter week) every 4-6 weeks to adapt and reset!",
        "fail": "🚀 You tried something hard and failed - that's success! Failure means you're pushing limits. Adjust, learn, try again. Every legend has failed!",
        "slow": "⏱️ Patience wins! Muscle building takes time - expect 1-2kg per month. Focus on consistency over quick results. Rome wasn't built in a day!",
        "goal": "🎯 Set SMART goals: Specific, Measurable, Achievable, Relevant, Time-bound. Break big goals into weekly milestones. Track progress!",
        "motivation": "💪 You're already here, that's huge! Every rep counts. Small progress is still progress. Focus on being 1% better each day. You've got amazing potential!",
        
        # VERY SPECIFIC NUTRITION (Check these before general ones)
        "breakfast": "🌅 Start strong! Try eggs (protein), oatmeal (carbs), banana (potassium). Avoid sugary cereals. A balanced breakfast boosts energy and metabolism!",
        "lunch": "🍱 Mid-day fuel: chicken/fish + brown rice + veggies. Balanced macros keep energy high. Prep meals on Sunday for consistency!",
        "dinner": "🌙 Light but nutritious: lean protein + salad + sweet potato. Eat 2-3 hrs before bed. Avoid heavy meals late night!",
        "protein": "🍗 Protein is crucial! Eat 1.6-2.2g per kg body weight daily. Sources: chicken, fish, eggs, greek yogurt, lentils. Distribute across meals!",
        "carb": "🍚 Carbs fuel workouts! Choose complex: oats, rice, sweet potato, quinoa. Time carbs around training for best performance!",
        "fat": "🥑 Healthy fats matter! Include avocado, nuts, olive oil, fatty fish. They support hormones and energy. Don't fear fat!",
        "water": "💧 Water is essential! Drink 0.5-1L per 100kg body weight. More if you're working out. Stay hydrated for better performance!",
        "macro": "📈 Master macros: Protein (muscle building), Carbs (energy), Fat (hormones). Adjust based on goals. Track with MyFitnessPal!",
        "snack": "🍎 Smart snacks: almonds, greek yogurt, apple with almond butter. Avoid chips/candy. Snacks should fuel, not derail!",
        
        # MEDIUM SPECIFICITY NUTRITION
        "meal": "🥗 Every meal matters! Follow the plate rule: 40% protein, 40% carbs, 20% healthy fats. Track your intake for best results!",
        "nutrition": "📊 Nutrition drives results! Track macros: 1.6-2.2g protein/kg body weight, carbs for energy, healthy fats. Consistency > perfection!",
        "diet": "🥗 Eat whole foods: lean proteins, veggies, fruits, and complex carbs. Avoid processed food. Stay consistent and track your intake. Nutrition is 70% of your results!",
        
        # SPECIFIC WORKOUT KEYWORDS
        "strength": "🏋️ Build strength: heavy compounds (squats, deadlifts, bench press), 4-6 reps, 3-4x/week. Progressive overload is key!",
        "muscle": "💪 Great! Focus on compound lifts like squats, deadlifts, and bench press. Eat 1.6-2.2g protein per kg of body weight and hit the gym 4-5 days a week. You've got this!",
        "exercise": "💪 Varied exercises = better results! Mix compound lifts (strength) + isolation (pump) + cardio (endurance). 4-5 days/week is ideal!",
        "weight": "⚖️ Consistent calorie deficit is key! Aim for 500-1000 cal deficit per day, combine cardio with strength training, and track your meals. Progress over perfection!",
        "reps": "📊 Rep ranges matter: 1-5 reps (strength), 6-12 (hypertrophy/muscle), 12+ (endurance). Match reps to your goals!",
        "set": "🔄 Train with intention: 3-4 sets per exercise, rest 60-90 secs between sets. Quality over quantity!",
        "cardio": "🏃 30-40 mins moderate cardio 3-4x/week or HIIT 2x/week. Mix it up: running, cycling, swimming. Cardio + strength = best results!",
        "stretch": "🧘 Stretch 10-15 mins daily post-workout for flexibility. Focus on tight areas: hamstrings, hips, shoulders. Yoga 1-2x/week works great too!",
        
        # GENERAL KEYWORDS (Least specific - checked last)
        "workout": "🏃 Start with 30 mins of cardio + strength training 3x/week. As you progress, increase volume gradually. Rest days are crucial for recovery. Keep pushing!",
        "gym": "🏋️ Hit the gym 4-5 days/week. Warm up 5-10 mins, train 45-60 mins, cool down. Progressive overload + consistency = gains!",
        "food": "🥗 Food is fuel! Prioritize: lean proteins, complex carbs, healthy fats, colorful veggies. Stay hydrated with 2-3L water daily!",
        "eat": "🍽️ Eat whole foods: chicken, fish, eggs, beans, rice, veggies, fruits. Cook at home more often. Clean eating = clean gains!",
    }
    
    # Match keywords in message to provide relevant response
    response_text = "🤖 Coach: Keep pushing towards your goals! Every workout brings you closer to success. You've got team spirit! 💪"
    for keyword, response in fallback_responses.items():
        if keyword in message:
            response_text = f"🤖 Coach: {response}"
            break
    
    return {
        "response": response_text,
        "suggestions": [
            "📊 Log your workout",
            "🎯 Track your mood",
            "💧 Stay hydrated"
        ]
    }, 200

# ===== ERROR HANDLERS =====
@app.errorhandler(404)
def not_found(error):
    return {"error": "Endpoint not found"}, 404

@app.errorhandler(500)
def server_error(error):
    return {"error": "Internal server error"}, 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
