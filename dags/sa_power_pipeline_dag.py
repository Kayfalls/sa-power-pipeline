"""Airflow DAG for sa-power-pipeline.

Extract and load run as separate tasks. Each retries on transient
failures, and failure callback logs a clear alert message when
retries are exhausted - the first step towards real alerting
(email/slack) in a later iteration.
"""

import logging
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from sa_power_pipeline.fetch_status import main as extract_task
from sa_power_pipeline.load_bigquery import load_all_raw_files as load_task

logger = logging.getLogger(__name__)


def alert_on_failure(context):
    """Log a clear alert when a task exhausts its retries and fails.

    This is intentionally simple - a log line, not an external notification.
    Wiring this to email/slack is a later iteration once we have a channel 
    to send it to.
    """
    task_id = context["task_instance"].task_id
    dag_id = context["dag"].dag_id
    execution_date = context["execution_date"]
    logger.error(
        "Alert: Task '%s' in DAG '%s' failed after all retries. Run: %s ",
        task_id, dag_id, execution_date
    )

default_args = {
    "owner": "kabelo",
    "start_date": datetime(2026, 9, 1),
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
    "on_failure_callback": alert_on_failure,
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