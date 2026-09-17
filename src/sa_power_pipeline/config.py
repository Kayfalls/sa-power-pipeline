"""Configuration for the sa-power-pipeline package.

Values here are the pipeline's current target area/schedule.
Iteration 13+ will make these dynamic (area search) - for now
they stay centralized so  there's one place to change them
"""


import os
from dotenv import load_dotenv

load_dotenv()

ESKOMSEPUSH_TOKEN: str | None = os.getenv("ESKOMSEPUSH_TOKEN")
BASE_URL: str = "https://developer.sepush.co.za/business/3.1"

AREA_ID: str = "za_gt_jhb_fourways_4pef"
SCHEDULE_ID: str = "eskde-10"

RAW_DATA_DIR: str = "data/raw"