# -*- coding: utf-8 -*-
from functions.excel_config.code_to_excel import *
from django.shortcuts import *
import os
from main.models import PanelLM


def code_to_database(request):
	cte = CodeToDb()
	cte.get_file_path_data(os.getcwd())
	cte.get_database_info()
	cte.get_urls()
	cte.urls_parting()
	return redirect("home")
