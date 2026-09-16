import requests
import os
import json
from datetime import datetime,timezone
from dotenv import load_dotenv

load_dotenv()

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
    print("Saved to", filepath)


def handle_response(response, label):
    if response.status_code == 200:
        data = response.json()
        print(data)
        print("Quota remaining:", response.headers.get("x-ratelimit-remaining"))
        return data
    elif response.status_code == 401:
        print(f"ERROR ({label}): Unauthorised. Check ESKOMSEPUSH_TOKEN in .env")
    elif response.status_code == 429:
        print(f"ERROR ({label}): API quota exhausted for today.")
        print("Quota resets at:", response.headers.get("x-ratelimit-reset"))
    elif response.status_code == 400:
        print(f"ERROR ({label}): Bad request - Check ID format.")
    else:
        print(f"ERROR ({label}): Unexpected status code {response.status_code}")
        print(response.text)
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
    fetch_status(timestamp)
    fetch_area(AREA_ID, timestamp)
    fetch_schedule(SCHEDULE_ID, timestamp)

if __name__ == "__main__":
    main()