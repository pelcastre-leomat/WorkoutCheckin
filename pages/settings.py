from datetime import date, timedelta
import time
import streamlit as st
from utils.db_enums import DB_Enums
import pandas as pd

@st.cache_data(persist="disk")
def fetch_settings():
    data = st.session_state.db_connection.fetch_data_table(
        table_id=DB_Enums.USER_SETTINGS_DB,
        offline=st.session_state.offline
    )
    return data

class Settings:
    def __init__(self,name):
        st.session_state.user_settings = fetch_settings()
        df = st.session_state.user_settings
        self.user_data = df[df[DB_Enums.NAME.value]== name.title()].iloc[0,1:-1].to_dict()
        st.session_state.settings_chaged = True
        

        self.has_changed = False
        today = date.today()
        next_week_date = today + timedelta(weeks=1)
        self.checkin_week = next_week_date.isocalendar().week

    def _set_workouts(self,num):
        if(num.isnumeric() and int(num)<=14):
            self.has_changed = not num == self.user_data[DB_Enums.WORKOUT_GOAL.value] if self.has_changed != True else self.user_data[DB_Enums.WORKOUT_GOAL.value]
            return num
        else:
            st.error("Please only input whole numeric values between 1 and 14.")
            return None

    def _set_cost(self,num):
        if(num.isnumeric()):
            self.has_changed = not num == self.user_data[DB_Enums.COST.value] if self.has_changed != True else self.user_data[DB_Enums.COST.value]
            return num
        else:
            st.error("Please only input numeric values.")
            return None

    def _send_data(self,updated_vals):
        st.session_state.settings_chaged = False
        self.user_data = updated_vals
        msg = st.info("Applying new settings",icon="⚙️")
        time.sleep(1)
        settings_queue = DB_Enums.SETTINGS_QUEUE.value
        data = {
            settings_queue:{
                DB_Enums.NAME.value:st.session_state.logged_name.title(),
                DB_Enums.WEEK.value:self.checkin_week
            }
        }
        data[settings_queue].update(updated_vals)
        if(st.session_state.offline):
            data[settings_queue].update({"id":99})
        try:
            update_queue = st.session_state.db_connection.send_data(
                table_id=DB_Enums.SETTINGS_QUEUE,
                sheet_name=settings_queue,
                data = data,
                offline=st.session_state.offline
            )
        except Exception as e:
            #Log sent to email?
            print(e)
            print("Could not change setting")
            msg.error("Could not change settings, try again later",icon="😭")
            return

        print(data)

        #TODO Error handling
        msg.success("Applied settings",icon="💪")
        # print(updated_vals)

    def show_settings(self):
        st.title("Settings")
        self.workout_goal = self.user_data[DB_Enums.WORKOUT_GOAL.value]
        self.workout_goal = self.user_data[DB_Enums.COST.value]
        n_workouts = self._set_workouts(st.text_input(label="Workout goal",value=self.user_data[DB_Enums.WORKOUT_GOAL.value]))
        cost = self._set_cost(st.text_input(label="Missed workout cost (SEK)",value=self.user_data[DB_Enums.COST.value]))
        st.button("Save changes",key="save_btn",on_click=self._send_data,kwargs={"updated_vals":{DB_Enums.WORKOUT_GOAL.value:n_workouts,DB_Enums.COST.value:cost}},disabled=not self.has_changed)


