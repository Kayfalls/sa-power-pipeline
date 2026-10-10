"""Send pipeline alerts to Discord via an incoming webhook.

Alerting must never be the thing that breaks the pipeline. so every
failure here is logged and swallowed rather than raised. Log lines
deliberately never include the exception text or the URL, because the
webhook URL is a secret.
"""

import os
import logging

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DISCORD_MESSAGE_LIMIT = 2000

def send_discord_alert(message:str) -> bool:
    """Post a message to the Discord webhook. Returns True if it was delivered."""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        logger.warning("DISCORD_WEBHOOK_URL is not set; alert not sent")
        return False

    try:
        response = requests.post(
            webhook_url,
            json={"content": message[:DISCORD_MESSAGE_LIMIT]},
            timeout=10,
        )
    except requests.RequestsException as e:
        logger.error("Failed to send Discord alert: %s", type(e).__name__)
        return False

    if not response.ok:
        logger.error("Discord rejected the alert (HTTP %s)", response.status_code)
        return False
    
    logger.info("Discord alert sent")
    return True

if __name__ == "__main__":
    send_discord_alert("Test alert from sa-power-pipeline: webhook is working")