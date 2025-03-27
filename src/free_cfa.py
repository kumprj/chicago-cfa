from datetime import datetime, timezone
import requests
import datetime
from datetime import datetime, timedelta
from send_text import send_text


# Loop through all the games from today to check if we have any that are Chicago/United Center.
def get_game_id():
    today = datetime.now(timezone.utc) - timedelta(days=1)
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")
    # day = "21"  # Use this for sample blackhawks game day testing.
    # month = '11' # Use this for sample blackhawks game day testing.
    todays_score_api = f"https://api-web.nhle.com/v1/score/{year}-{month}-{day}"
    response = requests.get(todays_score_api)

    # This CURL gets the game ID values for today and saves it if Chi is in the list.
    game_id = ""
    if response.status_code == 200:
        data = response.json()
        for item in data["games"]:
            # print(item) # For testing purposes as needed.
            if item["venue"]["default"] == "United Center":
                print(item["id"])
                game_id = item["id"]
                game_summary_func(game_id)

    else:
        print("Error: ", response.status_code)


# GAME SUMMARY - NHL Api. This returns the goals for the game by period.
def game_summary_func(game_id):
    game_summary = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/landing"
    response = requests.get(game_summary)
    player_scoring = ""
    goal_result = False
    if response.status_code == 200:

        data = response.json()
        first_period = data["summary"]["scoring"][0]["goals"]
        for goal in first_period:
            print(goal)
            if goal["teamAbbrev"]["default"] == "CHI":
                goal_result = True
                player_scoring = (
                    goal["firstName"]["default"] + " " + goal["lastName"]["default"]
                )
                print(f"player_scoring was {player_scoring}")
                break
            else:
                continue
    else:
        print("Error: ", response.status_code)

    if goal_result == True:
        send_text("Blackhawks", player_scoring)


# Lambda Handlers
def lambda_handler(event, context):
    get_game_id()


# # For Local dev
# def main():
#     get_game_id()

# # For Local dev
# if __name__ == "__main__":
#     main()
