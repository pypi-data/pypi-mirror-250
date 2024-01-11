import os
from dotenv import load_dotenv
from .scores import Sports
import requests
load_dotenv()


class NFLSDK:
    def __init__(self):
        self.key = os.environ.get('rapid_api_key')
        self.nfl_host = os.environ.get('rapid_api_nfl')




    def nfl_scores(self, days_from_game:str='3'):
        url = "https://odds.p.rapidapi.com/v4/sports/americanfootball_nfl/scores"

        querystring = {"daysFrom":days_from_game}

        headers = {
            "X-RapidAPI-Key": os.environ.get('rapid_api_key'),
            "X-RapidAPI-Host": os.environ.get('rapid_api_nfl')
        }

        response = requests.get(url, headers=headers, params=querystring).json()



        data = Sports(response)

        return data.as_dataframe