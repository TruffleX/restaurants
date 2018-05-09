import logging
from itertools
import pymongo
from db.dbclient import MongoClient
from itertools import cycle
import requests


class Cycle(list):
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except IndexError:
            if isinstance(key, int):
                key = len(self) % key
                return super().__getitem__(key)

            else:
                raise TypeError(f"TypeError: list indices must be integers or slices, not {type(key)}")


class YelpClient:
    """
    So the yelp client lets you call the API 5000 times each day,
    and within each call youre limited to 50 results.

    Once we ingest a restaurant, we do not want it to show up in future
    searches, lest we waste a search.

    Ideally, we would have a date added field; that way we could start
    at the beginning of yelp, do a sweep to the current date, and just
    include new restaurants in our search.

    Another constraint is that search results can only be access up to the
    1000 mark.

    Therefore, in dense regions you want to narrow your search.

    We will optimize these things later.

    For now, we note that the in the densest zip code in the US,
    we get just < 1000 results if we include a radius of 1500 meters.

    Here will be the metaprocedure:

    - get previous


    """

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('YELP_API_KEY')
        self.request_headers = {'Authorization': f'Bearer {self.api_key}'}
        self.mongo_client = MongoClient(collection='ops').collection
        self.op_name = "yelp-restaurant-ingest"
        self.last_ingest = self.get_last_ingest()
        self.searches = []

        self.zip_ranges = {
            'LA': range(90001, 90510),
            'Boston': range(1907, 2305)
        }

        self.zip_queue = self.get_zip_queue()

    def get_zip_queue(self):
        zip_queue = zip(*list(self.zip_ranges.values()))
        return Cycle([zipcode for ziplist in zip_queue for zipcode in ziplist])

    def get_last_ingest(self):
        cursor = self.mongo_client.find({"op": self.op_name})
        try:
            return cursor.sort('date', direction=pymongo.DESCENDING).limit(1).next()
        except StopIteration:
            return {}

    def _search(self, url, params, callback=None):
        """
        Going to make this function very javascripty for no reason
        """
        response = requests.get(url, params=params, headers=self.headers)
        if response.status_code != 200:
            if callback:
                return callback(status_code, response.json())
        else:
            return response.json()

    def log(self, status_code, reason):
        logging.error(f"Got HTTP Error {status_code}: {reason}")

    def pick_next_zip(self):
        if len(self.searches) == 0:
            last_searches = self.last_ingest.get('searches')
            if last_searches is None:
                last_search = self.zip_queue[-1]
            else:
                last_search = last_searches[-1]
        else:
            last_search = self.seaches[-1]

        idx = self.zip_queue.index(last_search) + 1
        return self.zip_queue[idx]

    def get_restaurants(self):
        categories = "restaurants"
        limit = 50
        sort_by = 'distance'
        url = 'https://api.yelp.com/v3/businesses/search'
        self._search(url, params, self.log)
