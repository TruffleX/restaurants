"""
Code that goes along with the Airflow tutorial located at:
https://github.com/airbnb/airflow/blob/master/airflow/example_dags/tutorial.py
"""

from etl.yelp import YelpClient

if __name__ == '__main__':
    YelpClient.get_restaurants(notebook=False, max_zips=5)