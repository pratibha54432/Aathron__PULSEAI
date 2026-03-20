# Dynamic Leaderboard Implementation

## Overview
Implemented a dynamic leaderboard endpoint that ranks users by their fitness goals, weight progress, and streak consistency.

## Backend Changes (/backend/main.py)

### New Endpoint: `GET /api/leaderboard`

**Location:** Lines 527-650 in main.py

**Functionality:**
- Fetches all users from the database
- Calculates weight progress, streaks, and scores for each user
- Organizes leaderboard by fitness goal type (fat_loss, muscle_gain, general)
- Returns ranked lists for each goal category

**Scoring Algorithm:**
- **Fat Loss Goal:** `score = (weight_lost * 100) + (streak_days * 10)`
    - Rewards users for losing weight
    - Bonus points for maintaining consistent logging streaks
  
- **Muscle Gain Goal:** `score = (weight_gained * 100) + (streak_days * 10)`
    - Rewards users for gaining weight (muscle)
    - Bonus points for consistency
  
- **General Fitness Goal:** `score = (weight_change * 50) + (streak_days * 10)`
    - Balanced approach for any weight change
    - Emphasizes consistency with streak tracking

**Streak Calculation:**
```python
- Parses weight log timestamps
- Counts consecutive days backwards from today
- Stops counting at first day with no log
- Example: 5-day streak means 5 consecutive days with weight logged
```

**Data Returned:**
```json
{
  "leaderboard": {
    "fat_loss": [...],
    "muscle_gain": [...],
    "general": [...]
  },
  "goals": ["fat_loss", "muscle_gain", "general"],
  "timestamp": "2024-X-XXTXX:XX:XX"
}
```

**Each User Entry Contains:**
- `rank` - Position in goal-specific leaderboard
- `user_id` - Unique user identifier
- `name` - User's display name
- `score` - Calculated fitness score
- `streak` - Current consecutive days of logging
- `weight_progress` - Total weight change
- `weight_change` - Net weight change
- `current_weight` - Latest logged weight
- `target_weight` - User's fitness goal weight
- `num_logs` - Total number of weight entries

## Frontend Changes (/frontend/index.html)

### Updated Function: `showLeaderboard()`

**Location:** Lines 1309-1365 in index.html

**Changes:**
1. Replaced hardcoded mock data with API call
2. Fetches leaderboard from `http://localhost:8000/api/leaderboard`
3. Filters leaderboard by current user's goal
4. Displays top 10 users for user's goal category
5. Highlights current user with blue styling

**Display Features:**
- **Medal System:**
  - 🥇 Rank 1 (Gold)
  - 🥈 Rank 2 (Silver)
  - 🥉 Rank 3 (Bronze)
  - ⭐ Ranks 4-10 (Star)

- **User Information:**
  - Rank position
  - User name (marked as "You" for current user)
  - Score (weighted calculation)
  - Streak (consecutive days)
  - Weight progress toward target

- **Styling:**
  - Current user highlighted with light blue background
  - Goal category displayed at top of leaderboard
  - Error handling with user-friendly messages

## API Response Example (Empty Database)

```json
{
  "leaderboard": {},
  "goals": [],
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

## API Response Example (With Data)

```json
{
  "leaderboard": {
    "fat_loss": [
      {
        "rank": 1,
        "user_id": "user_1",
        "name": "Alice",
        "score": 1050.0,
        "streak": 5,
        "weight_progress": 5.0,
        "weight_change": -5.0,
        "current_weight": 75.0,
        "target_weight": 70.0,
        "num_logs": 5
      },
      {
        "rank": 2,
        "user_id": "user_2",
        "name": "Bob",
        "score": 150.0,
        "streak": 3,
        "weight_progress": 1.5,
        "weight_change": -1.5,
        "current_weight": 78.5,
        "target_weight": 75.0,
        "num_logs": 3
      }
    ],
    "muscle_gain": [
      {
        "rank": 1,
        "user_id": "user_3",
        "name": "Charlie",
        "score": 480.0,
        "streak": 8,
        "weight_progress": 4.8,
        "weight_change": 4.8,
        "current_weight": 84.8,
        "target_weight": 90.0,
        "num_logs": 8
      }
    ]
  },
  "goals": ["fat_loss", "muscle_gain"],
  "timestamp": "2024-01-15T10:35:20.456789"
}
```

## Testing the Leaderboard

### 1. Start the backend:
```bash
cd /Users/lucky/Documents/FitnessCoachMVP/backend
python3 main.py
```

### 2. Test with curl:
```bash
curl http://localhost:8000/api/leaderboard | python3 -m json.tool
```

### 3. In browser:
- Open the fitness coach app
- Click on leaderboard icon/button
- Will automatically fetch and display rankings for your goal

## Key Features

✓ Goal-specific leaderboards (separate rankings per fitness goal)
✓ Dynamic scoring based on weight progress and consistency
✓ Streak calculation from timestamped weight logs
✓ Real-time ranking updates based on logged data
✓ Current user highlighting for easy self-reference
✓ Graceful error handling with user-friendly messages
✓ Top 10 display per goal category

## Error Handling

If leaderboard fails to load:
- Backend returns empty leaderboard for no data
- Frontend displays "No leaderboard data available for your goal yet"
- Connection errors show "Failed to load leaderboard. Please try again."

## Future Enhancements

- Multi-goal leaderboards (show all goals available)
- Time-period filtering (weekly, monthly, all-time)
- Goal completion percentage tracking
- Achievements and badges system
- Social sharing of leaderboard rankings
- Personalized comparison with friends
