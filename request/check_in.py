import time
import streamlit as st

def check_in(date):
    msg = st.info("Checking you in...",icon="🏋️")
    time.sleep(1)
    #ADD SOME ERROR HANDLING
    print(date)
    msg.success("Awesome you've checked in!",icon="🎉")
    st.balloons()

st.title("Check in")
date = st.date_input(label="When did you workout?")
st.button(label="Check in",on_click=check_in,kwargs={"date":date},disabled=st.session_state.has_checked_in,type="primary")