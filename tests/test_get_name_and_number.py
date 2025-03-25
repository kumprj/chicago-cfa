import unittest
import os
from unittest.mock import patch, MagicMock
from src.get_name_and_number import getNameAndNumber

class TestGetNameAndNumber(unittest.TestCase):
    def setup(self):
        os.environ['SENDER_NUMBER'] = '+1234567890'
        os.environ['TWILIO_AUTH_TOKEN'] = 'xyz123'
        os.environ['TWILIO_ACCOUNT_SID'] = 'abc123'
    @patch('src.get_name_and_number.boto3.resource')
    def test_get_name_and_number(self, mock_boto3_resource):
        # Mock the DynamoDB table and its scan method
        sender_number = os.getenv('SENDER_NUMBER')
        twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        # Ensure the environment variables are set correctly
        self.assertIsNotNone(sender_number)
        self.assertIsNotNone(twilio_auth_token)
        self.assertIsNotNone(twilio_account_sid)

        mock_table = MagicMock()
        mock_boto3_resource.return_value.Table.return_value = mock_table
        mock_table.scan.return_value = {
            'Items': [
                {'Name': 'John Doe', 'Phone': '1234567890'},
                {'Name': 'Jane Smith', 'Phone': '0987654321'}
            ]
        }

        # Call the function
        result = getNameAndNumber()

        # Assert the expected result
        expected_result = [('John Doe', '1234567890'), ('Jane Smith', '0987654321')]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()