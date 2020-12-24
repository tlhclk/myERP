# -*- coding: utf-8 -*-
### import_part
from django.urls import path
from . import views


### path_part
app_name='financial'
urlpatterns = [
	path('',views.FinancialHome.as_view(),name='financialhome'),
	path('get_report_data/',views.get_report_data,name='get_report_data'),
	path('build_transaction_history/',views.build_transaction_history,name='build_transaction_history'),
	path('multi_transaction_add/',views.MultiTransactionAdd.as_view(),name='multi_transaction_add')
]