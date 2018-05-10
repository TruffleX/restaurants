"""
Code that goes along with the Airflow tutorial located at:
https://github.com/airbnb/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from etl.yelp import YelpClient

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 5, 9),
    'email': ['aikramer2@gmail.com', 'jake.e.neely@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('yelp-restaurant-ingest',
          default_args=default_args,
          schedule_interval=timedelta(1))

task1 = PythonOperator(
    python_callable=YelpClient.get_restaurants,
    task_id='ingest-restaurants',
    op_kwargs={'max_zips': 5},
    dag=dag,
)