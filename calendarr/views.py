# -*- coding: utf-8 -*-
from django.shortcuts import redirect,render
from functions.report import RepetitiveReport as RepReport,CalendarrReport
from django.views import View
from django.http import JsonResponse
from functions.auth_func import ModelQueryset
from functions.general import *

class CalendarrHome(View):
	template_name = "calendarr/calendarr_report.html"
	
	def get_context_data(self):
		context_data = HomeData(self.request).get_context_data()
		cr = CalendarrReport(self.request)
		context_data["title"] = "Takvim Raporu"
		context_data["rr_title"] = "İşleme Alınacak Tekrarlı Olaylar"
		context_data["rr_object_list"] = cr.get_repetitiverecord_data()
		context_data["er_title"] = "Yaklaşan Etkinlikler"
		context_data["er_object_list"] = cr.get_comingevent_data()
		return context_data
	
	def get(self, request):
		return render(request, self.template_name, context=self.get_context_data())
	
	
class RepetitiveReport(View):
	template_name = "calendarr/repetitive_report.html"
	
	def get_context_data(self):
		context_data = HomeData(self.request).get_context_data()
		context_data["title"] = "Tekrarlı İşlemler Raporu"
		mq=ModelQueryset(self.request)
		repetitive_list=mq.get_queryset("Repetitive")
		context_data["repetitive_list"]=repetitive_list
		return context_data
	
	def get(self, request):
		return render(request, self.template_name, context=self.get_context_data())


def get_report_data(request):
	rep_code=request.GET["rep_code"]
	rr=RepReport(request)
	id_list,name_list,data_list=rr.gather_info(rep_code)
	return JsonResponse({"id_list":id_list,"name_list":name_list,"data_list":data_list})