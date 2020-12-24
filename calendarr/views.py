# -*- coding: utf-8 -*-
from django.shortcuts import redirect,render
from .models import *
from functions.report import *
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime as dt
from functions.general import HomeData
from django.views import View


class CalendarrHome(View):
	template_name = "calendarr/calendarr_report.html"
	
	def get_context_data(self):
		context_data = HomeData().get_context_data()
		cr = CalendarrReport(self.request)
		context_data["title"] = "Takvim Raporu"
		context_data["rr_title"] = "İşleme Alınacak Tekrarlı Olaylar"
		context_data["rr_object_list"] = cr.get_repetitiverecord_data()
		context_data["er_title"] = "Yaklaşan Etkinlikler"
		context_data["er_object_list"] = cr.get_comingevent_data()
		return context_data
	
	def get(self, request):
		return render(request, self.template_name, context=self.get_context_data())