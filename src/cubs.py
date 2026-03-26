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
from datetime import datetime, timedelta, timezone
import requests

from send_text import send_text


# For Local dev
def main():
    mlb = mlbstatsapi.Mlb()
    today = datetime.now(timezone.utc)
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")
    cubs_schedule = mlb.get_scheduled_games_by_date(
        start_date=f"{year}-{month}-{day}",
        end_date=f"{year}-{month}-{day}",
        teamId=112,
        sportId=1,
    )

    print(cubs_schedule)
    if len(cubs_schedule) == 0:
        print("No Cubs game today")
        return
    for item in cubs_schedule:
        gamepk = mlb.get_game_box_score(item.gamepk)
        if gamepk.teams.home.team.id == 112:
            print("Cubs home game found")
            # Use raw MLB API to get play-by-play data
            game_feed_url = f"https://statsapi.mlb.com/api/v1.1/game/{item.gamepk}/feed/live"
            response = requests.get(game_feed_url)
            game_data = response.json()
            
            # Look for play-by-play data
            if 'liveData' in game_data and 'plays' in game_data['liveData']:
                plays = game_data['liveData']['plays']
                
                if 'allPlays' in plays:
                    all_plays = plays['allPlays']
                    
                    # Track strikeouts by inning for Cubs pitching (TOP innings at home)
                    innings_strikeouts = {}
                    
                    for play in all_plays:
                        # At home, Cubs pitch in TOP innings
                        if (play.get('about', {}).get('halfInning') == "top" and
                            play.get('result', {}).get('eventType') == "strikeout"):
                            
                            inning = play['about']['inning']
                            if inning not in innings_strikeouts:
                                innings_strikeouts[inning] = 0
                            innings_strikeouts[inning] += 1
                    
                    # Check if any inning had 3 or more strikeouts
                    three_k_inning = False
                    for inning, strikeouts in innings_strikeouts.items():
                        if strikeouts >= 3:
                            print(f"Cubs struck out {strikeouts} batters in inning {inning}!")
                            three_k_inning = True
                            send_text("Cubs", f"Cubs struck out {strikeouts} batters in inning {inning}!")
                            break
                    
                    if not three_k_inning:
                        print("No inning with 3+ strikeouts by Cubs today")
                else:
                    print("No allPlays found in plays data")
            else:
                print("No liveData.plays found in game data")
            break


# Lambda Handlers
def lambda_handler(event, context):
    main()


# For Local dev
if __name__ == "__main__":
    main()
