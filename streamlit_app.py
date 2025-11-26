import re
import sys
import streamlit as st
from pages.settings import Settings
from pages.settings import fetch_settings
from utils.db_connection import DB_Connection
from pages.troubleshoot import show_screen
from utils.db_enums import DB_Enums

NAMES = [name.lower() for name in st.secrets["exercise_users"].split(",")]

def login():
    st.header("Log in")
    with st.form("login_form"):
        regex = re.compile('[^a-zA-Z]')
        role = regex.sub('', st.text_input("Input your name:")).lower()
        submitted = st.form_submit_button("Log in")
        if submitted:
            if(role in NAMES):
                st.session_state.logged_name = role
                st.session_state.db_connection = DB_Connection()
                st.rerun()
            else:
                st.error("Login failed. Verify you are an allowed user.",icon="⛔")

def logout():
    st.session_state.logged_name = None
    st.rerun()

if "logged_name" not in st.session_state:
    #Simple login skip for testing
    st.session_state.auto_login_name = None
    st.session_state.auto_login = False
    st.session_state.offline = False
    if len(sys.argv)>1:
        #CLEAN THIS SHIT UP
        arg_name = sys.argv[1]
        if(arg_name != " "):
            st.session_state.auto_login_name = arg_name
            st.session_state.auto_login = True
        st.session_state.db_connection = DB_Connection()
        st.session_state.offline = True if sys.argv[2] == "True" else False

    st.session_state.logged_name = st.session_state.auto_login_name
    st.session_state.settings_changed = False
    st.session_state.user_settings = None
    st.session_state.has_checked_in = False
    st.session_state.is_init = False

if st.session_state.logged_name is not None:
    name = st.session_state.logged_name

    df = fetch_settings()
    user_exists = not df[df[DB_Enums.NAME.value] == name.title()].empty

    if "needs_onboarding" not in st.session_state:
        st.session_state.needs_onboarding = not user_exists

    # --- ONBOARDING ---
    if st.session_state.needs_onboarding:
        st.title(f"Welcome {name.title()}! 👋")
        st.subheader("Let's get you set up.")
        
        with st.form("onboarding"):
            goal = st.selectbox("What is your fitness goal?", 
                                ["Lose Weight", "Build Muscle", "Improve Health"])
            experience = st.selectbox("Training experience", 
                                      ["Beginner", "Intermediate", "Advanced"])
            submitted = st.form_submit_button("Complete Onboarding")

        if submitted:
            # Insert into database here
            data = {
                "userSettings":{
                        DB_Enums.NAME.value:name.title(),
                        DB_Enums.WORKOUT_GOAL.value:3,
                        DB_Enums.COST.value:50,
                        "settingsValidFromWeek": 47,
                    }
                }
            st.session_state.db_connection.send_data("userSettings","userSettings",data,True)
            fetch_settings.clear()
            df = fetch_settings()
            print(df)
            st.session_state.needs_onboarding = False
            st.success("You're all set! 🎉")
            st.rerun()

        st.stop()      # 👈 prevents rest of page from loading
    # --- END ONBOARDING ---



    # User exists → normal flow
    settings_page = Settings(name)
    logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
    troubleshoot = st.Page(show_screen, title="Troubleshooting", icon=":material/bug_report:")
    settings = st.Page(settings_page.show_settings, title="Settings", icon=":material/settings:")

    check_in = st.Page("sections/check_in.py", title="Check in", icon=":material/check:")
    leaderboard = st.Page("sections/leaderboard.py", title="Leaderboard", icon=":material/crown:")

    account_pages = [settings, troubleshoot, logout_page]
    request_pages = [check_in, leaderboard]

st.logo("images/logo.png", icon_image="images/dumbell.png",size="large")

page_dict = {}
if st.session_state.logged_name in NAMES or st.session_state.auto_login:
    page_dict["Workouts"] = request_pages

if len(page_dict) > 0:
    pg = st.navigation(page_dict | {"Account": account_pages})
else:
    pg = st.navigation([st.Page(login)])

pg.run()
