import streamlit as st
from pages.settings import fetch_settings
from streamlit_extras.let_it_rain import rain

def show_screen():
    st.title("Troubleshooting")
    st.write(":red[AS WITH ANY BUTTON THAT FETCHES INFO, PLEASE ONLY USE THIS BUTTON WHEN NECESSARY.]")
    if st.button("Clear and Repopulate Settings Cache",on_click=fetch_settings.clear,type="primary"):
        st.success("Cleared and repopulated settings cache",icon="🎉")
        rain(
            emoji="🐛",
            font_size=54,
            falling_speed=1,
            animation_length=1,
        )