import unittest
from unittest.mock import patch
import requests
from sportradar.simulation.session import create_session
from sportradar.simulation.available_recordings import AvailableRecordings
from sportradar.simulation.config import Config


class TestCreateSession(unittest.TestCase):
    PLAYBACK_URL = Config.BASE_URL

    def setUp(self):
        self.rec = AvailableRecordings(self.PLAYBACK_URL)
        query = self.rec.construct_query()
        recordings = self.rec.post_json_data(query)
        self.recording_id = recordings.json()["data"]["recordings"][0]["id"]

    def _mock_response(self, mock_post, status_code=200):
        mock_response = requests.Response()
        mock_response.status_code = status_code
        mock_post.return_value = mock_response

    @patch("requests.post")
    def test_create_session(self, mock_post):
        self._mock_response(mock_post)
        response = create_session(url=self.PLAYBACK_URL, recording_id=self.recording_id)
        self.assertEqual(response.status_code, 200)

    @patch("requests.post")
    def test_create_session_exception(self, mock_post):
        mock_post.side_effect = requests.RequestException
        response = create_session(self.PLAYBACK_URL, self.recording_id)
        self.assertIsNone(response)


if __name__ == "__main__":
    unittest.main()
