# -*- coding: utf-8 -*-
### import_part
from django.urls import path
from . import views


### path_part
app_name='main'
urlpatterns = [
	path('code_to_database/',views.code_to_database,name='code_to_database_function'),
]