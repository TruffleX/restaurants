import logging
from db.dbclient import Feed

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
        #"http://www.laweekly.com/index.rss"
    ]
    for url in RSS_URLS:
        rssfeed = Feed(url)
        rssfeed.update_db()