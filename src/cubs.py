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
import boto3
from boto3.dynamodb.conditions import Key
import pytz

from send_text import send_text


# DynamoDB functions
def get_phone_numbers_table():
  """Get the phone numbers table for sending texts"""
  dynamodb = boto3.resource('dynamodb')
  return dynamodb.Table('ChickfilaData')


def get_notifications_table():
  """Get the notifications table for tracking sent texts"""
  dynamodb = boto3.resource('dynamodb')
  return dynamodb.Table('ChickFilADataSent')


def check_if_cubs_text_sent_today():
  """Check if Cubs text was already sent today"""
  table = get_notifications_table()
  # Always use Central Time, even in Lambda
  central_tz = pytz.timezone('America/Chicago')
  central_time = datetime.now(central_tz)
  today_str = central_time.strftime("%Y-%m-%d")

  print(f"Checking if text sent for Central Time date: {today_str}")

  try:
    response = table.get_item(
      Key={
        'NotificationKey': f'cubs-{today_str}'
      }
    )
    return 'Item' in response
  except Exception as e:
    print(f"Error checking DynamoDB: {e}")
    return False


def mark_cubs_text_sent_today():
  """Mark that Cubs text was sent today"""
  table = get_notifications_table()
  # Always use Central Time, even in Lambda
  central_tz = pytz.timezone('America/Chicago')
  central_time = datetime.now(central_tz)
  today_str = central_time.strftime("%Y-%m-%d")

  try:
    table.put_item(
      Item={
        'NotificationKey': f'cubs-{today_str}',
        'text_sent': True,
        'date': today_str,
        'timestamp': datetime.now(timezone.utc).isoformat()
      }
    )
    print(f"Marked Cubs text as sent for {today_str} (Central Time)")
  except Exception as e:
    print(f"Error marking DynamoDB: {e}")


# For Local dev
def main():
  mlb = mlbstatsapi.Mlb()
  today = datetime.now(timezone.utc)
  year = today.strftime("%Y")
  month = today.strftime("%m")
  day = today.strftime("%d")

  print(f"Looking for Cubs games on: {year}-{month}-{day}")
  print(f"Current UTC time: {today}")

  cubs_schedule = mlb.get_scheduled_games_by_date(
    start_date=f"{year}-{month}-{day}",
    end_date=f"{year}-{month}-{day}",
    teamId=112,
    sportId=1,
  )

  print(cubs_schedule)
  if len(cubs_schedule) == 0:
    print("No Cubs game found for today, checking yesterday...")
    # Try yesterday in case the game already finished
    yesterday = today - timedelta(days=1)
    yesterday_year = yesterday.strftime("%Y")
    yesterday_month = yesterday.strftime("%m")
    yesterday_day = yesterday.strftime("%d")

    print(f"Looking for Cubs games on: {yesterday_year}-{yesterday_month}-{yesterday_day}")

    cubs_schedule = mlb.get_scheduled_games_by_date(
      start_date=f"{yesterday_year}-{yesterday_month}-{yesterday_day}",
      end_date=f"{yesterday_year}-{yesterday_month}-{yesterday_day}",
      teamId=112,
      sportId=1,
    )

    print(cubs_schedule)
    if len(cubs_schedule) == 0:
      print("No Cubs game found for yesterday either")
      return
  for item in cubs_schedule:
    gamepk = mlb.get_game_box_score(item.gamepk)
    if gamepk.teams.home.team.id == 112:
      print("Cubs home game found")
      # Use raw MLB API to get play-by-play data
      game_feed_url = f"https://statsapi.mlb.com/api/v1.1/game/{item.gamepk}/feed/live"
      response = requests.get(game_feed_url)
      game_data = response.json()

      # Debug: Print the structure
      print("Game data keys:", list(game_data.keys()))

      # Look for play-by-play data
      if 'liveData' in game_data and 'plays' in game_data['liveData']:
        plays = game_data['liveData']['plays']
        print("Plays keys:", list(plays.keys()))

        if 'allPlays' in plays:
          all_plays = plays['allPlays']
          print(f"Number of plays: {len(all_plays)}")

          if len(all_plays) > 0:
            first_play = all_plays[0]
            print("First play keys:", list(first_play.keys()))

            # Check for result and about structure
            if 'result' in first_play:
              print("Result keys:", list(first_play['result'].keys()))
              if 'eventType' in first_play['result']:
                print("Event type example:", first_play['result']['eventType'])

            if 'about' in first_play:
              print("About keys:", list(first_play['about'].keys()))
              if 'halfInning' in first_play['about']:
                print("Half inning example:", first_play['about']['halfInning'])
              if 'inning' in first_play['about']:
                print("Inning example:", first_play['about']['inning'])

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

              # Check if text already sent today
              if not check_if_cubs_text_sent_today():
                send_text("Cubs", f"The Cubs struck out {strikeouts} batters in inning {inning}!")
                mark_cubs_text_sent_today()
              else:
                print("Cubs text already sent today, skipping notification")
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
