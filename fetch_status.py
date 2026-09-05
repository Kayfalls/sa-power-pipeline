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