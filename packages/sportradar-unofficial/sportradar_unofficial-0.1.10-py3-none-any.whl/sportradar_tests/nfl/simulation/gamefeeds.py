import unittest
from unittest.mock import patch
from sportradar.simulation.session import create_session
from sportradar.simulation import gamefeeds
from sportradar.simulation.config import Config


def _mock_get_response(mock_get, response_dict):
    mock_get.return_value = unittest.mock.MagicMock(status_code=200)
    mock_get.json.return_value = response_dict


class TestGameFeeds(unittest.TestCase):
    PLAYBACK_URL = Config.BASE_URL

    def setUp(self):
        game_feed = gamefeeds.GameFeeds()
        self.recording_id = game_feed.get_available_recordings()
        self.session_id = create_session(
            url=self.PLAYBACK_URL, recording_id=self.recording_id
        )

    def _create_and_assert_test(self, mock_get, gamefeed_func, response_content):
        _mock_get_response(mock_get, response_content)
        gamefeed_func(self.recording_id, self.session_id)

    @patch("requests.get")
    def test_get_game_boxscore(self, mock_get):
        self._create_and_assert_test(
            mock_get,
            gamefeed_func=gamefeeds.get_game_boxscore,
            response_content={"data": "TestBoxScore"},
        )

    @patch("requests.get")
    def test_get_game_info(self, mock_get):
        self._create_and_assert_test(
            mock_get,
            gamefeed_func=gamefeeds.get_game_info,
            response_content={"data": "TestGameInfo"},
        )

    @patch("requests.get")
    def test_get_game_roster(self, mock_get):
        self._create_and_assert_test(
            mock_get,
            gamefeed_func=gamefeeds.get_game_roster,
            response_content={"data": "TestGameRoster"},
        )


if __name__ == "__main__":
    unittest.main()
