
import json
import os

DATA_FILE = "user_data.json"

# Load user data
def load_user_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save user data
def save_user_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Add or update a user
def update_user(user_id, updates):
    data = load_user_data()
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {
            "coins": [],
            "strategies": [],
            "capital": 0.0,
            "experience": "beginner",
            "xp": 0,
            "loyalty_tier": "none"
        }
    data[user_id].update(updates)
    save_user_data(data)

# Get user data
def get_user(user_id):
    data = load_user_data()
    return data.get(str(user_id), None)

# Update coins
def set_user_coins(user_id, coins):
    update_user(user_id, {"coins": coins})

# Update strategies
def set_user_strategies(user_id, strategies):
    update_user(user_id, {"strategies": strategies})

# Update capital
def set_user_capital(user_id, capital):
    update_user(user_id, {"capital": capital})

# Update experience level
def set_user_experience(user_id, level):
    update_user(user_id, {"experience": level})

# Update XP and loyalty
def add_xp(user_id, xp_gain):
    user = get_user(user_id)
    if not user:
        return
    user["xp"] += xp_gain
    # Update loyalty tier
    if user["xp"] >= 500:
        user["loyalty_tier"] = "elite"
    elif user["xp"] >= 250:
        user["loyalty_tier"] = "gold"
    elif user["xp"] >= 100:
        user["loyalty_tier"] = "silver"
    else:
        user["loyalty_tier"] = "none"
    update_user(user_id, user)
