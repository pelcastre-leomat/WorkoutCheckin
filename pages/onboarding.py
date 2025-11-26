import streamlit as st

def show_page():
    st.set_page_config(page_title="Onboarding")

    st.title("Welcome!")
    st.write("Please enter a few details to get started.")

    # Collect onboarding inputs
    name = st.text_input("Your Name")
    age = st.number_input("Age", min_value=1, max_value=120)
    email = st.text_input("Email Address")

    # Validation + navigation
    if st.button("Continue"):
        if not name or not email:
            st.error("Please fill in all required fields.")
        else:
            # save to session state so next page can read it
            st.session_state["user_name"] = name
            st.session_state["user_age"] = age
            st.session_state["user_email"] = email

            st.switch_page("sections/check_in.py")
