from db.dbclient import Feed

if __name__ == '__main__':
    RSS_URLS = [
        'https://www.cntraveler.com/feed/rss',
    ]
    for url in RSS_URLS:
        rssfeed = Feed(url)
        rssfeed.update_db()