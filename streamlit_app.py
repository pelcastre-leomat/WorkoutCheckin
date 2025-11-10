import streamlit as st
from pages.settings import Settings

if "role" not in st.session_state:
    st.session_state.role = None
    st.session_state.settings_changed = False
    st.session_state.user_settings = None
    st.session_state.has_checked_in = False

ROLES = [None, "Requester"]

def login():
    st.header("Log in")
    role = st.selectbox("Choose your role", ROLES)

    if st.button("Log in"):
        st.session_state.role = role
        st.rerun()

def logout():
    st.session_state.role = None
    st.rerun()

role = st.session_state.role
settings_page = Settings()

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page(settings_page.show_settings, title="Settings", icon=":material/settings:")
check_in = st.Page(
    "request/check_in.py",
    title="Check in",
    icon=":material/check:",
    default=(role == "Requester"),
)
leaderboard = st.Page(
    "request/leaderboard.py", title="Leaderboard", icon=":material/crown:"
)

account_pages = [settings,logout_page]
request_pages = [check_in, leaderboard]

st.logo("images/logo.png", icon_image="images/dumbell.png",size="large")

page_dict = {}
if st.session_state.role in ["Requester"]:
    page_dict["Workouts"] = request_pages

if len(page_dict) > 0:
    pg = st.navigation(page_dict | {"Account": account_pages})
else:
    pg = st.navigation([st.Page(login)])

pg.run()