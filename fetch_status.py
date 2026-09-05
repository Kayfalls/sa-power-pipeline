import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("ESKOMSEPUSH_TOKEN")

url = "https://developer.sepush.co.za/business/3.1/status"
headers = {"token": token}

response = requests.get(url, headers=headers)
data = response.json()

print(data)

os.makedirs("data/raw", exist_ok=True)
with open("data/raw/status.json", "w") as f:
    json.dump(data, f, indent=2)