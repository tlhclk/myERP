# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views import View
from functions.report import *
from functions.general import *


def change_state(request):
	if "series_id" in request.GET:
		series_id=request.GET["series_id"]
		series=Series.objects.get(pk=series_id)
	else:
		series=None
	if "state_id" in request.GET:
		state_id=request.GET["state_id"]
	else:
		state_id = 4
	try:
		series.state_id = state_id
		series.save()
		return JsonResponse({"status": True})
	except:
		return JsonResponse({"status":False})

class SeriesHome(View):
	template_name = "series/series_report.html"

	def get_context_data(self):
		context_data = {}
		context_data["title"] = "Seri Raporu"
		context_data["state_list"] = SeriesStateLM.objects.all().order_by("desc")
		return context_data
	
	def get(self, request):
		return render(request, self.template_name, context=self.get_context_data())