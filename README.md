# restaurants

### Setup
Get docker. Note that our container current exposes port 8889, so if youre going to use jupyter stuff use that port.

```bash
cd env 
make build
make run
```

### Data
Will keep each dataset compressed on s3. I'm keeping them public for now. We'll coordinate on sharing AWS resources and make it private.
* [Yelp](https://s3-us-west-1.amazonaws.com/restaurant-review-data/yelp/yelp_dataset.tar). Run data/yelp/get_data.py to grab it..
