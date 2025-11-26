from datetime import datetime
import pandas as pd
import streamlit as st
from utils.db_enums import DB_Enums

def current_week_key():
    today = datetime.today()
    year, week_num, _ = today.isocalendar()
    return f"{year}-W{week_num}"

def populate_leaderboard():
    offline = st.session_state.offline
    this_week = datetime.today().isocalendar().week
    try:
        workout_data = fetch_workouts(offline=offline,options=f"[{DB_Enums.WEEK}]={this_week}")
        user_settings = parse_settings(offline=offline,week_str=current_week_key())
        return parse_workouts(workout_data,user_settings)
    except Exception as e:
        print(e)
        return None

def fetch_workouts(offline=False,options=None):
    full_week_workouts_df = st.session_state.db_connection.fetch_data_table(
        table_id=DB_Enums.WORKOUTS_DB,
        offline=offline,
        filter_options=options
    )
    #SAVE FWW_DF into state?
    counted_workouts_df = pd.DataFrame(full_week_workouts_df[DB_Enums.NAME].value_counts()).reset_index()
    counted_workouts_df.columns = [DB_Enums.NAME,DB_Enums.PERFORMED_WORKOUTS]
    return counted_workouts_df

#Change to save week this setting applies?
@st.cache_data(persist="disk")
def parse_settings(week_str:str,offline=False):
    print("Fetching settings table, not from cache")
    data = st.session_state.db_connection.fetch_data_table(
        table_id=DB_Enums.USER_SETTINGS_DB,
        offline=offline
    )
    return data

def parse_workouts(data,user_settings):
    df = data.merge(user_settings,on=DB_Enums.NAME,how="outer").fillna(0)
    gap = (df[DB_Enums.WORKOUT_GOAL] - df[DB_Enums.PERFORMED_WORKOUTS]).clip(lower=0)
    df.insert(1,"eligible",df[DB_Enums.WORKOUT_GOAL] <= df[DB_Enums.PERFORMED_WORKOUTS])
    df.insert(len(df.columns)-1,DB_Enums.OWES, gap * df[DB_Enums.COST])
    column_names = ["Name","Completed challenge","Workouts Performed","Workout Goal","Missed Workout Cost","Owes","Applied Settings Week"]
    df = df.sort_values(by=["eligible",DB_Enums.PERFORMED_WORKOUTS],ascending=False,ignore_index=True)
    df.index = df.index+1
    df.columns = column_names
    return df
