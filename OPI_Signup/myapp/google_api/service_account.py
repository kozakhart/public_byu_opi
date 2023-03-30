
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dateutil import parser
import datetime
import os
from pathlib import Path
import json

from dotenv import load_dotenv
load_dotenv()

CALENDAR_ID = os.getenv('Calendar_ID')

def main():
    dirname = os.path.dirname(__file__)
    SERVICE_ACCOUNT_FILE = os.path.join(dirname, 'service_creds.json')

    credentials = service_account.Credentials.from_service_account_file(filename=SERVICE_ACCOUNT_FILE)

    service = build('calendar', 'v3', credentials=credentials)

    Calendar_ID = CALENDAR_ID

    events = service.events().list(calendarId=Calendar_ID).execute()
    list = []
    dic = {}
    for any_event in events['items']:
        if "Center Closed" in any_event['summary']:
            date = any_event['start']['dateTime']
            date_preformat = parser.parse(date)
            date_format = datetime.datetime.strftime(date_preformat, '%m-%d-%Y')
            dic = {'Event':any_event['summary'], 'Date':date_format}
            list.append(dic)

    base_path = Path(__file__).parent
    file_path = (base_path / "events.json").resolve()
    with open(file_path, "w") as outfile:
        jsonString = json.dumps(list)
        outfile.write(jsonString)
        outfile.close()