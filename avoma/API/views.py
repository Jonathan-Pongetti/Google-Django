import os.path
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from API.serializers import TestSerializer, EventItemSerializer
from rest_framework.decorators import api_view
from API.models import EventItem
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.utils import timezone
from django.db.models.functions import ExtractWeek, TruncWeek

# Create your views here.


@csrf_exempt
def setupHook(request):
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    print('okay')
    service = build('calendar', 'v3', credentials=creds)

    eventcollect = {
        'id': str(uuid.uuid1()),
        'type': "web_hook",
        'address': "{address}/api/pushnotification/"
    }
    response = service.events().watch(calendarId='primary', body=eventcollect).execute()
    print(response)

    return JsonResponse('get methods', safe=False)

@csrf_exempt
def calendarAPI(request, id=0):
    if request.method=='GET':
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

        service = build('calendar', 'v3', credentials=creds)

                # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId="primary", timeMin=now,
                                              maxResults=10,
                                              ).execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return JsonResponse('no events found', safe=False)

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

        return JsonResponse(events, safe=False)



@csrf_exempt
def pushNotification(request):
    EventItem.objects.all().delete()
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    print('okay')
    service = build('calendar', 'v3', credentials=creds)
            # Call the Calendar API

    prev_months = datetime.utcnow() - relativedelta(months=+3)
    timeMin = prev_months.isoformat() +"Z"
    print('Getting the events from past 3 months')
    events_result = service.events().list(calendarId="primary", timeMin=timeMin).execute()
    events = events_result.get('items', [])
    if not events:
        print('No past events found.')
        return JsonResponse('no events found', safe=False)
    
    # # Prints the start and name of the next 10 events
    for event in events:

        if event["organizer"]["email"]== "unknownorganizer@calendar.google.com":
            continue
        Id = event["id"]
        creator = event["creator"]["email"]
        if "dateTime" in event["start"] and "dateTime" in event["end"]:
            start_time = event["start"]["dateTime"]
            end_time = event["end"]["dateTime"]
            duration = datetime.fromisoformat(end_time) - datetime.fromisoformat(start_time)
            print(duration)
        
            EventItem.objects.create(Id=Id,StartTime=start_time, EndTime=end_time, Duration=str(duration), Creator=creator)

        print('saved to db')
    return JsonResponse('google called this', safe=False)

@csrf_exempt
def timeSpent(request):
    event_list = EventItem.objects.all().values()
    total_time = timedelta()
    for event in event_list:
        if event['StartTime'] < timezone.now():
            (h, m, s) = str(event['Duration']).split(':')
            d = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            #print(total_time, ' + ', d, ' = ', total_time + d)
            total_time += d

    time = str(total_time).split(':')
    response_string = time[0] + " hours and " + time[1] + " minutes" 
    print(response_string)
    return JsonResponse(response_string, safe=False)

@csrf_exempt
def mostMeetings(request):
    event_list = EventItem.objects.all().values('Creator').annotate(total=Count('Creator')).order_by('-total')
    if event_list[0]["Creator"] == '':
        return JsonResponse(event_list[1], safe=False)
    else:
        return JsonResponse(event_list[0], safe=False)

@api_view(['GET'])
def busiestWeek(request):

    events = EventItem.objects.all().values().annotate(week=TruncWeek('StartTime')).order_by('week')
    week_events = events.values('week').order_by('week').annotate(count=Count('week')).order_by('-count')
    least_busy_week = week_events[0]
    most_busy_week = week_events[len(week_events)-1]
    print(least_busy_week, most_busy_week)
    
    return JsonResponse([least_busy_week, most_busy_week], safe=False)

