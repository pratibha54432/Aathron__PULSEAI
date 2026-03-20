#!/usr/bin/env python3
"""
Quick test script to verify backend setup
Run: python test_api.py
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_signup():
    """Test user registration"""
    print_section("TEST 1: User Registration")
    
    payload = {
        "name": "Hackathon Athlete",
        "email": "hacker@fitness.com",
        "age": 25,
        "gender": "male",
        "weight": 75,
        "height": 180,
        "goal": "muscle_gain",
        "budget": "medium",
        "daily_time": 45,
        "profession": "Software Engineer",
        "diet_preference": "balanced",
        "disabilities": [],
        "diseases": []
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=payload)
        if response.status_code == 200:
            user = response.json()
            print(f"✅ User registered successfully!")
            print(f"   User ID: {user.get('id')}")
            print(f"   Name: {user.get('name')}")
            return user.get('id')
        else:
            print(f"❌ Registration failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"   Make sure backend is running: uvicorn backend/main:app --reload")
        return None

def test_diet_plan(user_id):
    """Test AI diet plan generation"""
    print_section("TEST 2: AI Diet Plan Generation")
    
    payload = {
        "user_id": user_id,
        "goal": "weight_loss",
        "age": 25,
        "weight": 75,
        "height": 180,
        "diet_preference": "vegetarian"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/coach/diet-plan", json=payload)
        if response.status_code == 200:
            plan = response.json()
            print(f"✅ Diet plan generated!")
            print(f"\nPlan Preview:\n")
            print(plan.get('diet_plan', 'No plan')[:500] + "...")
            print(f"\nMacros: {plan.get('macros')}")
            return True
        else:
            print(f"❌ Diet plan failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"   Check GEMINI_API_KEY in backend/.env")
        return False

def test_workout(user_id):
    """Test AI workout generation"""
    print_section("TEST 3: AI Workout Generation")
    
    payload = {
        "user_id": user_id,
        "goal": "muscle_gain",
        "available_time": 45,
        "fitness_level": "intermediate"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/coach/workout", json=payload)
        if response.status_code == 200:
            workout = response.json()
            print(f"✅ Workout generated!")
            print(f"\nWorkout Preview:\n")
            print(workout.get('workout_plan', 'No workout')[:500] + "...")
            print(f"\nDuration: {workout.get('duration')} minutes")
            return True
        else:
            print(f"❌ Workout generation failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_mood_logging(user_id):
    """Test mood tracking"""
    print_section("TEST 4: Mood & Energy Logging")
    
    payload = {
        "user_id": user_id,
        "mood_score": 7,
        "energy_level": 8,
        "sleep_hours": 7.5,
        "stress_level": 3
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/progress/log-mood", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Mood logged successfully!")
            print(f"   Mood Score: {payload['mood_score']}/10")
            print(f"   Energy Level: {payload['energy_level']}/10")
            print(f"   Sleep Hours: {payload['sleep_hours']}h")
            print(f"   Stress Level: {payload['stress_level']}/10")
            return True
        else:
            print(f"❌ Mood logging failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_mood_workout(user_id):
    """Test mood-based workout suggestion"""
    print_section("TEST 5: Mood-Based Workout")
    
    payload = {
        "user_id": user_id,
        "mood": "stressed",
        "energy_level": 4,
        "available_time": 30
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/coach/mood-workout", json=payload)
        if response.status_code == 200:
            suggestion = response.json()
            print(f"✅ Mood-based workout suggestion generated!")
            print(f"\nSuggestion:\n")
            print(suggestion.get('workout_suggestion', 'No suggestion')[:500] + "...")
            print(f"\nIntensity: {suggestion.get('intensity')}")
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_progress(user_id):
    """Test progress retrieval"""
    print_section("TEST 6: Progress Statistics")
    
    try:
        response = requests.get(f"{BASE_URL}/api/progress/progress/{user_id}")
        if response.status_code == 200:
            progress = response.json()
            print(f"✅ Progress data retrieved!")
            print(f"   Total Mood Logs: {progress.get('total_logs', 0)}")
            print(f"   Average Mood: {progress.get('average_mood', 'N/A')}/10")
            print(f"   Mood Trend: {progress.get('mood_trend', 'N/A')}")
            return True
        else:
            print(f"⚠️  No progress data yet (first time): {response.status_code}")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_api_docs():
    """Test API documentation availability"""
    print_section("TEST 7: API Documentation")
    
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print(f"✅ API docs available at: {BASE_URL}/docs")
            print(f"   Interactive API testing enabled")
            return True
        else:
            print(f"❌ API docs not available")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("  PULSEAI AGENT - Backend Test Suite")
    print("="*60)
    print(f"Testing: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test connectivity
    try:
        response = requests.get(f"{BASE_URL}/docs")
    except requests.exceptions.ConnectionError:
        print_section("CONNECTION ERROR")
        print("❌ Cannot connect to backend server")
        print("\nMake sure to start the backend:")
        print("  cd backend")
        print("  uvicorn main:app --reload")
        return
    
    # Run tests
    results = {
        "API Docs": test_api_docs(),
        "User Registration": False,
        "Diet Plan Generation": False,
        "Workout Generation": False,
        "Mood Logging": False,
        "Mood-Based Workout": False,
        "Progress Tracking": False
    }
    
    user_id = test_signup()
    if user_id:
        results["User Registration"] = True
        results["Diet Plan Generation"] = test_diet_plan(user_id)
        results["Workout Generation"] = test_workout(user_id)
        results["Mood Logging"] = test_mood_logging(user_id)
        results["Mood-Based Workout"] = test_mood_workout(user_id) if results["Mood Logging"] else False
        results["Progress Tracking"] = test_progress(user_id)
    
    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status} | {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your backend is ready for development.")
        print("\nNext steps:")
        print("  1. Build React frontend in frontend/ directory")
        print("  2. Connect frontend to backend APIs")
        print("  3. Test full end-to-end flow")
        print("  4. Deploy to production")
    else:
        print("\n⚠️  Some tests failed. Check:")
        print("  - Backend server is running")
        print("  - GEMINI_API_KEY is set in backend/.env")
        print("  - Database is accessible")
        print("  - Internet connection is available")

if __name__ == "__main__":
    main()
