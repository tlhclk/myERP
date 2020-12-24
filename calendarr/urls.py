# -*- coding: utf-8 -*-
### import_part
from django.urls import path
from . import views


### path_part
app_name='calendarr'
urlpatterns = [
	path('',views.CalendarrHome.as_view(),name='calendarrhome'),
]