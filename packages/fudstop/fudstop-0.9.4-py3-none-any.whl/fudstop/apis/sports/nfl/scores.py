import pandas as pd

class Sports:
    def __init__(self, response):




        self.id = [i.get('id') for i in response] if len(response) > 0 else response.get('id', None)
        self.time = [i.get('commence_time') for i in response]
        self.completed = [i.get('completed') for i in response]
        self.home_team = [i.get('home_team') for i in response]
        self.away_team = [i.get('away_team') for i in response]
        self.last_update = [i.get('last_update') for i in response]
        self.sports_key = [i.get('sport_key') for i in response]
        self.sport_title = [i.get('sport_title') for i in response]
        scores = [i.get('score') for i in response]

        self.score_name = []
        self.score = []

        for game in scores:
            # Check if the game itself is None
            if game is None:
                self.score_name.append("N/A")
                self.score.append("N/A")
            elif not game.get('scores'):  # Check if 'scores' is None or empty
                self.score_name.append("UPCOMING")
                self.score.append("-")
            else:
                # Iterate over each score in the game
                for team in game['scores']:
                    # Check if team is not None
                    if team is not None:
                        # Get the team's name, use "UPCOMING" as default if None
                        team_name = team.get('name', "UPCOMING")
                        self.score_name.append(team_name)

                        # Get the team's score, use "-" as default if None
                        team_score = team.get('score', "-")
                        self.score.append(team_score)
                    else:
                        self.score_name.append("UPCOMING")
                        self.score.append("-")


        self.data_dict = { 
            'id': self.id,
            'commence_time': self.time,
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


class SportsEvent:
    def __init__(self, event_data):
        self.id = event_data.get('id')
        self.sport_key = event_data.get('sport_key')
        self.sport_title = event_data.get('sport_title')
        self.commence_time = event_data.get('commence_time')
        self.home_team = event_data.get('home_team')
        self.away_team = event_data.get('away_team')
        self.bookmakers = self.parse_bookmakers(event_data.get('bookmakers', []))

    def parse_bookmakers(self, bookmakers_data):
        bookmakers = []
        for bookmaker in bookmakers_data:
            bookmaker_info = {
                'key': bookmaker.get('key'),
                'title': bookmaker.get('title'),
                'last_update': bookmaker.get('last_update'),
                'markets': self.parse_markets(bookmaker.get('markets', []))
            }
            bookmakers.append(bookmaker_info)
        return bookmakers

    def parse_markets(self, markets_data):
        markets = []
        for market in markets_data:
            market_info = {
                'key': market.get('key'),
                'last_update': market.get('last_update'),
                'outcomes': self.parse_outcomes(market.get('outcomes', []))
            }
            markets.append(market_info)
        return markets

    def parse_outcomes(self, outcomes_data):
        outcomes = []
        for outcome in outcomes_data:
            outcome_info = {
                'name': outcome.get('name'),
                'price': outcome.get('price'),
                'point': outcome.get('point', None)  # 'point' might not be present
            }
            outcomes.append(outcome_info)
        return outcomes

    def __str__(self):
        return f"{self.sport_title} - {self.home_team} vs {self.away_team}"