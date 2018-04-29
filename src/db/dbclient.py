import logging
import os
import pymongo
import feedparser


class MongoClient:
    url = "mongodb://{user}:{password}@ds263639.mlab.com:63639/trufflex"

    def __init__(self):
        password = os.environ.get('MONGO_PASS')
        user = os.environ.get('MONGO_USER')
        url = MongoClient.url.format(user=user, password=password)
        self.client = pymongo.MongoClient(url)
        self.db = self.client.get_database('trufflex')


class RssClient(MongoClient):

    def __init__(self):
        super().__init__()
        self.collection = self.db.get_collection('RSS')

class Feed:
    def __init__(self, url, feedname=None):
        self.url = url
        self.feedname = feedname or ""
        self.client = RssClient()

    def get_rss(self):
        try:
            return feedparser.parse(self.url)
        except Exception as e:
            logging.warning(f"Exception {e} calling feedparser on {self.url}")
            return {"entries": []}

    def get_new_entries(self):
        rss = self.get_rss()
        current_entries = self.client.collection.find({'feed_url': self.url})
        item_ids = [i['id'] for i in current_entries]

        for entry in rss['entries']:
            if entry['id'] not in item_ids:
                entry['feed_name'] = self.feedname
                entry['feed_url'] = self.url
                yield entry

    def update_db(self):
        c = 0
        for entry in self.get_new_entries():
            c += 1
            self.client.collection.insert_one(entry)

        print(f"Uploaded {c} new documents for {self.url} to db")