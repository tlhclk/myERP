# -*- coding: utf-8 -*-
### import_part
from django.urls import path
from . import views


### path_part
app_name='financial'
urlpatterns = [
	path('',views.FinancialHome.as_view(),name='financialhome_report'),
	path('get_report_data/',views.get_report_data,name='get_report_data_ajax'),
	path('build_transaction_history/',views.build_transaction_history,name='build_transaction_history_function'),
	path('multi_transaction_add/',views.MultiTransactionAdd.as_view(),name='multi_transaction_add_function'),
	path('transaction_category_report/',views.CategoryReport.as_view(),name='transaction_category_report'),
	path('get_category_report_data/',views.get_category_report_data,name='get_category_report_data_ajax'),
]