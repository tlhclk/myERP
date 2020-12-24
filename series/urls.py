# -*- coding: utf-8 -*-
### import_part
from django.urls import path
from . import views


### path_part
app_name='series'
urlpatterns = [
	path('change_state',views.change_state,name='change_state'),
	path('',views.SeriesHome.as_view(),name='serieshome')
]