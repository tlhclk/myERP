# -*- coding: utf-8 -*-
### import_part
from django.urls import path
from . import views


### path_part
app_name='demo'
urlpatterns = [
	path('listen_comport/',views.listen_comport,name='listen_comport'),
	path('port_listener/',views.port_listener,name='port_listener_ajax'),
	path('demo/',views.demo,name='demo_ajax'),
	
]