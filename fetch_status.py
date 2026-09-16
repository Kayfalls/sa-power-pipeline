import logging
import requests
import os
import json
from datetime import datetime,timezone
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("ESKOMSEPUSH_TOKEN")
HEADERS = {"token": TOKEN}

BASE_URL = "https://developer.sepush.co.za/business/3.1"

AREA_ID = "za_gt_jhb_fourways_4pef"
SCHEDULE_ID = "eskde-10" #From iteration 5/6


def save_json(data, filename):
    os.makedirs("data/raw", exist_ok=True)
    filepath = f"data/raw/{filename}"
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print("Saved to %s", filepath)


def handle_response(response, label):
    if response.status_code == 200:
        data = response.json()
        logger.info("%s: success", label)
        logger.info("Quota remaining: %s", response.headers.get("x-ratelimit-remaining"))
        return data
    elif response.status_code == 401:
        logger.error("%s: Unauthorised. Check ESKOMSEPUSH_TOKEN in .env", label)
    elif response.status_code == 429:
        logger.warning("%s: API quota exhausted for today.", label)
        logger.warning("Quota resets at: %s", response.headers.get("x-ratelimit-reset"))
    elif response.status_code == 400:
        logger.error("%s: Bad request - Check ID format.", label)
    else:
        logger.error("%s: Unexpected status code %s", label, response.status_code)
        logger.error(response.text)
    return None

def fetch_status(timestamp):
    response = requests.get(f"{BASE_URL}/status", headers=HEADERS)
    data = handle_response(response, "status")
    if data:
        save_json(data, f"status_{timestamp}.json")
    return data

def fetch_area(area_id, timestamp):
    response = requests.get(f"{BASE_URL}/area", headers=HEADERS, params={"id": area_id})
    data = handle_response(response, "area")
    if data:
        save_json(data, f"area_{area_id}_{timestamp}.json")
    return data

def fetch_schedule(schedule_id, timestamp):
    response = requests.get(f"{BASE_URL}/schedule", headers=HEADERS, params={"id": schedule_id})
    data = handle_response(response, "schedule")
    if data:
        save_json(data, f"schedule_{schedule_id}_{timestamp}.json")
    return data

def main():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    logger.info("Starting pipeline run: %s", timestamp)
    fetch_status(timestamp)
    fetch_area(AREA_ID, timestamp)
    fetch_schedule(SCHEDULE_ID, timestamp)
    logger.info("Pipeline run complete: %s", timestamp)

if __name__ == "__main__":
    main()