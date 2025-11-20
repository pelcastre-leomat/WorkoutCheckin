import time
import streamlit as st
from utils.db_enums import DB_Enums
from datetime import datetime,timedelta

def check_in(date:datetime):
    offline = st.session_state.offline
    checkin_week = date.isocalendar().week
    if(checkin_week == datetime.today().isocalendar().week):
        msg = st.info("Checking you in...",icon="🏋️")
        time.sleep(1)
        workout_name = DB_Enums.WORKOUTS_DB[:-1] if DB_Enums.WORKOUTS_DB[-1] == "s" else DB_Enums.WORKOUTS_DB
        data = {
            workout_name: {
                DB_Enums.NAME.value:st.session_state.logged_name.title(),
                DB_Enums.DAY.value:datetime.strftime(date,"%d/%m/%Y"),
                DB_Enums.WEEK.value:checkin_week
            }
        }

        if(st.session_state.offline):
            data[workout_name].update({"id":99})
        try:
            full_week_workouts_df = st.session_state.db_connection.send_data(
                table_id=DB_Enums.WORKOUTS_DB,
                sheet_name=workout_name,
                data = data,
                offline=offline
            )
        except Exception as e:
            #Log sent to email?
            print(e)
            print("Could not check in user")
            msg.error("Could not check you in. Try again later.",icon="😭")
            return
        msg.success("Awesome you've checked in!",icon="🎉")
        st.balloons()
        print("Successfully checked in")
    else:
        st.error("Tying to cheat? You can only check in for the current week.",icon="🫵")

st.title(f"Let's check in, {st.session_state.logged_name.title()}!")
# Get today's date (as a date object)
today = datetime.today().date()

# Calculate Monday (start of current week)
monday = today - timedelta(days=today.weekday())

# Date input restricted to current week
date = st.date_input(
    label="When did you workout?",
    min_value=monday,
    max_value=today,
    value=today,  # must be within the range
    format="DD/MM/YYYY"
)
st.button(label="Check in",on_click=check_in,kwargs={"date":date},disabled=st.session_state.has_checked_in,type="primary")