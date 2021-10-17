from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'AlexSkp',
    'start_date': datetime(2014, 4, 1),
    'end_date': datetime(2014, 5, 31),
    'retries': 3,
    'retry_delay': timedelta(seconds=5),
    'email_on_retry': False,
    'Catchup': True,
    'depends_on_past': False
    
}

dag = DAG('uber_restaurant_trips_dag',
          default_args=default_args,
          description='loading data and restaurant data into redshift',
          schedule_interval='@daily',
          max_active_runs=1
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_trips_to_redshift = StageToRedshiftOperator(
    task_id='Stage_trips',
    dag=dag,
    redshift_conn_id="redshift",
    aws_conn_id="aws_credentials",
    table="staging_trips",
    s3_bucket="s3://alexskp-capstone/bucket_data/uber-data/{execution_date.year}/{execution_date.month}/{execution_date.day}",
    region="us-west-2",
    extra_params="""
        csv
        IGNOREHEADER 1
        TIMEFORMAT 'auto'
    """
)

stage_restaurants_to_redshift = StageToRedshiftOperator(
    task_id='Stage_restaurants',
    dag=dag,
    redshift_conn_id="redshift",
    aws_conn_id="aws_credentials",
    table="staging_restaurants",
    s3_bucket="s3://alexskp-capstone/bucket_data/restaurant-data/",
    region="us-west-2",
    extra_params="""
        json 's3://alexskp-capstone/bucket_data/NYrestaurants-jsonpath.json'
    """
)

load_quadrants_table_to_redshift = StageToRedshiftOperator(
    task_id='load_quadrants',
    dag=dag,
    redshift_conn_id="redshift",
    aws_conn_id="aws_credentials",
    table="quadrant_table",
    s3_bucket="s3://alexskp-capstone/bucket_data/quadrant_table.csv",
    region="us-west-2",
    extra_params="""
        csv
        IGNOREHEADER 1
    """
)

run_staging_quality_checks = DataQualityOperator(
    task_id='Run_staging_quality_checks',
    dag=dag,
    redshift_conn_id="redshift",
    tests = [
        {'test': "SELECT COUNT (*) FROM staging_trips WHERE datetime IS NULL", 'exp_result': 0},
        {'test': "SELECT COUNT (*) FROM staging_restaurants WHERE id IS NULL", 'exp_result': 0},
        {'test': "SELECT COUNT (*) FROM quadrant_table WHERE quadrant_id IS NULL", 'exp_result': 0}
    ]
)

load_address_dimension_table = LoadDimensionOperator(
    task_id='Load_address_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    query=SqlQueries.address_table_insert,
    final_table='address_table',
    columns='(address1, address2, address3, city, zip_code, country, state)',
    truncate=True
)

load_restaurant_dimension_table = LoadDimensionOperator(
    task_id='Load_restaurant_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    query=SqlQueries.restaurant_table_insert,
    final_table='restaurant_table',
    truncate=True
)

load_pickup_dimension_table = LoadDimensionOperator(
    task_id='Load_pickup_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    query=SqlQueries.pickup_table_insert,
    final_table='pickup_table',
    truncate=True
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    query=SqlQueries.time_table_insert,
    final_table='time_table',
    truncate=True
)

run_load_quality_checks = DataQualityOperator(
    task_id='Run_load_quality_checks',
    dag=dag,
    redshift_conn_id="redshift",
    tests = [
        {'test': "SELECT COUNT (*) FROM address_table WHERE address1 IS NULL", 'exp_result': 0},
        {'test': "SELECT COUNT (*) FROM restaurant_table WHERE restaurant_id IS NULL", 'exp_result': 0},
        {'test': "SELECT COUNT (*) FROM pickup_table WHERE datetime IS NULL", 'exp_result': 0},
        {'test': "SELECT COUNT (*) FROM time_table WHERE datetime IS NULL", 'exp_result': 0}
    ]
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

# ------------------- DAG EXECUTION ------------------- #

start_operator >> stage_trips_to_redshift
start_operator >> stage_restaurants_to_redshift
start_operator >> load_quadrants_table_to_redshift

stage_trips_to_redshift >> run_staging_quality_checks
stage_restaurants_to_redshift >> run_staging_quality_checks
load_quadrants_table_to_redshift >> run_staging_quality_checks

run_staging_quality_checks >> load_address_dimension_table
load_address_dimension_table >> load_restaurant_dimension_table
run_staging_quality_checks >> load_restaurant_dimension_table
run_staging_quality_checks >> load_pickup_dimension_table
run_staging_quality_checks >> load_time_dimension_table

load_address_dimension_table >> run_load_quality_checks
load_restaurant_dimension_table >> run_load_quality_checks
load_pickup_dimension_table >> run_load_quality_checks
load_time_dimension_table >> run_load_quality_checks

run_load_quality_checks >> end_operator
