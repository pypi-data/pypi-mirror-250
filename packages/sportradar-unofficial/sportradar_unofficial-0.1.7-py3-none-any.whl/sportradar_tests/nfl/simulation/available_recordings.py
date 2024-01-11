import unittest
from unittest.mock import patch, Mock
import requests
from sportradar.simulation.available_recordings import AvailableRecordings
from sportradar.simulation.config import Config


class TestAvailableRecordings(unittest.TestCase):
    def setUp(self):
        self.rec = AvailableRecordings(Config.BASE_URL)

    def test_construct_query(self):
        query = self.rec.construct_query()
        self.assertIsInstance(query, str)  # checks if return value is string

    @patch("requests.post")
    def test_post_json_data(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "key": "value"
        }  # Making the mock response return a dictionary
        mock_post.return_value = mock_response.json()

        query = self.rec.construct_query()
        response = self.rec.post_json_data(query)

        # asserts POST call was made with exactly these arguments
        mock_post.assert_called_with(
            Config.BASE_URL,
            headers={"Content-Type": f"application/{Config.FORMAT}"},
            json={"query": query, "variables": {"league": "nfl"}},
        )

        # asserts the return value is the expected dictionary
        self.assertIsInstance(response, dict)

    @patch("requests.post")
    def test_post_json_data_error(self, mock_post):  # moved inside class
        # Simulate a RequestException during requests.post
        mock_post.side_effect = requests.exceptions.RequestException()

        query = self.rec.construct_query()
        response = self.rec.post_json_data(query)

        # asserts POST call was made with exactly these arguments
        mock_post.assert_called_with(
            Config.BASE_URL,
            headers={"Content-Type": f"application/{Config.FORMAT}"},
            json={"query": query, "variables": {"league": "nfl"}},
        )

        # asserts the return value is None if a RequestException happened
        self.assertIsNone(response)


if __name__ == "__main__":
    unittest.main()
