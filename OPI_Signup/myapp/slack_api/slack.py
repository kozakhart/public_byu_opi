import os
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK')

def send_slack_message(message: str):
    import requests
    payload = '{"text": "%s"}' % message
    response = requests.post(
        SLACK_WEBHOOK,
        data = payload
    )
    print(response.text)

SLAT_SLACK_WEBHOOK = os.getenv('SLAT_SLACK_WEBHOOK')

def send_slat_slack_message(message: str):
    import requests
    payload = '{"text": "%s"}' % message
    response = requests.post(
        SLAT_SLACK_WEBHOOK,
        data = payload
    )
    print(response.text)
