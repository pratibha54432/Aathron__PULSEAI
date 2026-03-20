"""
Database Models for Fitness Coach - Pydantic v1 Compatible
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ===== ENUMS =====
class Goal(str, Enum):
    FAT_LOSS = "fat_loss"
    MUSCLE_GAIN = "muscle_gain"  
    MAINTENANCE = "maintenance"

class Mood(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    STRESSED = "stressed"

class Budget(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class DietPreference(str, Enum):
    VEGETARIAN = "veg"
    NON_VEGETARIAN = "non_veg"
    EGGITARIAN = "eggetarian"

# ===== USER MODELS =====
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    age: int
    gender: str
    weight: float
    height: float
    goal: Goal
    budget: Budget
    daily_time: int
    profession: str
    diet_preference: DietPreference
    disabilities: Optional[List[str]] = []
    diseases: Optional[List[str]] = []

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    age: int
    weight: float
    height: float
    goal: Goal

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    user_id: str
    message: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.now)

class MoodData(BaseModel):
    user_id: str
    mood_score: int = Field(..., ge=1, le=10)
    energy_level: int = Field(..., ge=1, le=10)
    sleep_hours: float
    stress_level: int = Field(..., ge=1, le=10)

class DietPlanRequest(BaseModel):
    user_id: str
    goal: Goal
    age: int
    weight: float
    height: float
    diet_preference: DietPreference

class WorkoutRequest(BaseModel):
    user_id: str
    goal: Goal
    available_time: int
    fitness_level: str = "intermediate"

class MoodWorkoutRequest(BaseModel):
    user_id: str
    mood: str
    energy_level: int = Field(..., ge=1, le=10)
    available_time: int = 30

class ProgressResponse(BaseModel):
    user_id: str
    total_logs: int
    average_mood: float
    average_energy: float
    average_sleep: float
    mood_trend: str
    recent_data: List[dict] = []

class StreakResponse(BaseModel):
    user_id: str
    current_streak: int
    total_workouts: int
