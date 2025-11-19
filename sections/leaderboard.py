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
def force_update():
    fetch_leaderboard.clear()
    st.session_state["force_refresh"] = True

st.title(f"Week {datetime.today().isocalendar().week}'s Stats and Info")
st.info("Facing issues with the table? Try purging it from your system (This will also force update the table).",icon="🐛")
st.button("Purge and Update Info",on_click=force_update)

df, last_updated = fetch_leaderboard()

if(df is None):
    fetch_leaderboard.clear()
    st.error("Couldn't fetch leaderboard, try again later",icon="🔥")

st.markdown(f":green[**Last updated:** {last_updated}]")
st.write(":red[Please only update or purge once a day]")
st.info("Depending on your device size, you might need to scroll to see more stats!",icon="ℹ️")
st.dataframe(df)

# Force update button
if st.button("Update Info", on_click=force_update,type="primary"):
    st.rerun()
