# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views import View
from functions.general import *
from functions.report import *


class PeopleHome(View):
	template_name = "people/people_report.html"
	person_id=None
	
	def get_relation_data(self):
		if "person_id" in self.request.GET:
			self.person_id = int(self.request.GET["person_id"])
			pr = PeopleReport(self.request)
			person=Person.objects.get(pk=self.person_id)
			return pr.get_relation_data(person)
		else:
			self.person_id = 440
			pr = PeopleReport(self.request)
			person=Person.objects.get(pk=self.person_id)
			return pr.get_relation_data(person)
	
	def get_context_data(self):
		context_data = HomeData(self.request).get_context_data()
		pr = PeopleReport(self.request)
		context_data["title"] = "Rehber Raporu"
		context_data["people_list"] = Person.objects.all()
		context_data["rt_title"] = "İlişki Ağacı"
		context_data["rt_object_dict"] = self.get_relation_data()
		context_data["f_title"] = "Sık Görüşülenler"
		context_data["f_object_list"] = pr.get_favorites_data()
		context_data["rt_id"] = self.person_id
		return context_data
	
	def get(self, request):
		return render(request, self.template_name, context=self.get_context_data())
	
