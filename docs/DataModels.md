This document is meant to describe the details of what data we store, how we store it, how its updated, how its accessed by the app.



# FrontEnd

## Data Model

### returned by model

Below is an example of what might get returned by the data model for a restaurant:

```code:python
{
    'id': 'di03u2jrlkej',
    'name': "Bob's Pizza",
    'coords': {
        "lat": 24, "lon":-34
    },
    'address': "123 baker st",
    'city': "Los Angeles",
    'state': "CA",
    'html_content': "Jonathan gold gave this place a great review on Oct 2 2017, see latimes.com/reviews/ipaosipio.html for details. <img src='s3.amazonaws.com/bobs.png'> <button for discard>"
}
```

Below are the underlying mongo data sources that be queried and composed into the final json document sent to the template:

```code:python
restaurant = {
    'id': 'di03u2jrlkej',
    'name': "Bob's Pizza",
    'coords': {
        "lat": 24, "lon":-34
    },
    'address': "123 baker st",
    'city': "Los Angeles",
    'state': "CA",
}

reviews = [
    {"restaurant_id": 'di03u2jrlkej', 'content': "loved it", "ML_Rating": 5, 'source_id': '9043jio2', "review_id": "reo3020ir", "inserted_at": "jan 1 2018", "reviewed_at": "Oct 2 2017"}
]

awards = [
    {"restaurant_id": 'di03u2jrlkej', 'title': "James Beard", 'source_id': '9043jio2', "inserted_at": "jan 1 2018", "granted_at": "Oct 2 2017", "for_period": "2018", 'status': 'nominated'}
]

images = [
    {'restaurant_id': 'di03u2jrlkej', 'url': 's3.amazonaws.com/bobs.png', 'title': "Front door"}
]
```