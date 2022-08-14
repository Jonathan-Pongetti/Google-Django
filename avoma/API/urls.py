from django.urls import path
from API import views

urlpatterns = [
    path('', views.setupHook, name='setupHook'),
    path('calendar/weeks/busiest', views.busiestWeek, name='weeks'),
    path('calendar/mostmeetings/', views.mostMeetings, name='mostmeetings'),
    path('calendar/timespent/', views.timeSpent, name='timespent'),
    path('calendar/', views.calendarAPI, name='calendarAPI'),
    path('pushnotification/', views.pushNotification, name='pushnotification'),
]