"""Load raw NDJSON files from data/raw/ into BigQuery.

Table name is derived from filename prefix:
    status_*.json -> raw.status
    area_*.json -> raw.area
    schedule_*.json -> raw.schedule
"""
from sa_power_pipeline.config import RAW_DATA_DIR
import os
import glob
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
RAW_DATA_DIR = "data/raw" 

def table_name_for_file(filepath: str) -> str:
    """Derive a BigQuery table name from a raw filename's prefix. """
    filename = os.path.basename(filepath)
    if filename.startswith("status_"):
        return "status"
    elif filename.startswith("area_"):
        return "area"
    elif filename.startswith("schedule_"):
        return "schedule"
    else:
        raise ValueError(f"Unrecognized file prefix: {filename}")



def load_json_file_to_bq(client: bigquery.Client, filepath: str, table_name: str) -> None:
    """Load a single local JSON file into a BigQuery table, autodetecting schema. """
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

def load_all_raw_files() -> None:
    """Load every NDJSON file in data/raw/ into its matching BigQuery table."""
    client = bigquery.Client(project=PROJECT_ID)
    filepaths = glob.glob(f"{RAW_DATA_DIR}/*.json")

    if not filepaths:
        logger.warning("No files found in %s", RAW_DATA_DIR)
        return

    for filepath in filepaths:
        try:
            table_name = table_name_for_file(filepath)
            load_json_file_to_bq(client, filepath, table_name)
        except ValueError as e:
            logger.warning(str(e))

if __name__ == '__main__':
    load_all_raw_files()
