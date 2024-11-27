from datetime import datetime
import requests
import json
import datetime
import os
import os
from datetime import datetime, timedelta

from src import get_name_and_number
from src.send_text import send_text


# Find your Account SID and Auth Token at twilio.com/console

# and set the environment variables. See http://twil.io/secure



def get_game_id():
    today = datetime.today() - timedelta(hours=8)
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")
    # day = "21" # Use sample blackhawks game with this
    todays_score_api = f"https://api-web.nhle.com/v1/score/{year}-{month}-{day}"
    response = requests.get(todays_score_api)


    # This CURL gets the game ID for today and saves it if Chi is in the list.
    game_id = ""
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # print(data)
        # Now you can work with the JSON data
        for item in data["games"]:
            # print(item)
            if item["venue"]["default"] == "United Center":
                print(item["id"])
                game_id = item["id"]
                game_summary_func(game_id)
    else:
        print("Error: ", response.status_code)


# GAME SUMMARY
def game_summary_func(game_id):
    game_summary = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/landing"
    response = requests.get(game_summary)
    goal_result = False
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # print(data['summary']['scoring'][0])
        first_period = data["summary"]["scoring"][0]["goals"]
        for goal in first_period:
            print(goal)
            if goal["teamAbbrev"]["default"] == "CHI":
                goal_result = True
                break
            else:
                continue
    else:
        print("Error: ", response.status_code)

    send_text(goal_result)

def main():
    get_game_id()

if __name__ == "__main__":
    main()
