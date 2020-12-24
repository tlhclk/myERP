# -*- coding: utf-8 -*-
### import_part
from django.urls import path
from . import views


### path_part
app_name='people'
urlpatterns = [
	path('',views.PeopleHome.as_view(),name='peoplehome')
]