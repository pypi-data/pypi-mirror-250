from dotenv import load_dotenv
import os
import unittest
from datetime import datetime
from sportradar.extract.playerfeeds import PlayerFeeds
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


class TestPlayerFeeds(unittest.TestCase):
    def setUp(self):
        self.player_feeds = PlayerFeeds(base_url=TestConstants.BASE_URL)
        self.player_id = "16423bd0-6239-454c-9ec8-f90477de17b1"
        self.expected_status = 200

    def test_get_player_profile(self):
        result = self.player_feeds.get_player_profile(
            access_level=TestConstants.ACCESS_LEVEL,
            language_code=TestConstants.LANGUAGE_CODE,
            version=TestConstants.VERSION,
            player_id=self.player_id,
            file_format=TestConstants.FORMAT,
            api_key=TestConstants.API_KEY,
        )
        if result.status_code == self.expected_status:
            save_data(
                response=result,
                db_uri=TestConstants.MONGODB_URL,
                database=TestConstants.MONGODB_DATABASE,
                collection=f'test_player_profile_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )
        assert (
            result.status_code == self.expected_status
        ), f"Expected status code {self.expected_status}, but got {result.status_code}."


if __name__ == "__main__":
    unittest.main(argv=[""], defaultTest="TestPlayerFeeds")
