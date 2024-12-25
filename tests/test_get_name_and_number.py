import unittest
from unittest.mock import patch, MagicMock
from src.blackhawks_cfa.get_name_and_number import getNameAndNumber

class TestGetNameAndNumber(unittest.TestCase):

    @patch('src.blackhawks_cfa.get_name_and_number.boto3.resource')
    def test_get_name_and_number(self, mock_boto3_resource):
        # Mock the DynamoDB table and its scan method
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