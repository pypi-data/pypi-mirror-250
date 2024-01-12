from dotenv import load_dotenv
import os
import unittest
from datetime import datetime
from sportradar.extract.gamefeeds import GameFeeds
from sportradar.workspace.datastore import save_data

load_dotenv("../../../.env")


class TestConstants:
    BASE_URL = "https://api.sportradar.us/nfl/official"
    ACCESS_LEVEL = "trial"
    VERSION = "v7"
    LANGUAGE_CODE = "en"
    FORMAT = "json"
    API_KEY = f'{os.environ.get("APIKEY")}'
    MONGODB_URL = f"{os.environ.get('MONGODB_URL')}"
    MONGODB_DATABASE = f"{os.environ.get('MONGODB_DATABASE')}"


class TestGameFeeds(unittest.TestCase):
    def setUp(self):
        self.game_feeds = GameFeeds(base_url=TestConstants.BASE_URL)
        self.game_id = "251ac0cf-d97d-4fe8-a39e-09fc4a95a0b2"
        self.expected_status = 200

    def test_get_game_boxscore(self):
        result = self.game_feeds.get_game_boxscore(
            access_level=TestConstants.ACCESS_LEVEL,
            language_code=TestConstants.LANGUAGE_CODE,
            version=TestConstants.VERSION,
            game_id=self.game_id,
            file_format=TestConstants.FORMAT,
            api_key=TestConstants.API_KEY,
        )
        if result.status_code == self.expected_status:
            save_data(
                response=result,
                db_uri=TestConstants.MONGODB_URL,
                database=TestConstants.MONGODB_DATABASE,
                collection=f'test_game_boxscore_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )
        assert (
            result.status_code == self.expected_status
        ), f"Expected status code {self.expected_status}, but got {result.status_code}."

    def test_get_game_roster(self):
        result = self.game_feeds.get_game_roster(
            access_level=TestConstants.ACCESS_LEVEL,
            language_code=TestConstants.LANGUAGE_CODE,
            version=TestConstants.VERSION,
            game_id=self.game_id,
            file_format=TestConstants.FORMAT,
            api_key=TestConstants.API_KEY,
        )
        if result.status_code == self.expected_status:
            save_data(
                response=result,
                db_uri=TestConstants.MONGODB_URL,
                database=TestConstants.MONGODB_DATABASE,
                collection=f'test_game_roster_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )
        assert (
            result.status_code == self.expected_status
        ), f"Expected status code {self.expected_status}, but got {result.status_code}."

    def test_get_game_statistics(self):
        result = self.game_feeds.get_game_statistics(
            access_level=TestConstants.ACCESS_LEVEL,
            language_code=TestConstants.LANGUAGE_CODE,
            version=TestConstants.VERSION,
            game_id=self.game_id,
            file_format=TestConstants.FORMAT,
            api_key=TestConstants.API_KEY,
        )
        if result.status_code == self.expected_status:
            save_data(
                response=result,
                db_uri=TestConstants.MONGODB_URL,
                database=TestConstants.MONGODB_DATABASE,
                collection=f'test_game_statistics_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )
        assert (
            result.status_code == self.expected_status
        ), f"Expected status code {self.expected_status}, but got {result.status_code}."

    def test_get_game_pbp(self):
        result = self.game_feeds.get_game_pbp(
            access_level=TestConstants.ACCESS_LEVEL,
            language_code=TestConstants.LANGUAGE_CODE,
            version=TestConstants.VERSION,
            game_id=self.game_id,
            file_format=TestConstants.FORMAT,
            api_key=TestConstants.API_KEY,
        )
        if result.status_code == self.expected_status:
            save_data(
                response=result,
                db_uri=TestConstants.MONGODB_URL,
                database=TestConstants.MONGODB_DATABASE,
                collection=f'test_game_pbp_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )
        assert (
            result.status_code == self.expected_status
        ), f"Expected status code {self.expected_status}, but got {result.status_code}."


if __name__ == "__main__":
    unittest.main(argv=[""], defaultTest="TestGameFeeds")
