import os
import unittest
from dotenv import load_dotenv
from sportradar.transform.draftfeeds import DraftFeedsTransformer


load_dotenv("../../../.env")


class TestConstants:
    MONGODB_URL = f"{os.environ.get('MONGODB_URL')}"
    MONGODB_DATABASE = f"{os.environ.get('MONGODB_DATABASE')}"


class TestDraftFeedsTransformer(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.dummy_data = {
            "home_team": "Team A",
            "away_team": "Team B",
            "_comment": "10-5",
        }
        self.gft = DraftFeedsTransformer(self.dummy_data)

    def test_transform_draft_summary(self):
        # Act
        result = self.gft.transform_draft_summary()

        # Assert
        self.assertIsInstance(result, dict)

    def test_transform_prospects(self):
        # Act
        result = self.gft.transform_prospects()

        # Assert
        self.assertIsInstance(result, dict)

    def test_transform_team_draft_summary(self):
        # Act
        result = self.gft.transform_team_draft_summary()

        # Assert
        self.assertIsInstance(result, dict)

    def test_transform_top_prospects(self):
        # Act
        result = self.gft.transform_top_prospects()

        # assert
        self.assertIsInstance(result, dict)

    def test_transform_trades(self):
        # Act
        result = self.gft.transform_trades()

        # assert
        self.assertIsInstance(result, dict)


if __name__ == "__main__":
    unittest.main(argv=[""], defaultTest="TestDraftFeedsTransformer")
