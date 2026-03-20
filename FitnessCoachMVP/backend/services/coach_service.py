"""
AI Coach Service - The brains of the operation
Handles intelligent decision making with Ollama API
"""

import requests
import json
from typing import Optional, List, Dict
from datetime import datetime
from models import Mood, Goal, MenstrualPhase, DietPreference
import os

class FitnessCoachAI:
    """Main AI Coach using Ollama API"""
    
    def __init__(self):
        # Initialize Ollama API
        self.ollama_base_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        self.model_name = os.getenv("OLLAMA_MODEL", "neural-chat")
        self.timeout = 120  # 2 minutes timeout for Ollama responses
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API and return response text"""
        try:
            url = f"{self.ollama_base_url}/api/generate"
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
        except requests.exceptions.ConnectionError:
            raise Exception(f"Cannot connect to Ollama at {self.ollama_base_url}. Make sure Ollama is running with: ollama serve")
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
    def generate_system_prompt(self, user_data: Dict) -> str:
        """Generate system prompt with user context"""
        return f"""You are a highly personalized AI Fitness Coach. 
        
        USER PROFILE:
        - Name: {user_data.get('name')}
        - Age: {user_data.get('age')}
        - Goal: {user_data.get('goal')}
        - Fitness Level: {user_data.get('fitness_level', 'beginner')}
        - Available Time: {user_data.get('daily_time')} minutes/day
        - Budget: {user_data.get('budget')}
        - Diet: {user_data.get('diet_preference')}
        - Disabilities: {user_data.get('disabilities', 'None')}
        
        CURRENT STATE:
        - Mood: {user_data.get('mood', 'neutral')}
        - Energy: {user_data.get('energy', 5)}/10
        - Sleep: {user_data.get('sleep_hours', 7)} hours
        - Weight: {user_data.get('weight')} kg
        
        {self._get_menstrual_context(user_data)}
        
        INSTRUCTIONS:
        1. Be supportive, motivating, and personalized
        2. Always explain the 'why' behind recommendations
        3. Provide specific, actionable advice
        4. Consider all disabilities and health conditions
        5. Adapt intensity based on current mood and energy
        6. Include YouTube/Google video links for exercises
        7. Make workouts exciting and achievable
        8. Be concise but comprehensive
        """
    
    def _get_menstrual_context(self, user_data: Dict) -> str:
        """Generate menstrual cycle context for women"""
        if user_data.get('gender') != 'Female':
            return ""
        
        phase = user_data.get('menstrual_phase', 'unknown')
        return f"""
        MENSTRUAL CYCLE PHASE: {phase}
        - Adjust intensity based on energy levels during this phase
        - Menstruation: Light workouts, focus on recovery
        - Follicular: Ramp up intensity, good for heavy lifting
        - Ovulation: Peak performance, conditioned training
        - Luteal: Moderate intensity, focus on steady cardio
        - Adjust nutrition: Increase iron during menstruation
        """
    
    async def chat_with_coach(self, user_data: Dict, message: str) -> Dict:
        """Chat endpoint - respond to user questions"""
        try:
            prompt = f"""{self.generate_system_prompt(user_data)}
            
            USER MESSAGE: {message}
            
            Respond as a supportive fitness coach. Be specific and actionable."""
            
            response_text = self._call_ollama(prompt)
            
            return {
                "response": response_text,
                "type": "chat",
                "timestamp": datetime.now()
            }
        except Exception as e:
            return {
                "error": str(e),
                "response": f"I'm having trouble responding right now. Error: {str(e)}"
            }
    
    async def generate_diet_plan(self, user_data: Dict) -> Dict:
        """Generate personalized diet plan based on body goals using Ollama"""
        try:
            # Extract goal-specific parameters
            goal = user_data.get('goal', 'maintenance')
            weight = user_data.get('weight', 70)
            age = user_data.get('age', 30)
            height = user_data.get('height', 170)
            
            # Calculate calorie and macro targets based on goal
            goal_specs = self._get_goal_specifications(goal, weight, age)
            
            prompt = f"""{self.generate_system_prompt(user_data)}

BODY GOAL: {goal.upper().replace('_', ' ')}
Weight: {weight} kg
Age: {age} years
Height: {height} cm
Diet Preference: {user_data.get('diet_preference', 'balanced')}

TARGET MACROS FOR {goal.upper().replace('_', ' ')}:
- Daily Calories: {goal_specs['calories']}
- Protein: {goal_specs['protein']}g ({goal_specs['protein_percent']}%)
- Carbs: {goal_specs['carbs']}g ({goal_specs['carbs_percent']}%)
- Fats: {goal_specs['fats']}g ({goal_specs['fats_percent']}%)

CREATE A PERSONALIZED DAILY DIET PLAN with:
1. Daily calorie target: {goal_specs['calories']} calories (for {goal.replace('_', ' ')})
2. Macro breakdown: Protein {goal_specs['protein']}g, Carbs {goal_specs['carbs']}g, Fats {goal_specs['fats']}g
3. Specific meal suggestions:
   - Breakfast (with calories)
   - Mid-morning snack (with calories)
   - Lunch (with calories)
   - Pre-workout snack (with calories)
   - Dinner (with calories)
   - Post-workout meal (with calories)
4. Hydration recommendations (based on activity level)
5. Supplements recommendations (if needed for {goal.replace('_', ' ')})
6. Meal prep tips for {user_data.get('diet_preference', 'balanced')} diet
7. Important notes for achieving {goal.replace('_', ' ')} goal

Make sure to:
- Respect {user_data.get('diet_preference', 'balanced')} diet preference
- Keep meals within budget: {user_data.get('budget', 'medium')}
- Consider disabilities: {user_data.get('disabilities', 'none')}
- Focus on practical and affordable options

Format: Use clear sections with meal names, food items, and calorie counts."""

            response_text = self._call_ollama(prompt)
            
            return {
                "plan": response_text,
                "type": "diet_plan",
                "goal": goal,
                "target_calories": goal_specs['calories'],
                "timestamp": datetime.now(),
                "menstrual_phase": user_data.get('menstrual_phase'),
                "macro_targets": {
                    "protein": f"{goal_specs['protein']}g",
                    "carbs": f"{goal_specs['carbs']}g",
                    "fats": f"{goal_specs['fats']}g"
                }
            }
        except Exception as e:
            return {
                "error": str(e),
                "plan": f"Error generating diet plan: {str(e)}. Make sure Ollama is running."
            }
    
    def _get_goal_specifications(self, goal: str, weight: float, age: int) -> Dict:
        """Get calorie and macro targets based on goal"""
        # Base metabolic rate approximation (Harris-Benedict)
        if age < 18:
            bmr = (13.871 * weight) + 660
        else:
            bmr = (10 * weight) + 625  # Simplified, assuming average height/activity
        
        # Adjust for activity level (assuming moderate activity)
        tdee = bmr * 1.55
        
        if goal == "fat_loss":
            # 500 calorie deficit per day (0.5 kg per week)
            calories = int(tdee * 0.85)
            return {
                "calories": calories,
                "protein": int(weight * 2.2),  # Higher protein for satiety
                "carbs": int((calories * 0.40) / 4),  # 40% carbs
                "fats": int((calories * 0.25) / 9),  # 25% fats
                "protein_percent": 35,
                "carbs_percent": 40,
                "fats_percent": 25
            }
        elif goal == "muscle_gain":
            # 300-500 calorie surplus
            calories = int(tdee * 1.15)
            return {
                "calories": calories,
                "protein": int(weight * 2.2),  # 2.2g per kg body weight
                "carbs": int((calories * 0.50) / 4),  # 50% carbs
                "fats": int((calories * 0.25) / 9),  # 25% fats
                "protein_percent": 25,
                "carbs_percent": 50,
                "fats_percent": 25
            }
        else:  # maintenance
            calories = int(tdee)
            return {
                "calories": calories,
                "protein": int(weight * 1.6),  # Standard protein intake
                "carbs": int((calories * 0.45) / 4),  # 45% carbs
                "fats": int((calories * 0.30) / 9),  # 30% fats
                "protein_percent": 30,
                "carbs_percent": 45,
                "fats_percent": 25
            }
    
    async def generate_workout_plan(self, user_data: Dict) -> Dict:
        """Generate personalized workout plan"""
        try:
            equipment = user_data.get('equipment', ['no_equipment'])
            prompt = f"""{self.generate_system_prompt(user_data)}
            
            Available equipment: {', '.join(equipment)}
            Workout duration: {user_data.get('daily_time')} minutes
            
            CREATE A WORKOUT PLAN with:
            1. Warm-up (5 mins)
            2. Main exercises with:
               - Exercise name
               - Sets x Reps
               - Form tips
               - Common mistakes
               - Easier modification
               - Harder progression
            3. Cool-down and stretching (5 mins)
            4. Rest days recommendation
            
            Make it engaging, achievable, and specific."""
            
            response_text = self._call_ollama(prompt)
            
            return {
                "plan": response_text,
                "type": "workout_plan",
                "timestamp": datetime.now(),
                "mood_adapted": user_data.get('mood')
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def generate_mood_based_workout(self, user_data: Dict, mood: Mood) -> Dict:
        """Generate workout based on current mood"""
        try:
            mood_adjustments = {
                Mood.EXCELLENT: "High-intensity, challenging, strength-focused",
                Mood.GOOD: "Balanced workout with cardio and strength",
                Mood.AVERAGE: "Moderate intensity, consistent pace",
                Mood.STRESSED: "Low-intensity, calming, yoga/stretching focused"
            }
            
            prompt = f"""{self.generate_system_prompt(user_data)}
            
            CURRENT MOOD: {mood.value}
            Mood adjustment: {mood_adjustments[mood]}
            
            Create a {user_data.get('daily_time')}-minute workout that:
            1. Matches the mood adjustment above
            2. Includes specific exercises with reps
            3. Ends with mood-appropriate cool-down
            4. Is achievable in available time"""
            
            response_text = self._call_ollama(prompt)
            
            return {
                "workout": response_text,
                "mood": mood.value,
                "type": "mood_workout",
                "timestamp": datetime.now()
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def get_motivation(self, user_data: Dict, context: Dict = None) -> str:
        """Generate motivational message based on user progress"""
        try:
            streak = context.get('streak', 0) if context else 0
            progress = context.get('progress', 0) if context else 0
            
            prompt = f"""{self.generate_system_prompt(user_data)}
            
            USER'S STREAK: {streak} days
            PROGRESS: {progress}% towards goal
            
            Create a SHORT, PERSONALIZED motivational message (2-3 sentences) that:
            1. Acknowledges their progress
            2. Pushes them to keep going
            3. References their specific goal
            4. Is enthusiastic but realistic"""
            
            response_text = self._call_ollama(prompt)
            return response_text
        except Exception as e:
            return "Keep going! You're doing great! 💪"
    
    async def get_menstrual_recommendations(self, phase: MenstrualPhase, mood: Mood) -> Dict:
        """Get phase-specific recommendations"""
        try:
            prompt = f"""You are a fitness expert specializing in women's health.
            
            MENSTRUAL CYCLE PHASE: {phase.value}
            CURRENT MOOD: {mood.value}
            
            Provide recommendations for:
            1. Workout intensity (1-10 scale)
            2. Cardio vs Strength balance
            3. Key nutrients to focus on
            4. Recovery strategies
            5. General tips for this phase
            
            Be specific and science-backed."""
            
            response_text = self._call_ollama(prompt)
            
            return {
                "phase": phase.value,
                "recommendations": response_text,
                "timestamp": datetime.now()
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def provide_form_feedback(self, exercise: str) -> Dict:
        """Provide exercise form tips with video links"""
        try:
            prompt = f"""You are a certified fitness trainer specializing in proper exercise form.
            
            EXERCISE: {exercise}
            
            Provide:
            1. Proper form instructions (step-by-step)
            2. Common mistakes to avoid
            3. Safety tips
            4. Muscle groups worked
            5. YouTube search terms to find proper form videos
            
            Be detailed and clear."""
            
            response_text = self._call_ollama(prompt)
            
            return {
                "exercise": exercise,
                "form_guide": response_text,
                "timestamp": datetime.now()
            }
        except Exception as e:
            return {"error": str(e)}


# Initialize coach instance
coach_ai = FitnessCoachAI()
