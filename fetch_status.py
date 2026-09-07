import requests
import os
import json
from datetime import datetime,timezone
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("ESKOMSEPUSH_TOKEN")

url = "https://developer.sepush.co.za/business/3.1/status"
headers = {"token": token}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
    print("Quota remaining:", response.headers.get("x-ratelimit-remaining"))
    print("Quota resets at:", response.headers.get("x-ratetime-reset"))
    
    os.makedirs("data/raw", exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"data/raw/status_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print("Saved to", filename)

elif response.status_code == 401:
    print("ERROR: Unauthorized. Check that ESKOMSEPUSH_TOKEN is set correctly in .env")

elif response.status_code == 429:
    print("ERROR: API quota exhausted for today.")
    print("Quota resets at:", response.headers.get("x-ratelimit-reset"))

else:
    print(f"ERROR: Unexpected status code {response.status_code}")
    print(response.text)

# Area Information
area_id = "za_gt_jhb_fourways_4pef" #hardcoded for now
area_url = "https://developer.sepush.co.za/business/3.1/area"
area_params = {"id": area_id}

area_response = requests.get(area_url, headers=headers, params=area_params)

if area_response.status_code == 200:
    area_data = area_response.json()
    print(area_data)

    area_filename = f"data/raw/area_{area_id}_{timestamp}.json"
    with open(area_filename, "w") as f:
        json.dump(area_data, f, indent=2)

    print("Saved to", area_filename)

elif area_response.status_code == 401:
    print("ERROR: Unauthorized on area request. Check token.")

elif area_response.status_code == 429:
    print("ERROR: API quota exhausted for today.")
    print("Quota resets at:", area_response.headers.get("x-ratelimit-reset"))

else:
    print(f"ERROR: Unexpected status code {area_response.status_code}")
    print(area_response.text)