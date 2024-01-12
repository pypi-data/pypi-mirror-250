import os
from dotenv import load_dotenv
import unittest
from datetime import datetime
from sportradar.extract.primaryfeeds import PrimaryFeeds
from sportradar.workspace.datastore import save_data

load_dotenv("../../../../.env")


class TestConstants:
    BASE_URL = "https://api.sportradar.us/nfl/official"
    ACCESS_LEVEL = "trial"
    VERSION = "v7"
    LANGUAGE_CODE = "en"
    FORMAT = "json"
    API_KEY = f'{os.environ.get("APIKEY")}'
    MONGODB_URL = f"{os.environ.get('MONGODB_URL')}"
    MONGODB_DATABASE = f"{os.environ.get('MONGODB_DATABASE')}"


class TestPrimaryFeeds(unittest.TestCase):
    def setUp(self):
        self.primary_feeds = PrimaryFeeds(base_url=TestConstants.BASE_URL)
        self.year = range(2017, 2024)
        self.season_type = ["REG", "PST"]
        self.expected_status = 200
        self.week_number = datetime.now().isocalendar()[1] - 34

    def test_get_current_season_schedule(self):
        result = self.primary_feeds.get_current_season_schedule(
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
                collection=f'test_current_season_schedule_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )

        assert (
            result.status_code == self.expected_status
        ), f"Expected Status code {self.expected_status}, but got {result.status_code}."

    def test_get_current_week_schedule(self):
        result = self.primary_feeds.get_current_week_schedule(
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
                collection=f'test_current_week_schedule_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )

        assert (
            result.status_code == self.expected_status
        ), f"Expected Status code {self.expected_status}, but got{result.status_code}."

    def test_get_season_schedule(self):
        for year_ in self.year:
            for season in self.season_type:
                result = self.primary_feeds.get_seasons_schedule(
                    access_level=TestConstants.ACCESS_LEVEL,
                    language_code=TestConstants.LANGUAGE_CODE,
                    version=TestConstants.VERSION,
                    year=year_,
                    season_type=season,
                    file_format=TestConstants.FORMAT,
                    api_key=TestConstants.API_KEY,
                )

                if result.status_code == self.expected_status:
                    save_data(
                        response=result,
                        db_uri=TestConstants.MONGODB_URL,
                        database=TestConstants.MONGODB_DATABASE,
                        collection=f'test_season_schedule_{year_}_{season}_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                    )

    def test_get_week_schedule(self):
        result = self.primary_feeds.get_weekly_schedule(
            access_level=TestConstants.ACCESS_LEVEL,
            language_code=TestConstants.LANGUAGE_CODE,
            version=TestConstants.VERSION,
            season_year=self.year[-1],
            season_type=self.season_type[0],
            week_number=self.week_number,
            file_format=TestConstants.FORMAT,
            api_key=TestConstants.API_KEY,
        )

        if result.status_code == self.expected_status:
            save_data(
                response=result,
                db_uri=TestConstants.MONGODB_URL,
                database=TestConstants.MONGODB_DATABASE,
                collection=f'test_weekly_schedule_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            )


if __name__ == "__main__":
    unittest.main(argv=[""], defaultTest="TestPrimaryFeeds")
