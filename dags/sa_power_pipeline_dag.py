"""Airflow DAG for sa-power-pipeline.

Runs the existing extract-then-load pipeline as a single task,
once daily.This is the first orchestration pass - no retries or
alerting yet, that's a later iteration.
"""

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from sa_power_pipeline.run_pipeline import run as run_pipeline

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

    run_pipeline_task = PythonOperator(
        task_id="run_pipeline",
        python_callable=run_pipeline,
    )