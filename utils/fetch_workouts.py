from datetime import datetime
import pandas as pd
import json
from collections import Counter
import streamlit as st



def populate_leaderboard():
    offline = st.session_state.offline
    this_week = datetime.today().isocalendar().week
    try:
        workout_data = fetch_workouts(offline,options=f"[week]={this_week}")
        user_settings = parse_settings(offline)
        return parse_workouts(workout_data,user_settings)
    except Exception as e:
        print(e)
        return None

def fetch_workouts(offline=False,options=None):
    return st.session_state.db_connection.fetch_data_table(
        table_id="workouts",
        offline=offline
    )

def parse_settings(offline=False):
    data = st.session_state.db_connection.fetch_data_table(
        table_id="user_settings",
        offline=offline
    )
    user_settings = {}
    for elem in data:
        user_settings[elem["name"]] = {"workout_goal":elem["workout_goal"],"cost":elem["cost"]}
    return user_settings

def parse_workouts(data,user_settings):
    counts = Counter(entry["name"] for entry in data)
    data = {"name": [], "workouts_goal":[],"performed_workouts": [],"is_eligible":[], "owes": []}
    for name, settings in user_settings.items():
        workout_count = counts.get(name, 0)
        data["name"].append(name)
        data["workouts_goal"].append(settings["workout_goal"])
        data["performed_workouts"].append(workout_count)
        data["is_eligible"].append(workout_count >= settings["workout_goal"])
        data["owes"].append(calc_owed(
            goal=settings["workout_goal"],
            workouts=workout_count,
            cost=settings["cost"]
        ))
    column_names = ["Name","Workout goal","Workouts Performed","Completed challenge","Owes"]
    df = pd.DataFrame(data).sort_values(by="is_eligible",ascending=False,ignore_index=True)
    df.index = df.index+1
    df.columns = column_names
    print(df)
    return df

def calc_owed(goal, workouts, cost):
    owed = (goal - workouts) * cost
    return 0 if owed < 0 else owed
