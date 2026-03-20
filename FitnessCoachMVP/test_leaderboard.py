#!/usr/bin/env python3
"""
Test script for the dynamic leaderboard endpoint
Run this after the Flask backend is running
"""

import os
import sys
import json
import time
import requests
from datetime import datetime, timedelta

# Add backend path for imports
backend_path = '/Users/lucky/Documents/FitnessCoachMVP/backend'
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

API_BASE = 'http://localhost:8000'

def test_leaderboard():
    """Test the leaderboard endpoint"""
    print("=" * 60)
    print("TESTING LEADERBOARD ENDPOINT")
    print("=" * 60)
    
    # First add some test data
    print("\n1. Adding test users...")
    test_users = [
        {
            "name": "Alice (Fat Loss)",
            "email": f"alice{int(time.time())}@test.com",
            "age": 28,
            "gender": "Female",
            "profession": "Engineer",
            "weight": 80,
            "target_weight": 75,
            "height": 165,
            "goal": "fat_loss",
            "diet_preference": "balanced",
            "budget": "moderate",
            "daily_time": 60
        },
        {
            "name": "Bob (Muscle Gain)",
            "email": f"bob{int(time.time())}@test.com",
            "age": 25,
            "gender": "Male",
            "profession": "Student",
            "weight": 75,
            "target_weight": 85,
            "height": 180,
            "goal": "muscle_gain",
            "diet_preference": "high_protein",
            "budget": "limited",
            "daily_time": 45
        },
        {
            "name": "Charlie (General)",
            "email": f"charlie{int(time.time())}@test.com",
            "age": 35,
            "gender": "Male",
            "profession": "Manager",
            "weight": 78,
            "target_weight": 76,
            "height": 175,
            "goal": "general",
            "diet_preference": "balanced",
            "budget": "high",
            "daily_time": 30
        }
    ]
    
    user_ids = []
    for user in test_users:
        try:
            response = requests.post(f'{API_BASE}/api/auth/signup', json=user)
            if response.status_code == 200:
                data = response.json()
                user_id = data.get('id')  # Changed from 'user_id' to 'id'
                user_ids.append(user_id)
                print(f"   ✓ Created {user['name']} (ID: {user_id})")
            else:
                print(f"   ✗ Failed to create {user['name']}: {response.text}")
        except Exception as e:
            print(f"   ✗ Error creating {user['name']}: {e}")
    
    if len(user_ids) == 0:
        print("   No users created, cannot test leaderboard")
        return
    
    # Add weight logs for each user
    print("\n2. Adding weight logs...")
    weight_logs = [
        # Alice: Losing weight (fat_loss goal)
        {"user_id": user_ids[0], "weights": [80, 79.5, 79, 78.5, 78]},
        # Bob: Gaining weight (muscle_gain goal)
        {"user_id": user_ids[1], "weights": [75, 76, 76.5, 77, 77.5]},
        # Charlie: Minor change (general goal)
        {"user_id": user_ids[2], "weights": [78, 77.9, 77.8]},
    ]
    
    for log_data in weight_logs:
        user_id = log_data['user_id']
        for i, weight in enumerate(log_data['weights']):
            try:
                response = requests.post(
                    f'{API_BASE}/api/progress/log-weight',
                    json={"user_id": user_id, "weight": weight}
                )
                if response.status_code == 200:
                    user_name = test_users[[u['email'] for u in test_users].index(
                        [u for u in test_users if 'alice' in u['email'].lower()][0]['email'] if 'alice' in u['email'].lower() else ''
                    )]['name'] if user_id == user_ids[0] else (
                        test_users[1]['name'] if user_id == user_ids[1] else test_users[2]['name']
                    )
                    print(f"   ✓ Logged {weight}kg for user {user_id}")
                else:
                    print(f"   ✗ Failed: {response.text}")
            except Exception as e:
                print(f"   ✗ Error: {e}")
            time.sleep(0.1)  # Small delay between logs
    
    # Test the leaderboard endpoint
    print("\n3. Testing GET /api/leaderboard...")
    try:
        response = requests.get(f'{API_BASE}/api/leaderboard')
        if response.status_code == 200:
            data = response.json()
            print("   ✓ Leaderboard endpoint working!")
            print(f"\n   Response structure:")
            print(f"   - Goals found: {data.get('goals', [])}")
            print(f"   - Timestamp: {data.get('timestamp', 'N/A')}")
            
            # Display results by goal
            leaderboard = data.get('leaderboard', {})
            for goal, rankings in leaderboard.items():
                print(f"\n   📊 {goal.upper()} LEADERBOARD:")
                if rankings:
                    for user in rankings[:3]:  # Show top 3
                        print(f"      #{user['rank']} {user['name']}")
                        print(f"         Score: {user['score']} | Streak: {user['streak']} days")
                        print(f"         Progress: {user['weight_progress']}kg | Current: {user['current_weight']}kg")
                else:
                    print(f"      (No users with {goal} goal)")
        else:
            print(f"   ✗ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ✗ Connection error: {e}")
        print(f"   ✗ Make sure Flask server is running on port 8000")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    test_leaderboard()
