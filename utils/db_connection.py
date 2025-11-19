import json
import requests
from streamlit import secrets
import pandas as pd

class DB_Connection:
    def __init__(self):
        self.base_url = f"https://api.sheety.co/{secrets['sheet_project_path']}"
        self.headers = {"Authorization": f"Bearer {secrets['sheet_bearer_url']}"}

    def fetch_data_table(self, table_id, offline=False,filter_options=None):
        if(offline):
            print("Using offline data")
            with open(f"data/{table_id}.json") as f:
                data = json.load(f)
        else:
            print("Fetching live data")
            filter_options = "" if filter_options is None else f"?filter{filter_options}"
            url = f"{self.base_url}/{table_id}{filter_options}"
            print(url)
            resp = requests.get(url, headers=self.headers)
            resp.raise_for_status()
            data = resp.json()
            print(data)
        data = next(iter(data.values()))
        df = pd.DataFrame(data)
        df = df.drop("id",axis=1)
        print(df)
        return df

    def send_data(self, table_id, data, offline=False):
        if(offline):
            with open(f"data/{table_id}.json", "w") as f:
                json.dump(data, f, indent=2)
        else:
            url = f"{self.base_url}/{table_id}"
            resp = requests.post(url, headers=self.headers, json=data)
            resp.raise_for_status()
            return resp.json()

    def delete_entry(self, table_id, entry_id, offline=False):
        if(offline):
            print(f"Would delete entry {entry_id} from {table_id} locally.")
        else:
            url = f"{self.base_url}/{table_id}/{entry_id}"
            resp = requests.delete(url, headers=self.headers)
            resp.raise_for_status()
            return resp.json()

    def update_entry(self, table_id, entry_id, data, offline=False):
        if(offline):
            print(f"Would update entry {entry_id} with {data} locally.")
        else:
            url = f"{self.base_url}/{table_id}/{entry_id}"
            resp = requests.put(url, headers=self.headers, json=data)
            resp.raise_for_status()
            return resp.json()
