import pandas as pd
import json
from collections import Counter

def fetch_workouts():
    try:
        with open("data.json") as f:
        # with open("data2.json") as f:
            data = json.load(f)["workouts"]
            user_settings = parse_settings()
        return parse_workouts(data,user_settings)
    except Exception as e:
        return None

def parse_settings():
    try:
        with open("user_settings.json") as f:
            data = json.load(f)
        user_settings = {}
        for elem in data["user_settings"]:
            user_settings[elem["name"]] = {"workout_goal":elem["workout_goal"],"cost":elem["cost"]}
        return user_settings
    except Exception as e:
        return None

def parse_workouts(data,user_settings):
    counts = Counter(entry["name"] for entry in data)
    data = {"name": [], "workouts": [], "owed": []}
    for name, settings in user_settings.items():
        workout_count = counts.get(name, 0)
        data["name"].append(name)
        data["workouts"].append(workout_count)
        data["owed"].append(calc_owed(
            goal=settings["workout_goal"],
            workouts=workout_count,
            cost=settings["cost"]
        ))
    df = pd.DataFrame(data).sort_values(by="workouts",ascending=False,ignore_index=True)
    df.index = df.index+1
    return df

def calc_owed(goal, workouts, cost):
    owed = (goal - workouts) * cost
    return 0 if owed < 0 else owed
