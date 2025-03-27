import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

import unittest
from unittest.mock import patch, MagicMock

# Import the send_text function
from src.send_text import send_text

# For this test to pass, the below env vars need to be set up. They are not being properly set in the Terminal.


@patch.dict(
    os.environ,
    {
        "TWILIO_ACCOUNT_SID": "abc123",
        "TWILIO_AUTH_TOKEN": "xyz123",
        "SENDER_NUMBER": "+1234567890",
    },
)
@patch("src.send_text.client.messages.create")
@patch("src.send_text.getNameAndNumber")
class TestSendText(unittest.TestCase):
    def setup(self):
        os.environ["SENDER_NUMBER"] = "+1234567890"
        os.environ["TWILIO_AUTH_TOKEN"] = "xyz123"
        os.environ["TWILIO_ACCOUNT_SID"] = "abc123"
        print(os.environ)

    def test_send_text(self, mock_get_name_and_number, mock_create):
        print(os.environ)
        sender_number = os.getenv("SENDER_NUMBER")
        twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        # Ensure the environment variables are set correctly
        self.assertIsNotNone(sender_number)
        self.assertIsNotNone(twilio_auth_token)
        self.assertIsNotNone(twilio_account_sid)
        # Mock the getNameAndNumber function
        mock_get_name_and_number.return_value = [("John Doe", "234567890")]

        # Mock the Twilio message creation
        mock_message = MagicMock()
        mock_create.return_value = mock_message
        mock_message.error_code = None

        # Call the function
        send_text("hockey", "Patrick Kane")
        # Debugging: Print the call count
        print(f"mock_message: {mock_message.called_count}")
        print(f"mock_create.called_count: {mock_create.call_count}")
        print(f"mock_create.called: {mock_create.called}")

        # print(f"mock_msg: {mock_msg.called}")

        # Assert the Twilio messages were sent
        self.assertEqual(mock_create.call_count, 1)

        # assert mock_create.called is True
        # Confirm if this works on Sundays.
        mock_create.assert_called_with(
            body="Great news, John Doe! Patrick Kane scored in the first period at home. Free sandwich has landed for tomorrow.",
            from_=os.environ["SENDER_NUMBER"],
            to="+1234567890",
        )
        # mock_create.assert_called_with(
        #     body="Great news, Jane Smith! Free Chick-fil-a breakfast has landed in your CFA App.",
        #     from_=os.environ["SENDER_NUMBER"],
        #     to="+10987654321"
        # )


if __name__ == "__main__":
    unittest.main()
