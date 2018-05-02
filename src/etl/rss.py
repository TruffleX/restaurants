import logging
from db.dbclient import RssClient
import feedparser

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
        item_ids = [i['link'] for i in current_entries]

        for entry in rss['entries']:
            if entry['link'] not in item_ids:
                entry['feed_name'] = self.feedname
                entry['feed_url'] = self.url
                yield entry

    def update_db(self):
        c = 0
        for entry in self.get_new_entries():
            c += 1
            self.client.collection.insert_one(entry)

        print(f"Uploaded {c} new documents for {self.url} to db")

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    RSS_URLS = [
        'https://www.cntraveler.com/feed/rss',
        'http://www.latimes.com/food/rss2.0.xml',
        'https://www.dailynews.com/things-to-do/restaurant-reviews-food/feed/',
        'https://www.kcrw.com/news-culture/shows/good-food-on-the-road/rss.xml',
        'http://www.lamag.com/culturefiles/feed/',
        'https://www.timeout.com/los-angeles/blog/feed.rss'
        "http://www.laweekly.com/index.rss"
    ]
    for url in RSS_URLS:
        rssfeed = Feed(url)
        rssfeed.update_db()