# >>> mlb = mlbstatsapi.Mlb()
# >>> game = mlb.get_game(662242)
# >>>
# >>> play_by_play = game.livedata.plays
# >>> line_score = game.livedata.linescore
# >>> box_score = game.livedata.boxscore
# ^^ live data

# Game box score:
# >>> mlb = mlbstatsapi.Mlb()
# >>> boxscore = mlb.get_box_score(662242)


# https://github.com/zero-sum-seattle/python-mlb-statsapi

import mlbstatsapi
import os
import requests

from send_text import send_text


# For Local dev
def main():
    mlb = mlbstatsapi.Mlb()
    cubs_schedule = mlb.get_scheduled_games_by_date(
        start_date="2025-03-25", end_date="2025-03-25", teamId=112, sportId=1
    )

    print(cubs_schedule)
    if len(cubs_schedule) == 0:
        print("No games today")
        return
    for item in cubs_schedule:
        gamepk = mlb.get_game_box_score(item.gamepk)
        if gamepk.teams.home.team.id == 112:
            print("got here")
            todays_score_api = (
                f"https://statsapi.mlb.com/api/v1/schedule?gamePk={item.gamepk}"
            )
            response = requests.get(todays_score_api)
            data = response.json()
            for item in data["dates"]:
                home_team_info = item["games"][0]["teams"]["home"]["team"]["name"]
                home_team_winner = item["games"][0]["teams"]["home"]["isWinner"]
                if home_team_info == "Chicago Cubs" and home_team_winner == True:
                    print("Cubs won today at home!")
                    # send_text("baseball", "Cubs")
                if home_team_info == "Chicago Cubs" and home_team_winner == False:
                    print("Cubs lost today at home :( ")


# Lambda Handlers
def lambda_handler(event, context):
    main()


# For Local dev
if __name__ == "__main__":
    main()
