"""
Authentication Router
"""

from fastapi import APIRouter, HTTPException
from models import UserRegister, UserResponse
from datetime import datetime
import json

router = APIRouter()

# Mock database
users_db = {}

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserRegister):
    """Register new user"""
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user_id = f"user_{len(users_db) + 1}"
    users_db[user.email] = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "gender": user.gender,
        "weight": user.weight,
        "height": user.height,
        "goal": user.goal.value,
        "budget": user.budget.value,
        "daily_time": user.daily_time,
        "profession": user.profession,
        "diet_preference": user.diet_preference.value,
        "disabilities": user.disabilities,
        "diseases": user.diseases,
        "created_at": datetime.now()
    }
    
    return users_db[user.email]

@router.post("/login")
async def login(email: str, password: str):
    """Login user"""
    if email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "success": True,
        "user_id": users_db[email]["id"],
        "token": f"token_{users_db[email]['id']}"
    }

@router.post("/logout")
async def logout(user_id: str):
    """Logout user"""
    return {"success": True, "message": "Logged out"}
