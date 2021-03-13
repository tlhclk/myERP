# -*- coding: utf-8 -*-
### import_part
from django.urls import path
from . import views


### path_part
app_name='calendarr'
urlpatterns = [
	path('',views.CalendarrHome.as_view(),name='calendarrhome_report'),
	path('repetitive_report/',views.RepetitiveReport.as_view(),name='repetitive_report'),
	path('get_report_data/',views.get_report_data,name='get_report_data_ajax'),
]