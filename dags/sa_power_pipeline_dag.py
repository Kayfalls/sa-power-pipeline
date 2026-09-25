"""Airflow DAG for sa-power-pipeline.

Splits extract and load into separate tasks so failures are 
visible and retryable independently  - a BigQuery hiccup shouldn't
force a re-run of the API extraction (and its quota cost).
"""

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from sa_power_pipeline.fetch_status import main as extract_task
from sa_power_pipeline.load_bigquery import load_all_raw_files as load_task

default_args = {
    "owner": "kabelo",
    "start_date": datetime(2026, 9, 1),
}

with DAG(
    dag_id="sa_power_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    tags=["sa-power-pipeline"],
) as dag:

    extract = PythonOperator(
        task_id="extract_from_eskomsepush",
        python_callable=extract_task,
    )

    load = PythonOperator(
        task_id="load_to_bigquery",
        python_callable=load_task,
    )

    extract >> load