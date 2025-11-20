import time
import streamlit as st
from datetime import datetime
from utils.fetch_workouts import populate_leaderboard

# Cached data fetch
@st.cache_data(persist="disk")
def fetch_leaderboard():
    print("Updating Table")
    df = populate_leaderboard()
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return df, last_updated

# Button handler: clears cache to trigger a fresh fetch next time
def force_update(df):
    msg = st.info("Fetching new stats and info",icon="⚙️")
    time.sleep(2)
    fetch_leaderboard.clear()
    st.session_state["force_refresh"] = True
    if(df is not None):
        msg.success("Successfully updated stats and info",icon="👍")
    else:
        msg.error("Couldn't fetch stats and info, try again later",icon="🔥")
st.title(f"Week {datetime.today().isocalendar().week}'s Stats and Info")
df, last_updated = fetch_leaderboard()

if(df is None):
    fetch_leaderboard.clear()

st.markdown(f"**Last updated:** {last_updated}")
st.info("Depending on your device size, you might need to scroll to see more stats!",icon="ℹ️")
st.dataframe(df)
st.write(":red[Please only update once a day]")
st.button("Update Info",on_click=force_update,kwargs={"df":df},type="primary")
