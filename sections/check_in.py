import time
import streamlit as st
from utils.db_enums import DB_Enumbs

def check_in(date):
    msg = st.info("Checking you in...",icon="🏋️")
    time.sleep(1)
    workout_name = DB_Enumbs.WORKOUTS_DB[:-1] if DB_Enumbs.WORKOUTS_DB[-1] == "s" else DB_Enumbs.WORKOUTS_DB
    print(workout_name)
    data = {
        workout_name:[
            {
                
            }
        ]
    }
    full_week_workouts_df = st.session_state.db_connection.send_data(
        table_id=DB_Enumbs.WORKOUTS_DB,
        data = data,
        offline=True
    )
    #ADD SOME ERROR HANDLING
    print(date)
    msg.success("Awesome you've checked in!",icon="🎉")
    st.balloons()

st.title(f"Let's check in, {st.session_state.auto_login_name.title()}!")
date = st.date_input(label="When did you workout?")
st.button(label="Check in",on_click=check_in,kwargs={"date":date},disabled=st.session_state.has_checked_in,type="primary")