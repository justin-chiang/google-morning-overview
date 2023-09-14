import os
from datetime import datetime, timedelta
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def create_service(api_name, api_version, cred_file, scopes):
    creds = None
    if os.path.exists('creds/token.json'):
        creds = Credentials.from_authorized_user_file('creds/token.json', scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_file, scopes)
            creds = flow.run_local_server(port=0)
        with open('creds/token.json', 'w') as token:
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

def get_tasks(service):
    today = datetime.now().date()
    start = datetime(today.year, today.month, today.day).isoformat() + 'Z'
    end = (datetime(today.year, today.month, today.day) + timedelta(1)).isoformat() + 'Z'

    tasklists = service.tasklists().list().execute()
    list_id = tasklists['items'][0]['id']

    tasks_list = []
    page_token = None
    while True:
        tasks = service.tasks().list(tasklist=list_id, showCompleted=False, dueMin=start, dueMax=end).execute()
        for task in tasks['items']:
            tasks_list.append(task)
        page_token = tasks.get('nextPageToken')
        if not page_token:
            break

    return tasks_list