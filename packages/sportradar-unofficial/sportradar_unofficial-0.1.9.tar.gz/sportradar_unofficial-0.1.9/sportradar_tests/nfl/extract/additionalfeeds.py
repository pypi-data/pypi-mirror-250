from dotenv import load_dotenv
import os
import unittest
from datetime import datetime
from sportradar.extract.additionalfeeds import AdditionalFeeds
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


class TestAdditionalFeeds(unittest.TestCase):
    def setUp(self):
        self.additionalfeeds = AdditionalFeeds(base_url=TestConstants.BASE_URL)
        self.year = datetime.now().year - 6  # 2023
        self.month = datetime.now().month - 1
        self.day = datetime.now().day - 15
        self.nfl_season = (
            "PST"  # Preseason (PRE), Regular Season (REG), or Post-Season (PST).
        )
        self.nfl_season_week = (
            "02"  # The number of weeks into the season in 2 digit format (WW).
        )
        self.expected_status = 200

    def test_get_weekly_depth_charts(self):
        result = self.additionalfeeds.get_weekly_depth_charts(
            access_level=TestConstants.ACCESS_LEVEL,
            language_code=TestConstants.LANGUAGE_CODE,
            version=TestConstants.VERSION,
            year=self.year,
            nfl_season=self.nfl_season,
            nfl_season_week=self.nfl_season_week,
            file_format=TestConstants.FORMAT,
            api_key=TestConstants.API_KEY,
        )
        if result.status_code == self.expected_status:
            save_data(
                response=result,
                db_uri=TestConstants.MONGODB_URL,
                database=TestConstants.MONGODB_DATABASE,
                collection=f'test_get_weekly_depth_charts_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )
        assert (
            result.status_code == self.expected_status
        ), f"Expected status code {self.expected_status}, but got {result.status_code}."

    def test_get_daily_change_log(self):
        result = self.additionalfeeds.get_daily_change_log(
            access_level=TestConstants.ACCESS_LEVEL,
            language_code=TestConstants.LANGUAGE_CODE,
            version=TestConstants.VERSION,
            year=self.year,
            month=self.month,
            day=self.day,
            file_format=TestConstants.FORMAT,
            api_key=TestConstants.API_KEY,
        )
        if result.status_code == self.expected_status:
            save_data(
                response=result,
                db_uri=TestConstants.MONGODB_URL,
                database=TestConstants.MONGODB_DATABASE,
                collection=f'test_get_daily_change_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )
        assert (
            result.status_code == self.expected_status
        ), f"Expected status code {self.expected_status}, but got {result.status_code}."

    def test_get_daily_transactions(self):
        result = self.additionalfeeds.get_daily_transactions(
            access_level=TestConstants.ACCESS_LEVEL,
            language_code=TestConstants.LANGUAGE_CODE,
            version=TestConstants.VERSION,
            year=self.year,
            month=self.month,
            day=self.day,
            file_format=TestConstants.FORMAT,
            api_key=TestConstants.API_KEY,
        )
        if result.status_code == self.expected_status:
            save_data(
                response=result,
                db_uri=TestConstants.MONGODB_URL,
                database=TestConstants.MONGODB_DATABASE,
                collection=f'test_get_daily_transactions_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )
        assert (
            result.status_code == self.expected_status
        ), f"Expected status code {self.expected_status}, but got {result.status_code}."

    def test_get_league_hierarchy(self):
        result = self.additionalfeeds.get_league_hierarchy(
            access_level=TestConstants.ACCESS_LEVEL,
            language_code=TestConstants.LANGUAGE_CODE,
            version=TestConstants.VERSION,
            file_format=TestConstants.FORMAT,
            api_key=TestConstants.API_KEY,
        )
        if result.status_code == self.expected_status:
            save_data(
                response=result,
                db_uri=TestConstants.MONGODB_URL,
                database=TestConstants.MONGODB_DATABASE,
                collection=f'test_get_league_hierarchy_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )
        assert (
            result.status_code == self.expected_status
        ), f"Expected status code {self.expected_status}, but got {result.status_code}."

    def test_get_postgame_standings(self):
        result = self.additionalfeeds.get_postgame_standings(
            access_level=TestConstants.ACCESS_LEVEL,
            language_code=TestConstants.LANGUAGE_CODE,
            version=TestConstants.VERSION,
            year=self.year,
            nfl_season=self.nfl_season,
            file_format=TestConstants.FORMAT,
            api_key=TestConstants.API_KEY,
        )

        if result.status_code == self.expected_status:
            save_data(
                response=result,
                db_uri=TestConstants.MONGODB_URL,
                database=TestConstants.MONGODB_DATABASE,
                collection=f'test_get_postgame_standings_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )
        assert (
            result.status_code == self.expected_status
        ), f"Expected status code {self.expected_status}, but got {result.status_code}."

    def test_get_seasons(self):
        result = self.additionalfeeds.get_seasons(
            access_level=TestConstants.ACCESS_LEVEL,
            language_code=TestConstants.LANGUAGE_CODE,
            version=TestConstants.VERSION,
            file_format=TestConstants.FORMAT,
            api_key=TestConstants.API_KEY,
        )
        if result.status_code == self.expected_status:
            save_data(
                response=result,
                db_uri=TestConstants.MONGODB_URL,
                database=TestConstants.MONGODB_DATABASE,
                collection=f'test_seasons {datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )
        assert (
            result.status_code == self.expected_status
        ), f"Expected status code {self.expected_status}, but got {result.status_code}."

    def test_get_weekly_seasons(self):
        result = self.additionalfeeds.get_weekly_injuries(
            access_level=TestConstants.ACCESS_LEVEL,
            language_code=TestConstants.LANGUAGE_CODE,
            version=TestConstants.VERSION,
            year=self.year,
            nfl_season=self.nfl_season,
            nfl_season_week=self.nfl_season_week,
            file_format=TestConstants.FORMAT,
            api_key=TestConstants.API_KEY,
        )

        if result.status_code == self.expected_status:
            save_data(
                response=result,
                db_uri=TestConstants.MONGODB_URL,
                database=TestConstants.MONGODB_DATABASE,
                collection=f'test_get_weekly_injuries {datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )
        assert (
            result.status_code == self.expected_status
        ), f"Expected status code {self.expected_status}, but got {result.status_code}."


if __name__ == "__main__":
    unittest.main(argv=[""], defaultTest="TestAdditionalFeeds")
