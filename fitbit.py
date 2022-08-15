import dotenv
import os
import requests
import base64
import json
from datetime import datetime as dt
dotenv.load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


class FitbitAPI():
    def __init__(self):
        self.access_token, self.refresh_token = self.get_tokens()
        
    def get_tokens(self):
        try:
            data = json.load(open('tokens.json','r'))
            return [data['access_token'], data['refresh_token']]
        except:
            return self.authorize()

    def store_tokens(self, access, refresh):
        self.access_token = access
        self.refresh_token = refresh
        json.dump({
            "access_token": access,
            "refresh_token": refresh
        }, open("tokens.json","w"))

    def authorize(self):
        url = f"https://www.fitbit.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&scope=activity&client_secret={CLIENT_SECRET}"
        print(url)
        auth_code = input("Authorization Code: ")
        authorization_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
        encoded_string = str(base64.b64encode(authorization_string.encode('utf-8')),'utf-8')
        r = requests.post(f'https://api.fitbit.com/oauth2/token?code={auth_code}&grant_type=authorization_code&client_id={CLIENT_ID}', headers={
            'authorization': f'Basic {encoded_string}',
            'content-type': 'application/x-www-form-urlencoded'
        })
        data = r.json()
        self.store_tokens(data['access_token'], data['refresh_token'])
        return [data['access_token'], data['refresh_token']]

    def refresh_tokens(self):
        authorization_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
        encoded_string = str(base64.b64encode(authorization_string.encode('utf-8')),'utf-8')
        r = requests.post(f'https://api.fitbit.com/oauth2/token?refresh_token={self.refresh_token}&grant_type=refresh_token&client_id={CLIENT_ID}', headers={
            'authorization': f'Basic {encoded_string}',
            'content-type': 'application/x-www-form-urlencoded'
        })
        data = r.json()
        self.store_tokens(data['access_token'], data['refresh_token'])
        return [data['access_token'], data['refresh_token']]

    def get_data(self,url):
        r = requests.get(url, headers={
            'authorization': f'Bearer {self.access_token}'
        })
        if r.status_code == 200:
            return r
        self.refresh_tokens()
        return self.get_data(url)

    def get_todays_data(self):
        url = f'https://api.fitbit.com/1/user/-/activities/date/{dt.now().strftime("%Y-%m-%d")}.json'
        r = self.get_data(url)
        data = r.json()
        return {
            "calories": data["summary"]["caloriesOut"],
            "distance": data["summary"]["distances"][0]["distance"],
            "steps": data["summary"]["steps"]\
        }

    def get_lifetime_stats(self):
        url = f'https://api.fitbit.com/1/user/-/activities.json'
        r = self.get_data(url)
        data = r.json()
        return {
            "best": {
                "steps": data["best"]["total"]["steps"],
                "distance": data["best"]["total"]["distance"],
            },
            "lifetime": {
                "steps": data["lifetime"]["total"]["steps"],
                "distance": data["lifetime"]["total"]["distance"]
            }
        }
    def get_activites(self):
        url = f'https://api.fitbit.com/1/user/-/activities/list.json?beforeDate={dt.now().strftime("%Y-%m-%d")}&sort=desc&limit=3&offset=0'
        r = self.get_data(url)
        data = r.json()
        return [{
            "name": activity["activityName"],
            "calories": activity["calories"],
            "duration": activity["duration"],
            "startTime": activity["startTime"]
        } for activity in data["activities"]]


if __name__ == "__main__":
    f = FitbitAPI()
    print(f.get_todays_data())
    print(f.get_lifetime_stats())
    print(f.get_activites())
