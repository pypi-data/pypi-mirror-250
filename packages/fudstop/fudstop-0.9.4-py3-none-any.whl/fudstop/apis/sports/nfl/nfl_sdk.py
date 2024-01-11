import os
from dotenv import load_dotenv
from .scores import Sports
import requests
load_dotenv()


class NFLSDK:
    def __init__(self):
        self.key = os.environ.get('rapid_api_key')
        self.nfl_host = os.environ.get('rapid_api_nfl')




    def nfl_scores(self):
        url = "https://odds.p.rapidapi.com/v4/sports/americanfootball_nfl/scores"

        querystring = {"daysFrom":"3"}

        headers = {
            "X-RapidAPI-Key": self.key,
            "X-RapidAPI-Host": self.nfl_host
        }

        response = requests.get(url, headers=headers, params=querystring).json()

        print(response)

        data = Sports(response)

        return data.as_dataframe
    
    # Function to fetch data
    def fetch_odds(self):
        url = "https://odds.p.rapidapi.com/v4/sports/upcoming/odds"
        querystring = {"regions":"us","oddsFormat":"decimal","markets":"h2h,spreads","dateFormat":"iso"}
        headers = {
            "X-RapidAPI-Key": os.environ.get('rapid_api_key'),  # Replace with your API Key
            "X-RapidAPI-Host": "odds.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        print(response.json())
        return response.json()