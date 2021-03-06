"""
The models.py module contains abstractions for grabbing information from db
to present within a view.

A view consumes a list of dictionaries; each of which either contains:

* lat/lon coordinates
* title
* text/images for each info window (styling will be handled elsewhere)

To avoid relying on places API whenever we want to get the location of a restaurant, lat/lon
should be stored in db.

We have have to this type of annotation as an ETL process.

See documentation for details on data models.
"""


from db.dbclient import MongoClient

class Restaurants:
    def __init__(self, dao):
        self.dao = dao.db.get_collection('restaurant')

    def filter_by_coords(self, west=None, east=None, north=None, south=None):
        if any([i is None for i in [west, east, south, north]]):
            raise ValueError("Must pass in values for all coordinates")

        query = {
            'coords.lat': {'$lt': east, '$gt': west},
            'coords.lon': {'$gt': south, '$lt': north},
        }

        return self.dao.find(query)

    def get_all(self):
        return filter(self.is_5_star, filter(self.is_valid, self.dao.find({})))

    def is_valid(self, blob):
        coords = blob.get('coords')
        if coords is None:
            return False
        lat, lon = coords.get('lat'), coords.get('lon')
        if lat is None or lon is None:
            return False
        if not isinstance(lat, float) or not isinstance(lon, float):
            return False
        return True

    def is_5_star(self, review):
        yelp = review.get('yelp')
        if yelp is None:
            return False
        rating = yelp.get('rating')
        if rating is None:
            return False
        if rating < 4:
            return False
        return True

class Model:
    def __init__(self):
        self.DataAccessObject = MongoClient()
        self.restaurants = Restaurants(self.DataAccessObject)
