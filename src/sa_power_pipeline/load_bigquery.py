"""Load raw JSON files from data/raw/ into BigQuery.

This is intentiionally simple: read a local JSON file, load it into
a BigQuery table with schema autodetect. No transformation happens
here -that's dbt's job, starting in a later iteration.
"""
import os
import logging
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET = "raw"



def load_json_file_to_bq(filepath:str, table_name:str) -> None:
    """Load a single local JSON file into a BigQuery table, autodetecting schema. """
    client = bigquery.Client(project=PROJECT_ID)
    table_id = f"{PROJECT_ID}.{DATASET}.{table_name}"
    
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    with open(filepath, "rb") as f:
        load_job = client.load_table_from_file(f, table_id, job_config=job_config)

    load_job.result() #waits for the job to finish
    logger.info("Loaded %s into %s", filepath, table_id)

if __name__ == '__main__':

    #Manual test: point this at one real file from data/raw/ to confirm the setup works
    load_json_file_to_bq("data/raw/status_20260905T081009Z.json", "status_test")
