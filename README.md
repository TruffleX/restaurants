# restaurants

## Setup
Get docker. Then:

```bash
make build
make run
```

## Commands:

* `make run`: Launch Environment
* `make jupyter`: Launch jupyter notebook in environment
* `make update`: Update DB with new RSS entries (from environment)
* `make app-dev`: Run the web app in dev mode.

## Tools

* etl/dbpedia.py: sparql client for grabbing dbpedia entries.
* etl/rss.py: executable script for updating mongo db with latest from known RSS feeds.
* db/dbclient: Client for interacting with mongo db

## Internal

* Trello: https://trello.com/b/0TjRZqR7/trufflex
* Mongo: https://mlab.com/databases/trufflex
* Slack: truffleX.slack.com
* github: https://github.com/TruffleX/restaurants
* google docs: https://drive.google.com/drive/folders/199qmYYjFKYldQxf5NUxysB2s9zC5WZnu

### dbpedia:
* list of prefixes: http://dbpedia.org/sparql?help=nsdecl
* online client: http://dbpedia.org/snorql
* great online editor: http://yasgui.org/
* https://query.wikidata.org/
* http://dbpedia.org/page/Hamburger
* http://vladimiralexiev.github.io/pubs/Tagarev2017-DomainSpecificGazetteer.pdf
* http://wiki.dbpedia.org/OnlineAccess

### RSS

* Within the container, run `python src/scripts/update_db.py` to collect new RSS entries and write them to db.
* To add a new RSS entry, update the `update_db.py` script (RSS_URLS) (**to do**: come up with a better way of doing this)


### Reviews
Will keep each dataset compressed on s3. I'm keeping them public for now. We'll coordinate on sharing AWS resources and make it private.
* [Yelp](https://s3-us-west-1.amazonaws.com/restaurant-review-data/yelp/yelp_dataset.tar). Run data/yelp/get_data.py to grab it..
