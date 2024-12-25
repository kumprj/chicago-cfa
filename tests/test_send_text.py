import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import unittest
from unittest.mock import patch, MagicMock
from src.blackhawks_cfa.send_text import send_text, delete_data, polish_number
from src.blackhawks_cfa.get_name_and_number import getNameAndNumber
class TestSendText(unittest.TestCase):

    @patch('src.blackhawks_cfa.send_text.getNameAndNumber')
    @patch('src.blackhawks_cfa.send_text.client.messages.create')
    def test_send_text(self, mock_create, mock_get_name_and_number):
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

        # Assert the Twilio messages were sent
        self.assertEqual(mock_create.call_count, 2)
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

    @patch('src.blackhawks_cfa.send_text.phone_numbers_table.delete_item')
    def test_delete_data(self, mock_delete_item):
        # Call the function
        delete_data('John Doe', '1234567890')

        # Assert the delete_item was called with correct parameters
        mock_delete_item.assert_called_once_with(
            Key={"Name": 'John Doe', "Number": "GRP1#1234567890"}
        )

    def test_polish_number(self):
        # Test cases for polish_number function
        self.assertEqual(polish_number('+1-123-456-7890'), '1234567890')
        self.assertEqual(polish_number('+11234567890'), '1234567890')
        self.assertEqual(polish_number('123-456-7890'), '1234567890')
        self.assertEqual(polish_number('1234567890'), '1234567890')

if __name__ == '__main__':
    unittest.main()