import time
import streamlit as st

class Settings:
    def __init__(self):
        if(st.session_state.user_settings is None):
            st.session_state.user_settings = self._fetch_settings()
        st.session_state.settings_chaged = True
        self.has_changed = False

    def _set_workouts(self,num):
        if(num.isnumeric() and int(num)<=14):
            self.has_changed = not num == st.session_state.user_settings["workout_goal"] if self.has_changed != True else st.session_state.user_settings["workout_goal"]
            return num
        else:
            st.error("Please only input whole numeric values between 1 and 14.")
            return None

    def _set_cost(self,num):
        if(num.isnumeric()):
            self.has_changed = not num == st.session_state.user_settings["cost"] if self.has_changed != True else st.session_state.user_settings["cost"]
            return num
        else:
            st.error("Please only input numeric values.")
            return None

    def _send_data(self,updated_vals):
        st.session_state.settings_chaged = False
        st.session_state.user_settings = updated_vals
        msg = st.info("Applying new settings",icon="⚙️")
        time.sleep(1)
        #TODO Error handling
        msg.success("Applied settings",icon="💪")
        print(updated_vals)

    def show_settings(self):
        st.title("Settings")
        self.workout_goal = st.session_state.user_settings["workout_goal"]
        self.workout_goal = st.session_state.user_settings["cost"]
        n_workouts = self._set_workouts(st.text_input(label="Workout goal",value=st.session_state.user_settings["workout_goal"]))
        cost = self._set_cost(st.text_input(label="Missed workout cost (SEK)",value=st.session_state.user_settings["cost"]))
        st.button("Save changes",key="save_btn",on_click=self._send_data,kwargs={"updated_vals":{"workout_goal":n_workouts,"cost":cost}},disabled=not self.has_changed)

    def _fetch_settings(self):
        return {"workout_goal":"3","cost":"30"}
