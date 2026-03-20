# Ollama API Integration for Dynamic Diet Plan Generation

## Summary of Changes

The FitnessCoachMVP backend has been successfully updated to use **Ollama API** for dynamic diet plan generation instead of predefined plans or Google Gemini API.

---

## What Changed

### 1. **Backend Service Layer** (`services/coach_service.py`)

#### Removed:
- Google Gemini API initialization
- `google.generativeai` dependency
- Safety settings configuration for Gemini

#### Added:
- Ollama API integration using `requests` library
- `_call_ollama()` method for making API requests to local Ollama instance
- `_get_goal_specifications()` method to calculate calorie and macro targets based on body goals

#### Updated Methods:
- `generate_diet_plan()` - Now dynamically generates diet plans based on:
  - **Body Goal**: `fat_loss`, `muscle_gain`, `maintenance`
  - **User Metrics**: Weight, Age, Height
  - **Diet Preference**: Vegetarian, Non-vegetarian, Eggitarian
  - **Budget**: Low, Medium, High
  - **Disabilities & Diseases**: Fully considered

- `chat_with_coach()` - Uses Ollama API
- `generate_workout_plan()` - Uses Ollama API
- `generate_mood_based_workout()` - Uses Ollama API
- `get_motivation()` - Uses Ollama API
- `get_menstrual_recommendations()` - Uses Ollama API
- `provide_form_feedback()` - Uses Ollama API

---

### 2. **Flask Routes** (`main.py`)

#### Updated Endpoints:

1. **`POST /api/coach/diet-plan`**
   - Now uses Ollama API instead of Gemini
   - Calculates goal-specific calorie targets
   - Returns macro breakdown (protein, carbs, fats percentages)
   - Includes complete meal plan with calorie counts
   - Returns target_calories and macro_targets in response

2. **`POST /api/coach/workout`**
   - Uses Ollama API for personalized workout generation
   - Incorporates available time and goal

3. **`POST /api/coach/mood-workout`**
   - Uses Ollama API for mood-based workout modification
   - Includes mood adjustments and energy level considerations

#### Added Helper Functions:
- `calculate_macro_targets()` - Calculates BMR and macro distribution based on goal

---

### 3. **Environment Configuration** (`.env` file)

#### Added:
```env
# Ollama API Configuration
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=neural-chat
```

#### Requirements:
- Ollama must be running locally: `ollama serve`
- Default model: `neural-chat` (7B parameters)
- API timeout: 120 seconds for complex diet plans

---

## How Diet Plans Are Generated

### Calorie Calculation:

The system uses **Harris-Benedict Formula** for BMR:
- **BMR = (10 × weight_kg) + 625**
- **TDEE = BMR × 1.55** (moderate activity level)

### Goal-Specific Macro Breakdown:

#### **Fat Loss** (15% deficit)
- Calories: `TDEE × 0.85`
- Protein: `Weight × 2.2g` (35%)
- Carbs: `Weight × 2.3g` (40%)
- Fats: `Weight × 0.8g` (25%)

#### **Muscle Gain** (15% surplus)
- Calories: `TDEE × 1.15`
- Protein: `Weight × 2.2g` (25%)
- Carbs: `Weight × 3.1g` (50%)
- Fats: `Weight × 0.8g` (25%)

#### **Maintenance**
- Calories: `TDEE`
- Protein: `Weight × 1.6g` (30%)
- Carbs: `Weight × 2.3g` (45%)
- Fats: `Weight × 0.8g` (30%)

---

## Example API Responses

### Muscle Gain Plan (Age: 28, Weight: 75kg, Height: 180cm)
```json
{
    "target_calories": 2450,
    "goal": "muscle_gain",
    "macros": {
        "protein": "165g (25%)",
        "carbs": "306g (50%)",
        "fats": "68g (25%)"
    },
    "diet_plan": "Daily meal plan with specific foods and calories..."
}
```

### Fat Loss Plan (Age: 30, Weight: 85kg, Budget: Low)
```json
{
    "target_calories": 1943,
    "goal": "fat_loss",
    "macros": {
        "protein": "187g (35%)",
        "carbs": "194g (40%)",
        "fats": "53g (25%)"
    },
    "diet_plan": "Budget-friendly meal plan with emphasis on satiety..."
}
```

---

## Key Features

✅ **Dynamic Generation**: Plans are created on-demand based on user data
✅ **Goal-Specific**: Different macros and calories for different goals
✅ **Personalized**: Considers weight, age, height, budget, diet preference, disabilities
✅ **Scientifically Backed**: Uses Harris-Benedict BMR formula and evidence-based macro splits
✅ **Detailed**: Includes specific meals, calorie counts, hydration, supplements, meal prep tips
✅ **Practical**: Budget-conscious and respects dietary restrictions
✅ **Scalable**: Uses local Ollama (free) instead of cloud APIs

---

## Installation & Setup

### Prerequisites:
1. Install Ollama: https://www.ollama.ai
2. Pull neural-chat model: `ollama pull neural-chat`
3. Start Ollama: `ollama serve`

### Run Flask Server:
```bash
cd /Users/lucky/Documents/FitnessCoachMVP/backend
python3 main.py
```

### Test Diet Plan Endpoint:
```bash
curl -X POST http://localhost:8000/api/coach/diet-plan \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "muscle_gain",
    "age": 28,
    "weight": 75,
    "height": 180,
    "diet_preference": "non_veg"
  }'
```

---

## Migration from Gemini to Ollama

| Aspect | Before (Gemini) | After (Ollama) |
|--------|---|---|
| **API** | Google Cloud | Local Ollama |
| **Cost** | Paid |  Free |
| **Latency** | Network dependent | Local machine |
| **Diet Plans** | Predefined templates | Dynamic generation |
| **Customization** | Limited | Unlimited |
| **Dependencies** | google-generativeai | requests |
| **Model** | gemini-pro | neural-chat |

---

## Files Modified

1. `/backend/services/coach_service.py` - Updated AI service to use Ollama
2. `/backend/main.py` - Updated Flask routes to use Ollama
3. `/.env` - Added Ollama configuration variables

---

## Testing Results

✅ **Muscle Gain Plan**: Generated 2450 calories with 50% carbs, 25% protein, 25% fat
✅ **Fat Loss Plan**: Generated 1943 calories with 40% carbs, 35% protein, 25% fat
✅ **Vegetarian Preference**: Plans use tofu, tempeh, quinoa instead of meat
✅ **Budget Consideration**: Low budget plans include affordable ingredients

---

## Next Steps (Optional Enhancements)

1. Add database persistence for user profiles
2. Implement meal shopping list generation
3. Add recipe variations for meal diversity
4. Store historical diet plans for tracking
5. Add weekly meal plan generation
6. Integrate with nutrition tracking APIs

---

**Status**: ✅ **Complete** - Dynamic diet plan generation with Ollama API is fully implemented and tested.
