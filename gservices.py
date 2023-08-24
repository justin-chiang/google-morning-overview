import os
import json
import pytz
from datetime import datetime, timedelta
from dateutil import tz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def create_service(api_name, api_version, cred_file, scopes):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_file, scopes)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build(api_name, api_version, credentials=creds, static_discovery=False)
        print(api_name, 'service built successfully')
        return service
    except HttpError as err:
        print(err)

def get_todays_events(service):
    today = datetime.utcnow().date()
    start = datetime(today.year, today.month, today.day, hour=7).isoformat() + 'Z'
    end = (datetime(today.year, today.month, today.day, hour=7) + timedelta(1)).isoformat() + 'Z'

    print(start)
    print(end)

    todays_events = []
    page_token = None
    while True:
        events = service.events().list(calendarId='primary', timeMin=start, timeMax=end, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        for event in events['items']:
            todays_events.append(event)
        page_token = events.get('nextPageToken')
        if not page_token:
            break

    return todays_events