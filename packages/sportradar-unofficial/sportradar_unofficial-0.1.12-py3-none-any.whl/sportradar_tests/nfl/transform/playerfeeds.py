import os
import unittest
from dotenv import load_dotenv

from sportradar.transform.playerfeeds import PlayerFeedsTransformer

load_dotenv("../../../.env")


class TestConstants:
    MONGODB_URL = f"{os.environ.get('MONGODB_URL')}"
    MONGODB_DATABASE = f"{os.environ.get('MONGODB_DATABASE')}"


class TestPlayerFeedsTransformer(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.dummy_data = {
            "home_team": "Team A",
            "away_team": "Team B",
            "_comment": "10-5",
        }
        self.gft = PlayerFeedsTransformer(self.dummy_data)

    def test_transform_player_profile(self):
        # Act
        result = self.gft.transform_player_profile()

        # Assert
        self.assertIsInstance(result, dict)


if __name__ == "__main__":
    unittest.main(argv=[""], defaultTest="TestPlayerFeedsTransformer")
