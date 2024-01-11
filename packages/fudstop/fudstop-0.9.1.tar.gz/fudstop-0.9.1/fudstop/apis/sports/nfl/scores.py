import pandas as pd

class Sports:
    def __init__(self, response):




        self.id = [i.get('id') for i in response]
        self.time = [i.get('commence_time') for i in response]
        self.completed = [i.get('completed') for i in response]
        self.home_team = [i.get('home_team') for i in response]
        self.away_team = [i.get('away_team') for i in response]
        self.last_update = [i.get('last_update') for i in response]
        self.sports_key = [i.get('sports_key') for i in response]
        self.sport_title = [i.get('sport_title') for i in response]
        scores = [i.get('score') for i in response]

        self.score_name = [i.get('name') for i in scores]
        self.score = [i.get('score') for i in scores]



        self.data_dict = { 
            'id': self.id,
            'time': self.time,
            'completed': self.completed,
            'home_team': self.home_team,
            'away_team': self.away_team,
            'last_updated': self.last_update,
            'sports_key': self.sports_key,
            'sports_title': self.sport_title,
            'team_name': self.score_name,
            'team_score': self.score
        }



        self.as_dataframe = pd.DataFrame(self.data_dict)


