import os
import requests
import logging

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def send_slack_message(text: str) -> bool:
    if not SLACK_WEBHOOK_URL:
        logging.error("Slack webhook URL is not set.")
        return False

    payload = {"text": text}

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            logging.info("Slack message sent successfully.")
            return True
        else:
            logging.error(f"Slack message failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logging.exception("Exception while sending Slack message.")
        return False
