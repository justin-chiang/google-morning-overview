from gservices import create_service

CRED_FILE = 'credentials.json'

CALENDAR_API_NAME = 'calendar'
CALENDAR_API_VERSION = 'v3'
CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

TASKS_API_NAME = 'tasks'
TASKS_API_VERSION = 'v1'
TASKS_SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']

calendar = create_service(CALENDAR_API_NAME, CALENDAR_API_VERSION, CRED_FILE, CALENDAR_SCOPES)
tasks = create_service(TASKS_API_NAME, TASKS_API_VERSION, CRED_FILE, TASKS_SCOPES)
