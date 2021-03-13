# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,reverse
from django.views import View
from django.views.generic import FormView
from functions.general import *
from functions.report import *
from functions import organizer
from django.http import JsonResponse
import datetime as dt
from .forms import MultiTransactionAddForm


def get_report_data(request):
	if "m_name" in request.GET:
		m_name=request.GET["m_name"]
	else:
		m_name=None
	if m_name=="Transaction":
		tr=TransactionReport(request)
		id_list,name_list,data_list=tr.gather_info()
		rep_model=tr.get_rep_model()
		return JsonResponse({"id_list":id_list,"name_list":name_list,"data_list":data_list,"rep_model":rep_model})
	elif m_name=="Account":
		ar=AccountReport(request)
		id_list,name_list,data_list=ar.gather_info()
		rep_model=ar.get_rep_model()
		return JsonResponse({"id_list":id_list,"name_list":name_list,"data_list":data_list,"rep_model":rep_model})
	else:
		return JsonResponse({"id_list": [], "name_list": [], "data_list": [],"rep_model":None})

class FinancialHome(View):
	template_name = "financial/financial_report.html"
	
	def get_context_data(self):
		context_data = HomeData(self.request).get_context_data()
		context_data["title"] = "Finans Raporu"
		report_data=[]
		report_data.append((False,"chart1","Mevcut Hesap Durumu","name","Account"))
		report_data.append((True,"chart2","Hesap Bazlı Gider Dağılımı","account","Transaction",1))
		report_data.append((True,"chart3","Kategori Bazlı Gider Dağılımı","category","Transaction",1))
		report_data.append((True,"chart4","Firma Bazlı Gider Dağılımı","corporation","Transaction",1))
		report_data.append((True,"chart5","Firma Bazlı Gelir Dağılımı","corporation","Transaction",2))
		context_data["report_data"]=report_data
		return context_data
	
	def get(self, request):
		return render(request, self.template_name, context=self.get_context_data())

def build_transaction_history(request):
	account_list=Account.objects.filter(user=request.user).filter(is_active=True)
	return organizer.build_transaction_history(account_list)

class MultiTransactionAdd(FormView):
	template_name = "financial/transaction_form.html"
	tra_obj = None
	form_class=MultiTransactionAddForm

	def get_fields(self):
		self.tra_obj=ModelLM.objects.get(pk=10)
		self.field_list = FieldLM.objects.filter(model=self.tra_obj)
		self.fields = [field.name for field in self.field_list]
	
	def get_context_data(self, **kwargs):
		context ={}
		self.get_fields()
		context["form_title"] = "Çoklu İşlem Kaydı"
		context["title"] = "Çoklu İşlem Kaydı"
		context["m_name"] = self.tra_obj.name
		context["list_title"] = "İşlem Listesi"
		context["last_object"]=Transaction.objects.first()
		context["detail_title"]="Son İşlem Kaydı"
		context["form"]=self.get_form(self.get_form_class())
		return context
	
	def get_form_kwargs(self):
		kwargs = super(MultiTransactionAdd, self).get_form_kwargs()
		kwargs["request"] = self.request
		return kwargs
	
	def form_valid(self, form):
		new_transaction=form.transaction_save(self.request.user)
		form.change_save(new_transaction)
		form.repetitive_record_save(new_transaction)
		return self.get_success_url(form=form)
	
	def get_initial(self):
		initial_dict = super(MultiTransactionAdd, self).get_initial()
		for item in self.request.GET:
			initial_dict[item] = self.request.GET.get(item)
		return initial_dict
	
	def get_success_url(self,**kwargs):
		form=kwargs["form"]
		new_kwargs={}
		new_kwargs["account"] = form.cleaned_data["account"].id
		new_kwargs["date"] = str(form.cleaned_data["date"])
		new_kwargs["time"] = str(form.cleaned_data["time"])
		new_kwargs["category"] = form.cleaned_data["category"].id
		new_kwargs["corporation"] = form.cleaned_data["corporation"].id
		new_kwargs["desc"] = form.cleaned_data["desc"]
		new_kwargs["tr_type"] = form.cleaned_data["tr_type"].id
		new_kwargs["amount"] = form.cleaned_data["amount"]
		person = form.cleaned_data["person"]
		if person!=None:
			new_kwargs["person"]=person.id
		change = form.cleaned_data["change"]
		if change!=None:
			new_kwargs["change"]=change.id
		repetitive_record = form.cleaned_data["repetitive_record"]
		if repetitive_record!=None:
			new_kwargs["repetitive_record"]=repetitive_record.id
		redirect_url=redirect("financial:multi_transaction_add_function").url+"?"+"&".join(["%s=%s" % (key,value) for key,value in new_kwargs.items()])
		return redirect(redirect_url)


class CategoryReport(View):
	template_name = "financial/transaction_category_report.html"
	
	def get_context_data(self):
		context_data = HomeData(self.request).get_context_data()
		context_data["title"] = "Kategori Bazlı İşlem Hacmi Raporu"
		mq = ModelQueryset(self.request)
		category_list = mq.get_queryset("TransactionCategoryLM")
		context_data["category_list"] = category_list
		return context_data
	
	def get(self, request):
		return render(request, self.template_name, context=self.get_context_data())

def get_category_report_data(request):
	cat_id = request.GET["cat_id"]
	rr = TransactionCategoryReport(request)
	name_list, data_list = rr.gather_info(cat_id)
	return JsonResponse({"name_list": name_list, "data_list": data_list})
	