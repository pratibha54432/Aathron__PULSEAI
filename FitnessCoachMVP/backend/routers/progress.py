"""
Progress Tracking Router
"""

from fastapi import APIRouter, HTTPException
from models import MoodData, ProgressTracker
from datetime import datetime

router = APIRouter()

# Mock database for progress
progress_db = {}
mood_history_db = {}

@router.post("/log-mood")
async def log_mood(user_id: str, mood: MoodData):
    """Log user mood and energy data"""
    if user_id not in mood_history_db:
        mood_history_db[user_id] = []
    
    mood_entry = {
        "mood_score": mood.mood_score,
        "energy_level": mood.energy_level,
        "sleep_hours": mood.sleep_hours,
        "stress_level": mood.stress_level,
        "timestamp": datetime.now()
    }
    mood_history_db[user_id].append(mood_entry)
    
    return {
        "success": True,
        "message": "Mood logged successfully",
        "data": mood_entry
    }

@router.get("/progress/{user_id}")
async def get_progress(user_id: str):
    """Get user progress and statistics"""
    if user_id not in mood_history_db:
        raise HTTPException(status_code=404, detail="No progress data found")
    
    moods = mood_history_db[user_id]
    
    # Calculate statistics
    avg_mood = sum(m["mood_score"] for m in moods) / len(moods)
    avg_energy = sum(m["energy_level"] for m in moods) / len(moods)
    avg_sleep = sum(m["sleep_hours"] for m in moods) / len(moods)
    
    return {
        "user_id": user_id,
        "total_logs": len(moods),
        "average_mood": round(avg_mood, 1),
        "average_energy": round(avg_energy, 1),
        "average_sleep": round(avg_sleep, 1),
        "mood_trend": "improving" if moods[-1]["mood_score"] > avg_mood else "declining",
        "recent_data": moods[-7:] if len(moods) > 7 else moods
    }

@router.post("/log-workout/{user_id}")
async def log_workout(user_id: str, workout_data: dict):
    """Log completed workout"""
    if user_id not in progress_db:
        progress_db[user_id] = {"workouts": [], "streak": 0}
    
    progress_db[user_id]["workouts"].append({
        "date": datetime.now(),
        "exercises": workout_data.get("exercises"),
        "duration": workout_data.get("duration"),
        "intensity": workout_data.get("intensity"),
        "notes": workout_data.get("notes", "")
    })
    
    # Update streak
    progress_db[user_id]["streak"] += 1
    
    return {
        "success": True,
        "message": "Workout logged",
        "current_streak": progress_db[user_id]["streak"]
    }

@router.get("/streak/{user_id}")
async def get_streak(user_id: str):
    """Get user workout streak"""
    if user_id not in progress_db:
        return {"streak": 0, "message": "No workouts logged yet"}
    
    return {
        "user_id": user_id,
        "current_streak": progress_db[user_id]["streak"],
        "total_workouts": len(progress_db[user_id]["workouts"])
    }

@router.post("/log-weight/{user_id}")
async def log_weight(user_id: str, weight: float):
    """Log weight update for progress tracking"""
    if user_id not in progress_db:
        progress_db[user_id] = {"weights": [], "streak": 0}
    
    progress_db[user_id]["weights"].append({
        "weight": weight,
        "date": datetime.now()
    })
    
    return {
        "success": True,
        "message": "Weight logged",
        "current_weight": weight
    }
