from datetime import datetime
from dateutil import parser

from gservices import create_service, get_todays_events
from snspublish import publish

CRED_FILE = 'creds/credentials.json'
CALENDAR_API_NAME = 'calendar'
CALENDAR_API_VERSION = 'v3'
TASKS_API_NAME = 'tasks'
TASKS_API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/tasks.readonly']

calendar = create_service(CALENDAR_API_NAME, CALENDAR_API_VERSION, CRED_FILE, SCOPES)
tasks = create_service(TASKS_API_NAME, TASKS_API_VERSION, CRED_FILE, SCOPES)

calendar_overview = ''
todays_events = get_todays_events(calendar)
for event in todays_events:
    name = event.get('summary')
    start = event.get('start').get('dateTime')
    end = event.get('end').get('dateTime')

    if start != None and end != None:
        start = parser.parse(start).strftime('%I:%M%p').lower()
        end = parser.parse(end).strftime('%I:%M%p').lower()
        calendar_overview += f'{start}-{end}: {name}\n'
    else:
        calendar_overview += f'all day: {name}\n'

curr_date = datetime.now()
subject = f'daily overview - {curr_date.strftime("%b %d").lower()} ◝(๑꒪່౪̮꒪່๑)◜'
message = f'daily overview for {curr_date.strftime("%B %d %Y").lower()}:\n\n{calendar_overview}'

publish(subject, message)