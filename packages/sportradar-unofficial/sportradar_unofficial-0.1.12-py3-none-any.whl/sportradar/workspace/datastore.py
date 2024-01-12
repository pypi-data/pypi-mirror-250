from urllib3.util.retry import Retry
from pydantic import HttpUrl
from requests.adapters import HTTPAdapter
import requests
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from sportradar import logging_helpers

logger = logging_helpers.get_logger(__name__)
SERVER_API = "1"
PORT = 27017

def setup_http_session():
    """

    This function sets up an HTTP session with retries and mounts an adapter for handling HTTP requests.

    Returns:
        session (requests.Session): The initialized HTTP session.

    """
    retries = Retry(
        total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def get_data_from_mongodb(db_uri, database, collection: str):
    """
    Args:
        db_uri: The URI of the MongoDB server.
        database: The name of the database to connect to.
        collection: The name of the collection to fetch data from.

    Returns:
        The response from the fetch operation.

    Raises:
        Exception: If there is an error while getting data from the MongoDB server.

    """
    try:
        response = fetch_from_database(db_uri, database, collection)
        return response
    except Exception as e:
        logger.error(f"Error getting data from MONGODB_DATABASE: {e}")


def fetch_from_database(db_uri, database, collection):
    """
    Fetches data from a MongoDB collection.

    Args:
        db_uri (str): The URI for connecting to the MongoDB server.
        database (str): The name of the database to fetch data from.
        collection (str): The name of the collection to fetch data from.

    Returns:
        cursor: A cursor object containing the fetched data.

    Raises:
        ValueError: If the database environment variable is not set.

    """
    mongo_client = MongoClient(host=db_uri, server_api=ServerApi(SERVER_API), port=PORT)
    if database is None:
        raise ValueError("MongoDB environment variable not set.")
    else:
        db = mongo_client[database]
        return list(db[collection].find())


def save_data(response, db_uri, database, collection):
    """
    Save data to MongoDB collection.

    Parameters:
    - response (object): The response object containing the data to be saved.
    - db_uri (str): The MongoDB connection URI.
    - database (str): The name of the database in which to save the data.
    - collection (str): The name of the collection in which to save the data.

    Raises:
    - ValueError: If the database name is None.

    """
    mongo_client = MongoClient(host=db_uri, server_api=ServerApi("1"), port=27017)
    if database is None:
        raise ValueError("MongoDB environment variable not set.")
    else:
        db = mongo_client[database]
        db[collection].insert_one(response.json())
        print("Saved data to MongoDB.")


class SportRadarFetcher:
    """
    Class to fetch data from SportRadar API.

    Attributes:
    - timeout (float): The timeout value for HTTP requests in seconds.
    - http (Session): The HTTP session object for making requests.
    - mongo_client (MongoClient): The MongoDB client object for connecting to the database.
    - mongo_db (str): The name of the MongoDB database.

    Methods:
    - __init__.py(timeout: float = 30): Initializes the SportRadarFetcher instance.
    - _fetch_from_url(url: HttpUrl) -> requests.Response: Fetches data from the given URL.
    - fetch_data(url: HttpUrl) -> requests.Response: Fetches data from the SportRadar API.

    """

    def __init__(self, timeout: float = 30):
        self.timeout = timeout
        self.http = setup_http_session()

    def _fetch_from_url(self, url: HttpUrl) -> requests.Response:
        logger.info(f"Retrieving {url} from SportsRadar")
        response = self.http.get(url, timeout=self.timeout)
        if response.status_code == requests.codes.ok:
            logger.debug(f"Successfully downloaded from {url}")
            return response
        raise ValueError(f"Could not download from {url}: {response.text}")

    def fetch_data(self, url: HttpUrl) -> requests.Response:
        try:
            return self._fetch_from_url(url)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            raise


class DataStore:
    """
    Class for storing and retrieving data using a specified fetcher.

    Parameters:
    - fetcher (SportRadarFetcher): The fetcher object used to retrieve data.

    Attributes:
    - fetcher (SportsRadarFetcher): The fetcher object used to retrieve data.
    - data (dict): A dictionary to store the fetched data.

    Methods:
    - fetch_data(url): Fetches data from the specified URL using the fetcher object. Returns the response if the request is successful.
    - get_data_from_database(collection): Retrieves data from the specified collection in the database. Returns a list of dictionaries.
    """

    def __init__(self, fetcher: SportRadarFetcher):
        self.fetcher = fetcher
        self.data = {}

    def fetch_data(self, url):
        try:
            response = self.fetcher.fetch_data(url)
            if response.status_code == requests.codes.ok:
                self.data.update({url: response.json()})
                return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            raise
