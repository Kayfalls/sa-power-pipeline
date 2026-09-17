"""Single entrypoint: extract from EskomSePush, then load into BigQuery.

This is the script a scheduler (Airflow, cron, etc.) will eventualy
call. It composes the two existing modules rather than duplicating
their logic.
"""

import logging

from sa_power_pipeline.fetch_status import main as extract
from sa_power_pipeline.load_bigquery import load_all_raw_files as load

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

def run() -> None:
    """Run one full extract-then-load pipeline pass."""
    logger.info("=== Starting ELT pipeline ===")
    extract()
    load()
    logger.info("=== Pipeline run complete ===")

if __name__ == "__main__":
    run()
    