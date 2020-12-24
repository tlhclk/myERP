# -*- coding: utf-8 -*-
from functions.excel_config.code_to_excel import *
from django.shortcuts import *
import os
from main.models import PanelLM


def code_to_database(request):
	cte = CodeToDb()
	cte.get_model_data()
	return redirect("home")
