"""
Coach Router - API endpoints for AI coaching
"""

from fastapi import APIRouter, HTTPException, Depends
from models import ChatResponse, CoachRequest, DietPlan, WorkoutPlan, Mood
from services.coach_service import coach_ai
from typing import Optional
from datetime import datetime

router = APIRouter()

# Mock user data (in production, fetch from database)
mock_users = {
    "user1": {
        "name": "John",
        "age": 28,
        "goal": "fat_loss",
        "fitness_level": "intermediate",
        "daily_time": 60,
        "budget": "medium",
        "diet_preference": "non_veg",
        "disabilities": None,
        "weight": 85,
        "gender": "Male",
        "mood": "good",
        "energy": 8,
        "sleep_hours": 7,
        "equipment": ["dumbbells", "barbell", "treadmill"]
    }
}

async def get_user_data(user_id: str) -> dict:
    """Get user data from database (mocked)"""
    if user_id not in mock_users:
        raise HTTPException(status_code=404, detail="User not found")
    return mock_users[user_id]

# ===== CHAT ENDPOINT =====
@router.post("/chat", response_model=ChatResponse)
async def chat_with_coach(
    user_id: str,
    message: str,
    user_data: dict = Depends(get_user_data)
):
    """
    Chat with the AI fitness coach
    
    Request params:
    - user_id: User ID
    - message: User's message to coach
    
    Returns: ChatResponse with coach's response
    """
    try:
        response = await coach_ai.chat_with_coach(user_data, message)
        
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        
        return ChatResponse(
            response=response["response"],
            type=response["type"],
            timestamp=response["timestamp"],
            context_used={"user_id": user_id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== DIET PLAN ENDPOINT =====
@router.post("/generate-diet")
async def generate_diet_plan(
    user_id: str,
    user_data: dict = Depends(get_user_data)
):
    """
    Generate personalized diet plan
    
    Returns: Personalized diet plan with meals, macros, and tips
    """
    try:
        plan = await coach_ai.generate_diet_plan(user_data)
        
        if "error" in plan:
            raise HTTPException(status_code=500, detail=plan["error"])
        
        return {
            "success": True,
            "user_id": user_id,
            "plan": plan["plan"],
            "timestamp": datetime.now(),
            "type": "diet_plan",
            "menstrual_adapted": user_data.get('gender') == 'Female'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== WORKOUT PLAN ENDPOINT =====
@router.post("/generate-workout")
async def generate_workout_plan(
    user_id: str,
    equipment: Optional[list] = None,
    user_data: dict = Depends(get_user_data)
):
    """
    Generate personalized workout plan
    
    Params:
    - user_id: User ID
    - equipment: Available equipment (optional)
    
    Returns: Structured workout plan with exercises, sets, reps, and form videos
    """
    try:
        if equipment:
            user_data['equipment'] = equipment
        
        workout = await coach_ai.generate_workout_plan(user_data)
        
        if "error" in workout:
            raise HTTPException(status_code=500, detail=workout["error"])
        
        return {
            "success": True,
            "user_id": user_id,
            "workout": workout["plan"],
            "duration": user_data.get('daily_time'),
            "difficulty": user_data.get('fitness_level'),
            "equipment_used": equipment or user_data.get('equipment'),
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== MOOD-BASED WORKOUT =====
@router.post("/mood-workout")
async def get_mood_based_workout(
    user_id: str,
    mood: Mood,
    user_data: dict = Depends(get_user_data)
):
    """
    Get workout adapted to current mood
    
    Params:
    - user_id: User ID
    - mood: Current mood (excellent, good, average, stressed)
    
    Returns: Mood-appropriate workout plan
    """
    try:
        user_data['mood'] = mood
        workout = await coach_ai.generate_mood_based_workout(user_data, mood)
        
        if "error" in workout:
            raise HTTPException(status_code=500, detail=workout["error"])
        
        return {
            "success": True,
            "user_id": user_id,
            "workout": workout["workout"],
            "mood": mood.value,
            "duration": user_data.get('daily_time'),
            "benefits": f"This {mood.value} mood workout will help you maintain consistency while respecting your energy levels",
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== MOTIVATION ENDPOINT =====
@router.get("/motivation")
async def get_motivation(
    user_id: str,
    streak: int = 0,
    progress: int = 0,
    user_data: dict = Depends(get_user_data)
):
    """
    Get personalized motivational message
    
    Params:
    - user_id: User ID
    - streak: Current workout streak (days)
    - progress: Progress towards goal (percentage)
    
    Returns: Motivational message
    """
    try:
        context = {
            "streak": streak,
            "progress": progress
        }
        
        message = await coach_ai.get_motivation(user_data, context)
        
        return {
            "success": True,
            "user_id": user_id,
            "message": message,
            "streak": streak,
            "progress": progress,
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== EXERCISE FORM ENDPOINT =====
@router.get("/exercise-form")
async def get_exercise_form(
    exercise: str,
    user_id: str = None
):
    """
    Get detailed form guide for an exercise
    
    Params:
    - exercise: Exercise name
    - user_id: Optional user ID for personalization
    
    Returns: Form guide with YouTube links and tips
    """
    try:
        form_guide = await coach_ai.provide_form_feedback(exercise)
        
        if "error" in form_guide:
            raise HTTPException(status_code=500, detail=form_guide["error"])
        
        return {
            "success": True,
            "exercise": exercise,
            "form_guide": form_guide["form_guide"],
            "youtube_search_terms": f"How to do {exercise} proper form",
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== MENSTRUAL RECOMMENDATIONS =====
@router.get("/menstrual-recommendations")
async def get_menstrual_recommendations(
    user_id: str,
    phase: str,  # 'menstruation', 'follicular', 'ovulation', 'luteal'
    mood: Mood,
    user_data: dict = Depends(get_user_data)
):
    """
    Get recommendations based on menstrual cycle phase
    
    Only available for female users
    
    Returns: Phase-specific recommendations for workout and nutrition
    """
    if user_data.get('gender') != 'Female':
        raise HTTPException(
            status_code=400,
            detail="This endpoint is for female users only"
        )
    
    try:
        recommendations = await coach_ai.get_menstrual_recommendations(phase, mood)
        
        if "error" in recommendations:
            raise HTTPException(status_code=500, detail=recommendations["error"])
        
        return {
            "success": True,
            "user_id": user_id,
            "phase": phase,
            "mood": mood.value,
            "recommendations": recommendations["recommendations"],
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== SYNC: Save Chat History =====
@router.post("/save-chat")
async def save_chat(user_id: str, message: str, response: str):
    """Save chat message to history (database would handle this)"""
    return {
        "success": True,
        "user_id": user_id,
        "saved_at": datetime.now(),
        "message_length": len(message),
        "response_length": len(response)
    }
