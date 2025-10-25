import datetime
import requests
import streamlit as st

sheet_url = st.secrets["sheet_url"]
sheet_bearer_key = st.secrets["sheet_bearer_url"]
sheety_endpoint = f"https://api.sheety.co/{sheet_url}"

def save_to_file(name:str,date:datetime.date):
    week_num = date.isocalendar()[1]
    headers = {
        "Authorization":f"Bearer {sheet_bearer_key}"
    }
    workout = {
        "workout":{
            "name":name,
            "day": date.strftime("%d/%m/%Y"),
            "week":week_num,
        }
    }
    req = requests.post(url=sheety_endpoint,json=workout,headers=headers)
