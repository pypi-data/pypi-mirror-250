import os
import unittest
from dotenv import load_dotenv

from sportradar.transform.gamefeeds import GameFeedsTransformer

load_dotenv("../../../.env")


class TestConstants:
    MONGODB_URL = f"{os.environ.get('MONGODB_URL')}"
    MONGODB_DATABASE = f"{os.environ.get('MONGODB_DATABASE')}"


class TestGameFeedsTransformer(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.dummy_data = {
            "home_team": "Team A",
            "away_team": "Team B",
            "_comment": "10-5",
        }
        self.gft = GameFeedsTransformer(self.dummy_data)

    def test_transform_boxscore(self):
        # Act
        result = self.gft.transform_boxscore()
        print(result)

        # Assert
        self.assertIsInstance(result, dict)

    def test_transform_game_roster(self):
        # Act
        result = self.gft.transform_game_roster()

        # Assert
        self.assertIsInstance(result, dict)

    def test_transform_game_stats(self):
        # Act
        result = self.gft.transform_game_statistics()

        # Assert
        self.assertIsInstance(result, dict)


if __name__ == "__main__":
    unittest.main(argv=[""], defaultTest="TestGameFeedsTransformer")
