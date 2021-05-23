# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import *
from functions.report import CalendarrReport, PeopleReport
from functions.general import HomeData
from constant.models import SeriesStateLM
from django.contrib.auth.views import LoginView, LogoutView
from authentication.forms import RegisterForm
from authentication.models import UserIp,MyUserProfile
from functions.auth_func import ModelQueryset, ModelFunc
from django.contrib.auth.models import User
from functions.other import MailService

class Index(View):
	template_name = "index.html"
	
	def get_context_data(self):
		context_data = HomeData(self.request).get_context_data()
		context_data["title"] = "Hoş Geldiniz"
		return context_data
	
	def get(self, request):
		return render(request, self.template_name, context=self.get_context_data())


class Home(View):
	template_name = "home.html"
	
	def get_context_data(self):
		context_data = HomeData(self.request).get_context_data()
		report_data = []
		report_data.append((1, 1, 1, "name", "Account"))
		context_data["report_data"] = report_data
		cr = CalendarrReport(self.request)
		context_data["rr_object_list"] = cr.get_repetitiverecord_data()
		pr = PeopleReport(self.request)
		context_data["f_object_list"] = pr.get_favorites_data()
		context_data["series_title"] = "Takip Edilen Seriler"
		context_data["state"] = SeriesStateLM.objects.get(pk=2)
		return context_data
	
	def get(self, request):
		return render(request, self.template_name, context=self.get_context_data())


class GlobalAddView(ModelFunc, CreateView):
	template_name = "global_form.html"
	ability = "Add"
	model_obj = None
	fields = []
	field_list = None
	
	def __init__(self):
		super(GlobalAddView, self).__init__()
	
	def get_queryset(self):
		self.model_obj = self.get_model_obj(self.kwargs["m_name"])
		self.model = self.get_model(self.model_obj)
		self.field_list = self.get_model_fields(self.model_obj, self.ability)
		self.fields = [field.name for field in self.field_list]
		object_list = self.model.objects.all()
		return object_list
	
	def get_context_data(self, **kwargs):
		context = super(GlobalAddView, self).get_context_data()
		context["profile_pic_path"] = HomeData(self.request).get_profile_pic_path()
		context["form_title"] = self.model_obj.form_title % "Yeni"
		context["title"] = self.model_obj.form_title % "Yeni"
		context["field_list"] = self.field_list
		context["m_name"] = self.model_obj.name
		context["list_title"] = self.model_obj.list_title
		return context
	
	def form_valid(self, form):
		self.object = form.save()
		self.object.save()
		return super().form_valid(form)
	
	def get_success_url(self):
		return redirect("global_detail", m_name=self.model_obj.name, pk=self.object.id).url
	
	def get_initial(self):
		initial_dict = super(GlobalAddView, self).get_initial()
		for item in self.request.GET:
			initial_dict[item] = self.request.GET.get(item)
		return initial_dict
	
	def get_form(self, form_class=None):
		form = super(GlobalAddView, self).get_form(form_class)
		for f_name, form_field in form.fields.items():
			form_field.widget.attrs["class"] = "form-control"
			if "date" in f_name:
				form_field.widget.attrs["data-toggle"] = "datetimepicker"
				form_field.widget.attrs["data-target"] = "#id_" + f_name
				form_field.widget.attrs["class"] += " datetimepicker date"
			elif "time" in f_name:
				form_field.widget.attrs["data-toggle"] = "datetimepicker"
				form_field.widget.attrs["data-target"] = "#id_" + f_name
				form_field.widget.attrs["class"] += " datetimepicker time"
		return form


class GlobalUpdateView(ModelFunc, UpdateView):
	template_name = "global_form.html"
	ability = "Update"
	fields = []
	
	def __init__(self):
		super(GlobalUpdateView, self).__init__()
	
	def get_queryset(self):
		self.model_obj = self.get_model_obj(self.kwargs["m_name"])
		self.model = self.get_model(self.model_obj)
		self.field_list = self.get_model_fields(self.model_obj, self.ability)
		self.fields = [field.name for field in self.field_list]
		object_list = self.model.objects.all()
		return object_list
	
	def get_context_data(self, **kwargs):
		context = super(GlobalUpdateView, self).get_context_data()
		context["profile_pic_path"] = HomeData(self.request).get_profile_pic_path()
		context["form_title"] = self.model_obj.form_title % self.object
		context["title"] = self.model_obj.form_title % self.object
		context["field_list"] = self.field_list
		context["m_name"] = self.model_obj.name
		context["list_title"] = self.model_obj.list_title
		return context
	
	def form_valid(self, form):
		self.object = form.save()
		return super().form_valid(form)
	
	def get_success_url(self):
		return redirect("global_detail", m_name=self.model_obj.name, pk=self.object.id).url
	
	def get_form(self, form_class=None):
		form = super(GlobalUpdateView, self).get_form(form_class)
		for f_name, form_field in form.fields.items():
			form_field.widget.attrs["class"] = "form-control"
			if "date" in f_name:
				form_field.widget.attrs["data-toggle"] = "datetimepicker"
				form_field.widget.attrs["data-target"] = "#id_" + f_name
				form_field.widget.attrs["class"] += " datetimepicker date"
			elif "time" in f_name:
				form_field.widget.attrs["data-toggle"] = "datetimepicker"
				form_field.widget.attrs["data-target"] = "#id_" + f_name
				form_field.widget.attrs["class"] += " datetimepicker time"
		return form


class GlobalDeleteView(ModelFunc, DeleteView):
	template_name = "global_delete.html"
	ability = "Delete"
	
	def __init__(self):
		super(GlobalDeleteView, self).__init__()
	
	def get_queryset(self):
		self.model_obj = self.get_model_obj(self.kwargs["m_name"])
		self.model = self.get_model(self.model_obj)
		# self.field_list=self.get_model_fields(self.model_obj,self.ability)
		object_list = self.model.objects.all()
		return object_list
	
	def get_context_data(self, **kwargs):
		context = super(GlobalDeleteView, self).get_context_data()
		context["profile_pic_path"] = HomeData(self.request).get_profile_pic_path()
		context["delete_title"] = self.model_obj.form_title % self.object
		context["title"] = self.model_obj.form_title % self.object
		context["m_name"] = self.model_obj.name
		return context
	
	def get_success_url(self):
		return redirect("global_list", m_name=self.model_obj.name).url


class GlobalListView(ModelFunc, ListView):
	template_name = "global_list.html"
	paginate_by = 50
	ability = "List"
	fields = []
	
	def __init__(self):
		super(GlobalListView, self).__init__()
	
	def get_extras(self):
		extra_dict = {}
		for item in self.request.GET:
			extra_dict[item] = self.request.GET[item]
		return extra_dict
	
	def get_queryset(self):
		mq = ModelQueryset(self.request)
		object_list = mq.get_queryset(self.kwargs["m_name"])
		return object_list
	
	def get_fields(self):
		return self.get_model_fields(self.kwargs["m_name"], self.ability)
	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(GlobalListView, self).get_context_data()
		context["profile_pic_path"] = HomeData(self.request).get_profile_pic_path()
		self.model_obj = self.get_model_obj(self.kwargs["m_name"])
		context["m_name"] = self.model_obj.name
		context["title"] = self.model_obj.list_title
		context["fields"] = self.get_fields()
		return context


class GlobalDetailView(ModelFunc, DetailView):
	template_name = "global_detail.html"
	ability = "Detail"
	fields = []
	
	def __init__(self):
		super(GlobalDetailView, self).__init__()
	
	def get_queryset(self):
		self.model_obj = self.get_model_obj(self.kwargs["m_name"])
		self.model = self.get_model(self.model_obj)
		object_list = self.model.objects.all()
		return object_list
	
	def get_fields(self):
		return self.get_model_fields(self.kwargs["m_name"], self.ability)
	
	def get_context_data(self, **kwargs):
		context = super(GlobalDetailView, self).get_context_data()
		context["profile_pic_path"] = HomeData(self.request).get_profile_pic_path()
		context["title"] = self.model_obj.detail_title % self.object
		context["m_name"] = self.model_obj.name
		context["list_title"] = self.model_obj.list_title
		context["fields"] = self.get_fields()
		return context


class MyLoginView(LoginView):
	def get_perm(self, user_name, ip):
		perm_list = UserIp.objects.filter(user_name__username=user_name, ip=ip)
		if len(perm_list) == 0:
			user_list = User.objects.filter(username=user_name)
			if len(user_list) > 0:
				user = user_list[0]
				new_user_ip = UserIp.objects.create(user_name=user, ip=ip, permission=False)
				new_auth_key = new_user_ip.create_auth_key()
				new_user_ip.auth_key = new_auth_key
				new_user_ip.save()
				ms = MailService("admin@myerp.talhacelik.com")
				ms.set_recipient_list(["talhacelk@gmail.com"])
				ms.set_subject("Yeni Ip Ile Giris Denemesi")
				ms.set_headers("Yeni Ip Ile Giris Denemesi")
				message="Giris Benemesi Bilgileri:\n\nIp:%s\nKullanıcı Adı:%s\nKullanıcı Mail Adresi:%s\nKullanıcı Adı Soyadı:%s\nYetkilendirme Anahtarı:%s\n\nAdresinde yapılan kullanıcı girisi engellendi\nYetkilendirmek İcin <a href='https://myerp.talhacelik.com/register_validation/?validation_code=%s'>Buraya Tıklayınız!</a>\n" %(ip, user.username, user.email, user.get_full_name(), new_auth_key, new_auth_key)
				ms.set_body(message)
				ms.send_email()
		else:
			if perm_list[0].permission == True:
				return True
		return False
	
	def form_valid(self, form):
		ip = self.request.META["REMOTE_ADDR"]
		self.request.session.set_expiry(14400)
		if self.request.method == "POST":
			login_form = self.request.POST
			user_name = login_form["username"]
			if not self.get_perm(user_name, ip):
				return redirect("/login/?warning=NoPermission")
			if "remember_me" in login_form:
				if login_form["remember_me"] == "on":
					self.request.session.set_expiry(3600 * 24 * 30)
		return super(MyLoginView, self).form_valid(form)
	
	def get_success_url(self):
		return redirect("home").url


class MyLogOutView(LogoutView):
	def get_success_url_allowed_hosts(self):
		return redirect("/")


class MyRegisterView(FormView):
	template_name = "registration/register.html"
	form_class = RegisterForm
	
	def form_valid(self, form):
		ip = self.request.META["REMOTE_ADDR"]
		if self.request.method == "POST":
			form.save(ip)
		return HttpResponseRedirect(self.get_success_url())
	
	def get_success_url(self):
		user_ip = UserIp.objects.last()
		return "/register_validation/?validation_code=%s" % (user_ip.auth_key)


class RegisterValidationView(View):
	def grant_permission(self, user_ip):
		user_ip.permission = True
		user_ip.save()
	
	def get(self, request):
		if "validation_code" in request.GET:
			auth_key = request.GET["validation_code"].replace(" ", "+")
			user_ip_list = UserIp.objects.filter(permission=False).filter(auth_key=auth_key)
			for user_ip in user_ip_list:
				self.grant_permission(user_ip)
				return redirect("/login")
		return redirect("/home")