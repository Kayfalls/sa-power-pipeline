import logging
import requests
import os
import json
from datetime import datetime,timezone
from typing import Any

from sa_power_pipeline.config import (
    ESKOMSEPUSH_TOKEN,
    BASE_URL,
    AREA_ID,
    SCHEDULE_ID,
    RAW_DATA_DIR,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

HEADERS: dict[str, str] = {"token": ESKOMSEPUSH_TOKEN or ""}


def save_json(data: dict[str, Any], filename: str) -> None:
    """Write a dict to data/raw/<filename> as a single-line NDJSON record. """
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    filepath = f"{RAW_DATA_DIR}/{filename}"
    with open(filepath, "w") as f:
        f.write(json.dumps(data) + "\n")
    logger.info("Saved to %s", filepath)


def handle_response(response: requests.Response, label:str) -> dict[str, Any] | None:
    """Inspect an API response and return its JSON body, or None on failure."""
    if response.status_code == 200:
        data = response.json()
        logger.info("%s: success", label)
        logger.info("Quota remaining: %s", response.headers.get("x-ratelimit-remaining"))
        return data
    elif response.status_code == 401:
        logger.error("%s: Unauthorized. Check ESKOMSEPUSH_TOKEN in .env", label)
    elif response.status_code == 429:
        logger.warning("%s: API quota exhausted for today.", label)
        logger.warning("Quota resets at: %s", response.headers.get("x-ratelimit-reset"))
    elif response.status_code == 400:
        logger.error("%s: Bad request - check ID format.", label)
    else:
        logger.error("%s: Unexpected status code %s", label, response.status_code)
        logger.error(response.text)
    return None

def fetch_status(timestamp: str) -> dict[str, Any] | None:
    """Fetch national/municipal loadshedding status and save it. """
    response = requests.get(f"{BASE_URL}/status", headers=HEADERS)
    data = handle_response(response, "status")
    if data:
        data["extracted_at"] = timestamp
        save_json(data, f"status_{timestamp}.json")
    return data

def fetch_area(area_id: str, timestamp:str) -> dict[str, Any] | None:
    """Fetch area metadata (name, schedules) for a given area id and save it. """
    response = requests.get(f"{BASE_URL}/area", headers=HEADERS, params={"id": area_id})
    data = handle_response(response, "area")
    if data:
        data["extracted_at"] = timestamp
        save_json(data, f"area_{area_id}_{timestamp}.json")
    return data

def fetch_schedule(schedule_id: str, timestamp: str) -> dict[str, Any] | None:
    """Fetch schedule events/slots for a given schedule id and save it. """
    response = requests.get(f"{BASE_URL}/schedule", headers=HEADERS, params={"id": schedule_id})
    data = handle_response(response, "schedule")
    if data:
        data["extracted_at"] = timestamp
        save_json(data, f"schedule_{schedule_id}_{timestamp}.json")
    return data

def main() -> None:
    """Run one full pipeline pass: status, area, schedule. """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    logger.info("Starting pipeline run: %s", timestamp)
    fetch_status(timestamp)
    fetch_area(AREA_ID, timestamp)
    fetch_schedule(SCHEDULE_ID, timestamp)
    logger.info("Pipeline run complete: %s", timestamp)

if __name__ == "__main__":
    main()