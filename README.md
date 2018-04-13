# restaurants

### Setup
Get docker.

```bash
cd env 
make build
make run
```

### Data
Will keep each dataset compressed on s3. I'm keeping them public for now. We'll coordinate on sharing AWS resources and make it private.
* [Yelp](https://s3-us-west-1.amazonaws.com/restaurant-review-data/yelp/yelp_dataset.tar). Run data/yelp/get_data.py to grab it **incomplete**.
