from unittest import TestCase
from unittest.mock import patch, MagicMock
import os
from src.free_cfa import get_game_id

class TestFreeCfa(TestCase):
    def setUp(self):
        os.environ['SENDER_NUMBER'] = '+1234567890'
        os.environ['TWILIO_AUTH_TOKEN'] = 'xyz123'
        os.environ['TWILIO_ACCOUNT_SID'] = 'abc123'
    @patch('src.free_cfa.requests.get')
    @patch('src.free_cfa.game_summary_func')
    def test_get_game_id(self, mock_game_summary_func, mock_requests_get):
        # Mock the DynamoDB table and its scan method
        sender_number = os.getenv('SENDER_NUMBER')
        twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        # Ensure the environment variables are set correctly
        self.assertIsNotNone(sender_number)
        self.assertIsNotNone(twilio_auth_token)
        self.assertIsNotNone(twilio_account_sid)
        # Mock the response from the requests.get call
        mock_response = MagicMock()
        mock_requests_get.return_value = mock_response

        # Mock a successful response with a game at United Center
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "games": [
                {
                    "id": "12345",
                    "venue": {"default": "United Center"}
                }
            ]
        }

        # Call the function
        get_game_id()

        # Assert the game_summary_func was called with the correct game_id
        mock_game_summary_func.assert_called_once_with("12345")

    @patch('src.free_cfa.requests.get')
    def test_get_game_id_no_games(self, mock_requests_get):
        # Mock the response from the requests.get call
        mock_response = MagicMock()
        mock_requests_get.return_value = mock_response

        # Mock a successful response with no games at United Center
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "games": [
                {
                    "id": "12345",
                    "venue": {"default": "Other Venue"}
                }
            ]
        }

        # Call the function
        get_game_id()

        # Assert the game_summary_func was not called
        mock_requests_get.assert_called_once()