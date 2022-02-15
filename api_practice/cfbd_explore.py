import cfbd
import time
import pandas as pd
import numpy as np


configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = 'HZ/BOzuiV0K6nL6tfibIjEcjI8F5dO82dpIBnyb3yWAk1jb4P5XDbyVlMDheyEDe'
configuration.api_key_prefix['Authorization'] = 'Bearer'

api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))

frames = []
for j in range(2000, 2022):
    games = api_instance.get_games(year=j)
    print(j)
    season_df = pd.DataFrame.from_records([dict(id=games[i].id, year=int(j), week=games[i].week, home_team=games[i].home_team, home_conference=games[i].home_conference, home_points=games[i].home_points, away_team=games[i].away_team, away_conference=games[i].away_conference, away_points=games[i].away_points) for i in range(len(games))])
    season_df['winning_team'] = np.where(season_df['home_points'] > season_df['away_points'], season_df['home_team'], season_df['away_team'])
    frames.append(season_df)
    time.sleep(0.25)

seasons_df = pd.concat(frames)
