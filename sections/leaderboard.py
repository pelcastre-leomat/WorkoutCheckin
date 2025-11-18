import streamlit as st
import time
from datetime import datetime
from utils.fetch_workouts import populate_leaderboard

# Cached data fetch
@st.cache_data(persist="disk")
def fetch_leaderboard():
    print("RUNNING")  # Will only appear when cache is refreshed
    time.sleep(1)  # Simulate slow fetch
    df = populate_leaderboard()
    # df = None
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return df, last_updated

# Button handler: clears cache to trigger a fresh fetch next time
def force_update():
    fetch_leaderboard.clear()
    st.session_state["force_refresh"] = True  # Used to immediately trigger new cache fill

st.title("Leaderboard")

# Retrieve data (recomputed if cache cleared)
df, last_updated = fetch_leaderboard()

if(df is None):
    fetch_leaderboard.clear()
    st.error("Couldn't fetch leaderboard, try again later",icon="🔥")

st.write(f"**Last updated:** {last_updated}")
st.dataframe(df)

# Force update button
st.write(":red[Please only update once a day]")
if st.button("Force Update", on_click=force_update,type="primary"):
    st.rerun()