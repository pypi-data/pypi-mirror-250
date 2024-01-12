import os
import unittest
from dotenv import load_dotenv

from sportradar.transform.teamfeeds import TeamFeedsTransformer

load_dotenv("../../../.env")


class TestConstants:
    MONGODB_URL = f"{os.environ.get('MONGODB_URL')}"
    MONGODB_DATABASE = f"{os.environ.get('MONGODB_DATABASE')}"


class TestTeamFeedsTransformer(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.dummy_data = {
            "home_team": "Team A",
            "away_team": "Team B",
            "_comment": "10-5",
        }
        self.gft = TeamFeedsTransformer(self.dummy_data)

    def test_transform_team_roster(self):
        # Act
        result = self.gft.transform_team_roster()

        # Assert
        self.assertIsInstance(result, dict)

    def test_transform_seasonal_statistics(self):
        # Act
        result = self.gft.transform_seasonal_statistics()

        # Assert
        self.assertIsInstance(result, dict)

    def test_transform_team_profile(self):
        # Act
        result = self.gft.transform_team_profile()

        # Assert
        self.assertIsInstance(result, dict)


if __name__ == "__main__":
    unittest.main(argv=[""], defaultTest="TestTeamFeedsTransformer")
