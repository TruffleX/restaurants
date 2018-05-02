import logging
import os
import pymongo
import feedparser


class MongoClient:
    url = "mongodb://{user}:{password}@ds263639.mlab.com:63639/trufflex"

    def __init__(self, collection=None):
        password = os.environ.get('MONGO_PASS')
        user = os.environ.get('MONGO_USER')
        url = MongoClient.url.format(user=user, password=password)
        self.client = pymongo.MongoClient(url)
        self.db = self.client.get_database('trufflex')
        if collection is not None:
            self.collection = self.db.get_collection(collection)

    @staticmethod
    def fromCollection(collection):
        return MongoClient(collection)


class RssClient(MongoClient):

    def __init__(self):
        super().__init__("RSS")

class KnowledgeClient(MongoClient):

    def __init__(self):
        super().__init__("knowledge")
