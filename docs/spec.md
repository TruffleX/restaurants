# TruffleX

## Goal

To build an AI food tour guide based on deep understanding of user preferences.

Make a product for ourselves, that we find useful.

## Use Case

I love food and my favorite part of traveling to a new city, or exploring a
familiar city, is discovering amazing food. Unfortunately, it's not always
easy to understand what the most exciting opportunities are for my specific
tastes. Guides can often be tarnished by hype, or compromise authenticity by
driving too much tourism. I would love to have an intelligent, dynamic, and
deeply understanding food guide highly refined to my palate and preferences.

I love annotated maps, itineraries, and tools that let me explore my surroundings (curated of course). I would
like my food guide to be aware of planning/logistics challenges.

## Open questions:

* People like restaurants for many reasons. How should a food guide take these into account?
    * It was new, exciting and interesting. Novelty. Different from my past experiences.
    * It was delicious. Food preference matching.
    * It was comforting, familiar, sentimental. The food/restaurant has ties to my culture, family, childhood, etc.
    * It was easy, convenient, en route to a common destination, fast.
    * It was conducive to positive social interactions, perhaps for friends, for a date, for out of town guests, business, etc...
    * It was impressive, the caliber/craft of the food, the design of the restaurant, the quality of the service.

* Are all reviews useful to me as an individual, or are some just noise, or worse, misleading?


## Data Sources

* Yelp
* Wikipedia for semantic analysis
* Food magazines in each city (start with LA and Boston)
* Newspapers in each city if not behind paywall
* Serious Eats to help populate the global space of food
    * I found a Kaggle dataset for this as well.
* All Recipes for ingredient coocurrance

## Ideas

* Embed users in ingredient space
* Embed restaurants in ingredient/cuisine space.
* Bayesian reranking of recommendations based on features like environmental.
preferences, preferred times, locations, etc.
* Semantically tag restaurants via wiki as a pseudo-knowledge base.
* Embed user/restaurant ratings into a lower dimensional preference space.
* Collect restaurant reviews via multiple RSS feeds. If we can create a decent review sentiment model, we
create an artificial rating for the review even if the reviewer didnt explicitely give a rating. These ratings can be used to establish preferences.
If both users and reviewers can be mapped to a preference space, then we can learn to match users with the most relevant feedback.