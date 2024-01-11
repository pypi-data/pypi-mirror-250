import os
import unittest
from dotenv import load_dotenv

from sportradar.transform.primaryfeeds import PrimaryFeedsTransformer

load_dotenv("../../.env")


class TestConstants:
    MONGODB_URL = f"{os.environ.get('MONGODB_URL')}"
    MONGODB_DATABASE = f"{os.environ.get('MONGODB_DATABASE')}"


class TestPrimaryFeedsTransformer(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.dummy_data = {
            "home_team": "Team A",
            "away_team": "Team B",
            "_comment": "10-5",
        }

        self.gft = PrimaryFeedsTransformer(self.dummy_data)

    def test_transform_current_season_schedule(self):
        # Act
        result = self.gft.transform_current_season_schedule()
        print(result)

        # Assert
        self.assertIsInstance(result, dict)

    def test_transform_current_week_schedule(self):
        # Act
        result = self.gft.transform_current_week_schedule()
        print(result)

        # Assert
        self.assertIsInstance(result, dict)

    def test_transform_seasons_schedule(self):
        # Act
        result = self.gft.transform_seasons_schedule()
        print(result)

        # Assert
        self.assertIsInstance(result, dict)

    def test_transform_weekly_schedule(self):
        # Act
        result = self.gft.transform_weekly_schedule()
        print(result)

        # Assert
        self.assertIsInstance(result, dict)


if __name__ == "__main__":
    unittest.main(argv=[""], defaultTest="TestPrimaryFeedsTransformer")
