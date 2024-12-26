import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import unittest
from unittest.mock import patch, MagicMock

# Import the send_text function
from src.send_text import send_text

@patch.dict(os.environ, {
    "TWILIO_ACCOUNT_SID": "abc123",
    "TWILIO_AUTH_TOKEN": "xyz123",
    "SENDER_NUMBER": "+1234567890"
})
@patch('src.send_text.client.messages.create')
@patch('src.send_text.getNameAndNumber')
class TestSendText(unittest.TestCase):

    def test_send_text(self, mock_get_name_and_number, mock_create):
        # Mock the getNameAndNumber function
        mock_get_name_and_number.return_value = [
            ('John Doe', '1234567890'),
            ('Jane Smith', '0987654321')
        ]

        # Mock the Twilio message creation
        mock_message = MagicMock()
        mock_create.return_value = mock_message
        mock_message.error_code = None

        # Call the function
        send_text()
        # Debugging: Print the call count
        print(f"mock_create: {mock_create}")

        # Assert the Twilio messages were sent
        self.assertEqual(mock_create, 2)
        mock_create.assert_any_call(
            body='Great news, John Doe! Free Chick-fil-a breakfast has landed in your CFA App.',
            from_=os.environ["SENDER_NUMBER"],
            to='+11234567890'
        )
        mock_create.assert_any_call(
            body='Great news, Jane Smith! Free Chick-fil-a breakfast has landed in your CFA App.',
            from_=os.environ["SENDER_NUMBER"],
            to='+10987654321'
        )

if __name__ == '__main__':
    unittest.main()