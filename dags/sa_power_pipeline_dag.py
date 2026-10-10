"""Airflow DAG for sa-power-pipeline.

Four tasks in sequence: extract from EskomSePush, load raw JSON
into BigQuery, run dbt models, then run dbt tests. Each step is
independently visible and retryable in the Airflow UI.
"""

import logging
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from sa_power_pipeline.alerts import send_discord_alert
from sa_power_pipeline.fetch_status import main as extract_task
from sa_power_pipeline.load_bigquery import load_all_raw_files as load_task

logger = logging.getLogger(__name__)

DBT_PROJECT_DIR = "/opt/airflow/sa_power_dbt"
DBT_BIN = "/home/airflow/dbt-venv/bin/dbt"


def alert_on_failure(context):
    """Log and send a Discord alert when a task exhausts its retries."""
    ti = context["task_instance"]
    dag_id = context["dag"].dag_id
    run_time = context.get("logical_date")
    error = str(context.get("exception", "unknown error"))[:500]

    logger.error(
        "ALERT: Task '%s' in DAG '%s' failed after all retries. Run: %s",
        ti.task_id,
        dag_id,
        run_time,
    )

    send_discord_alert(
        f"**ALERT: {dag_id} failed**\n"
        f"Task: `{ti.task_id}`\n"
        f"Run: {run_time}\n"
        f"Error: {error}\n"
        f"Logs: {ti.log_url}"
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

    dbt_freshness = BashOperator(
        task_id="dbt_source_freshness",
        bash_command=f"{DBT_BIN} source freshness --project-dir {DBT_PROJECT_DIR}",
        retries=0,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"{DBT_BIN} run --project-dir {DBT_PROJECT_DIR}",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"{DBT_BIN} test --project-dir {DBT_PROJECT_DIR}",
    )

    extract >> load >> dbt_freshness >>dbt_run >> dbt_test