from datetime import datetime
from dateutil import parser

from gservices import create_service, get_todays_events, get_tasks
from snspublish import publish

CRED_FILE = 'creds/credentials.json'
CALENDAR_API_NAME = 'calendar'
CALENDAR_API_VERSION = 'v3'
TASKS_API_NAME = 'tasks'
TASKS_API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/tasks.readonly']

calendar = create_service(CALENDAR_API_NAME, CALENDAR_API_VERSION, CRED_FILE, SCOPES)
tasks = create_service(TASKS_API_NAME, TASKS_API_VERSION, CRED_FILE, SCOPES)

calendar_overview = 'Google Calendar Overview: \n'
todays_events = get_todays_events(calendar)
if len(todays_events) != 0:
    for event in todays_events:
        name = event.get('summary')
        start = event.get('start').get('dateTime')
        end = event.get('end').get('dateTime')

        if start != None and end != None:
            start = parser.parse(start).strftime('%I:%M%p')
            end = parser.parse(end).strftime('%I:%M%p')
            calendar_overview += f'• {start}-{end}: {name}\n'
        else:
            calendar_overview += f'all day: {name}\n'
else:
    calendar_overview += f'• No events today!\n'

tasks_overview = 'Google Tasks Overview: \n'
total_tasks = get_tasks(tasks)
if len(total_tasks) != 0:
    for task in total_tasks:
        name = task.get('title')
        tasks_overview += f'• {name}\n'
else:
    tasks_overview += f'• No tasks due today!\n'

curr_date = datetime.now()
subject = f'Daily Overview - {curr_date.strftime("%b %d")}'
message = f'Your daily overview for {curr_date.strftime("%B %d %Y")}:\n\n{calendar_overview}\n{tasks_overview}'

publish(subject, message)