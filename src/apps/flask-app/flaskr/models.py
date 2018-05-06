"""
The models.py module contains abstractions for grabbing information from db
to present within a view.

A view consumes a list of dictionaries; each of which either contains:

* lat/lon coordinates
* title
* text/images for each info window (styling will be handled elsewhere)

To avoid relying on places API whenever we want to get the location of a restaurant, lat/lon
should be stored in db.

We have have to this type of annotation as an ETL process.

See documentation for details on data models.
"""

