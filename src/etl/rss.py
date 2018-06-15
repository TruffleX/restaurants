import logging
from db.dbclient import MongoClient
import feedparser
from bs4 import BeautifulSoup
import requests as req
from pymongo import ReplaceOne
from tqdm import tqdm
from ml.review_model import ReviewModel

class Feed:
    # type, attr, value
    meta_keywords = [
        ('meta_keywords','name','news_keywords'),
        ('meta_title', 'property',"og:title"),
        ('meta_description','property', "og:description"),
        ('meta_twitter_title','name','twitter:text:title')
    ]

    def __init__(self, url=None, feedname=None):
        self.url = url
        self.feedname = feedname or ""
        self.client = MongoClient("RSS")
        self.article_client = MongoClient("articles")
        self.review_model = None

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
        rss_count = 0
        doc_count = 0

        for entry in self.get_new_entries():
            rss_count += 1
            self.client.collection.insert_one(entry)
        logging.info(f"Uploaded {rss_count} new documents for {self.url} to db.RSS")

    def rss_to_articles(self):
        rss_entries = list(self.client.collection.find({}))
        already_processed_ids = list(self.article_client.collection.find({}, projection=['rss_id']))
        already_processed_ids = [str(i['rss_id']) for i in already_processed_ids]
        count = 0
        ops = []
        logging.info("Beginning Article Extraction...")
        for i, entry in tqdm(enumerate(rss_entries)):
            if str(entry['_id']) not in already_processed_ids:
                try:
                    data = self.parse(entry)
                    if data:
                        ops.append(ReplaceOne({'rss_id': data['rss_id']}, data, upsert=True))
                        count += 1
                except Exception as e:
                    logging.error(f"Exception caught parsing/uploading article:\n{e}")
            else:
                logging.info("Skipping, already in db")
                #pass

        if ops:
            self.article_client.collection.bulk_write(ops)

        logging.info(f"Backfilled {count} old documents for {self.url} to db.RSS, missed {i+1 - count}")

    def score_articles(self):
        """
        grabs each article, feeds it through the is_review model, annotates the document with a score.
        :return:
        """

        self.review_model = ReviewModel()
        self.review_model.load()

        articles_entries = list(self.article_client.collection.find({}))
        count = 0
        ops = []
        logging.info("Annotating Articles with Review Scores...")
        for i, entry in tqdm(enumerate(articles_entries)):
            try:
                score = self.review_model.predict(entry)
                entry['is_review_score'] = score
                ops.append(ReplaceOne({'_id': entry['_id']}, entry, upsert=True))
                count += 1
            except Exception as e:
                logging.error(f"Exception caught assigning review score to article:\n{e}")
        if ops:
            self.article_client.collection.bulk_write(ops)
        logging.info(f"Assigned {count} review scores to db.articles, missed {i+1 - count}")


    def parse(self, entry):
        link = entry.get('link')
        ID = str(entry.get('_id'))
        if link:
            resp = req.get(link)
            if resp.status_code == 200 and hasattr(resp, 'content'):
                raw_content = resp.content
                soup = BeautifulSoup(raw_content, "lxml")
                soup = self.clean_soup(soup)
                data = self.extract(soup)
                data['link'] = link
                data['rss_id'] = ID
                return data

    @staticmethod
    def clean_soup(soup, remove_scripts=True, remove_style=True, remove_meta=False):
        if remove_scripts:
            for script in soup('script'):
                script.extract()

        if remove_style:
            for script in soup('style'):
                script.extract()

        if remove_meta:
            for script in soup('meta'):
                script.extract()

        return soup

    def extract(self, soup):
        title_html = soup.find('title')
        title = title_html.text if title_html else None
        meta = self.extract_metadata(soup)
        content = self.extract_content(soup)
        return {
            'title': title,
            **content,
            **meta
        }

    def extract_content(self, soup):
        return {'content': " ".join([i.text for i in soup('p')])}

    def extract_metadata(self, soup):
        vals = {}
        for meta in soup('meta'):
            for name, attr, value in self.meta_keywords:
                found = meta.attrs.get(attr)
                if found == value:
                    vals[name] = meta.attrs.get('content')
        return vals


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
        "http://www.laweekly.com/index.rss",
        "https://www.finedininglovers.com/rss/all/latest",
        "https://therestaurantexpert.com/feed/",
        "https://www.theinfatuation.com/feed/atom",
    ]
    for url in RSS_URLS:
        rssfeed = Feed(url)
        rssfeed.update_db()
    rssfeed = Feed()
    rssfeed.rss_to_articles()
    rssfeed.score_articles()
