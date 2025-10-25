import streamlit as st
from save_to_file import save_to_file

def checkin_user(user,date):

    if(user != "" and user.isalpha()):
        user = user.title()
        if(user in st.secrets["exercise_users"].split(",")):
            st.session_state.title = f"Thank you for checking-in, {user}!"
            st.session_state.disabled = True
            save_to_file(user,date)
    else:
        st.session_state.title = "Please input a valid name."

if 'title' not in st.session_state:
    st.session_state.title = "Weekly Workout Check-In"
    st.session_state.disabled = False

st.title(st.session_state.title)
if(not st.session_state.disabled):
    date = st.date_input("Date to check-in:", "today",format="DD/MM/YYYY",disabled=st.session_state.disabled)
    user = st.text_input("Who do you want to check-in?",disabled=st.session_state.disabled)
    checkin_btn = st.button('Check-in', on_click=checkin_user,
        args=(user,date),disabled=st.session_state.disabled)
