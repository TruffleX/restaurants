# restaurants

## Setup
Get docker. Note that our container current exposes port 8889, so if youre going to use jupyter stuff use that port.

```bash
make build
make run
```


## Commands:

* `make run`: Launch Environment
* `make jupyter`: Launch jupyter notebook in environment
* `make update`: Update DB with new RSS entries (from environment)

## Data
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
