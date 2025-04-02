import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone
import requests
import cubs

class TestCubsMain(unittest.TestCase):
    @patch("cubs.mlbstatsapi.Mlb")
    @patch("cubs.requests.get")
    def test_no_cubs_game_today(self, mock_requests_get, mock_mlb):
        # Mock the MLB API response for no games
        mock_mlb_instance = mock_mlb.return_value
        mock_mlb_instance.get_scheduled_games_by_date.return_value = []

        with patch("builtins.print") as mock_print:
            cubs.main()
            mock_print.assert_any_call("No Cubs game today")

    @patch("cubs.mlbstatsapi.Mlb")
    @patch("cubs.requests.get")
    def test_cubs_win_at_home(self, mock_requests_get, mock_mlb):
        # Mock the MLB API response for a Cubs home win
        mock_mlb_instance = mock_mlb.return_value
        mock_mlb_instance.get_scheduled_games_by_date.return_value = [
            MagicMock(gamepk=12345)
        ]
        mock_game_box_score = MagicMock()
        mock_game_box_score.teams.home.team.id = 112
        mock_mlb_instance.get_game_box_score.return_value = mock_game_box_score

        mock_requests_get.return_value.json.return_value = {
            "dates": [
                {
                    "games": [
                        {
                            "teams": {
                                "home": {
                                    "team": {"name": "Chicago Cubs"},
                                    "isWinner": True,
                                }
                            }
                        }
                    ]
                }
            ]
        }

        with patch("builtins.print") as mock_print:
            cubs.main()
            mock_print.assert_any_call("Cubs won today at home!")

    @patch("cubs.mlbstatsapi.Mlb")
    @patch("cubs.requests.get")
    def test_cubs_lose_at_home(self, mock_requests_get, mock_mlb):
        # Mock the MLB API response for a Cubs home loss
        mock_mlb_instance = mock_mlb.return_value
        mock_mlb_instance.get_scheduled_games_by_date.return_value = [
            MagicMock(gamepk=12345)
        ]
        mock_game_box_score = MagicMock()
        mock_game_box_score.teams.home.team.id = 112
        mock_mlb_instance.get_game_box_score.return_value = mock_game_box_score

        mock_requests_get.return_value.json.return_value = {
            "dates": [
                {
                    "games": [
                        {
                            "teams": {
                                "home": {
                                    "team": {"name": "Chicago Cubs"},
                                    "isWinner": False,
                                }
                            }
                        }
                    ]
                }
            ]
        }

        with patch("builtins.print") as mock_print:
            cubs.main()
            mock_print.assert_any_call("Cubs lost today at home :( ")

    @patch("cubs.mlbstatsapi.Mlb")
    @patch("cubs.requests.get")
    def test_non_cubs_game(self, mock_requests_get, mock_mlb):
        # Mock the MLB API response for a non-Cubs game
        mock_mlb_instance = mock_mlb.return_value
        mock_mlb_instance.get_scheduled_games_by_date.return_value = [
            MagicMock(gamepk=12345)
        ]
        mock_game_box_score = MagicMock()
        mock_game_box_score.teams.home.team.id = 999  # Not Cubs team ID
        mock_mlb_instance.get_game_box_score.return_value = mock_game_box_score

        with patch("builtins.print") as mock_print:
            cubs.main()
            # mock_print.assert_any_call("got here")  # Ensure it reaches the logic


if __name__ == "__main__":
    unittest.main()