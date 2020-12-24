# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,reverse
from functions.general import HomeData
from django.views.generic import *
from functions.form_after import *
import functions.auth_func as af
import functions.model as mdl
from operator import attrgetter as atg
from functions.report import CalendarrReport,PeopleReport
from constant.models import SeriesStateLM
from django.contrib.auth.views import LoginView
import datetime as dt


def form_redirection(request):
    previous_url=request.META["HTTP_REFERER"]
    url_parts=previous_url.split("/")
    m_name=url_parts[4]
    if m_name=="Transaction":
        fa=TransactionFormAfter(request)
        return fa.get_direction()
    elif m_name=="RepetitiveRecord":
        fa = RepetitiveRecordFormAfter(request)
        return fa.get_direction()
    else:
        if url_parts[3]=="add":
            last=sorted(af.get_queryset(request.user,m_name),key=atg("id"))[-1]
            return redirect("global_detail",m_name=m_name,pk=last.id)
        if url_parts[3]=="update":
            return redirect("global_detail",m_name=m_name,pk=url_parts[5])
        else:
            return redirect("global_list",m_name=m_name)

class Home(View):
    template_name = "home.html"

    def get_context_data(self):
        context_data = HomeData().get_context_data()
        if self.request.user.is_authenticated:
            report_data=[]
            report_data.append((1,1,1,"name","Account"))
            context_data["report_data"]=report_data
            cr = CalendarrReport(self.request)
            context_data["rr_object_list"] = cr.get_repetitiverecord_data()
            pr = PeopleReport(self.request)
            context_data["f_object_list"] = pr.get_favorites_data()
            context_data["series_title"] = "Takip Edilen Seriler"
            context_data["state"] = SeriesStateLM.objects.get(pk=2)
        return context_data

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

class GlobalAddView(CreateView):
    template_name = "global_form.html"
    ability = "Add"
    model_obj=None
    fields = []
    field_list=None
    
    def get_queryset(self):
        self.model_obj, self.model = af.get_model(self.kwargs["m_name"])
        self.field_list= af.get_fields(self.model_obj, self.ability)
        self.fields = [field.name for field in self.field_list]
        object_list = self.model.objects.all()
        return object_list
    
    def get_context_data(self,**kwargs):
        context = super(GlobalAddView, self).get_context_data()
        context["form_title"] = self.model_obj.form_title % "Yeni"
        context["title"] = self.model_obj.form_title % "Yeni"
        context["field_list"] = self.field_list
        context["m_name"] = self.model_obj.name
        context["list_title"] = self.model_obj.list_title
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        if hasattr(self.object,"user"):
            if "user" in form.cleaned_data:
                if form.cleaned_data["user"]==None:
                    self.object.user = self.request.user
            else:
                self.object.user=self.request.user
            self.object.save()
        else:
            self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return form_redirection(self.request).url

    def get_initial(self):
        initial_dict = super(GlobalAddView, self).get_initial()
        for item in self.request.GET:
            initial_dict[item] = self.request.GET.get(item)
        return initial_dict
    
    def get_form(self, form_class=None):
        form = super(GlobalAddView, self).get_form(form_class)
        for f_name,form_field in form.fields.items():
            form_field.widget.attrs["class"]="form-control"
            if "date" in f_name:
                form_field.widget.attrs["data-toggle"]="datetimepicker"
                form_field.widget.attrs["data-target"]="#id_"+f_name
                form_field.widget.attrs["class"]+=" datetimepicker date"
            elif "time" in f_name:
                form_field.widget.attrs["data-toggle"]="datetimepicker"
                form_field.widget.attrs["data-target"]="#id_"+f_name
                form_field.widget.attrs["class"]+=" datetimepicker time"
        return form

class GlobalUpdateView(UpdateView):
    template_name = "global_form.html"
    ability = "Update"
    model_obj=None
    fields = []
    field_list=None
    
    def get_queryset(self):
        self.model_obj, self.model = af.get_model(self.kwargs["m_name"])
        self.field_list= af.get_fields(self.model_obj, self.ability)
        self.fields = [field.name for field in self.field_list]
        if "user" in self.fields:
            object_list = self.model.objects.filter(user=self.request.user)
        else:
            object_list = self.model.objects.all()
        return object_list
    
    def get_context_data(self, **kwargs):
        context = super(GlobalUpdateView, self).get_context_data()
        context["form_title"] = self.model_obj.form_title % self.object
        context["title"] = self.model_obj.form_title % self.object
        context["field_list"] = self.field_list
        context["m_name"] = self.model_obj.name
        context["list_title"] = self.model_obj.list_title
        return context
    
    def form_valid(self, form):
        if hasattr(self.object,"user"):
            if self.request.user==self.object.user:
                self.object = form.save()
                return super().form_valid(form)
            else:
                return redirect("global_update",m_name=self.model_obj.name,pk=self.object.id)
        else:
            self.object = form.save()
            return super().form_valid(form)

    def get_success_url(self):
        return form_redirection(self.request).url
    
    def get_form(self, form_class=None):
        form = super(GlobalUpdateView, self).get_form(form_class)
        for f_name,form_field in form.fields.items():
            form_field.widget.attrs["class"]="form-control"
            if "date" in f_name:
                form_field.widget.attrs["data-toggle"]="datetimepicker"
                form_field.widget.attrs["data-target"]="#id_"+f_name
                form_field.widget.attrs["class"]+=" datetimepicker date"
            elif "time" in f_name:
                form_field.widget.attrs["data-toggle"]="datetimepicker"
                form_field.widget.attrs["data-target"]="#id_"+f_name
                form_field.widget.attrs["class"]+=" datetimepicker time"
        return form

class GlobalDeleteView(DeleteView):
    template_name = "global_delete.html"
    ability = "Delete"
    model_obj=None
    
    def get_queryset(self):
        self.model_obj, self.model = af.get_model(self.kwargs["m_name"])
        object_list = self.model.objects.all()
        return object_list
    
    def get_context_data(self, **kwargs):
        context = super(GlobalDeleteView, self).get_context_data()
        context["delete_title"] = self.model_obj.form_title % self.object
        context["title"] = self.model_obj.form_title % self.object
        context["m_name"] = self.model_obj.name
        return context

    def get_success_url(self):
        return form_redirection(self.request).url

class GlobalListView(ListView):
    template_name = "global_list.html"
    paginate_by = 50
    ability = "List"
    model_obj=None
    fields = []
    
    def get_extras(self):
        extra_dict={}
        for item in self.request.GET:
            extra_dict[item]=self.request.GET[item]
        return extra_dict
        
    def get_filter(self):
        extra_dict=self.get_extras()
        if "page" in extra_dict:
            del extra_dict["page"]
        return extra_dict
    
    def get_queryset(self):
        self.model_obj, self.model = af.get_model(self.kwargs["m_name"])
        object_list = af.get_queryset(self.request.user, self.model_obj.name,filter_dict=self.get_filter())
        return object_list
    
    def get_fields(self):
        return af.get_fields(self.model_obj, self.ability)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GlobalListView, self).get_context_data()
        context["m_name"] = self.model_obj.name
        context["title"] = self.model_obj.list_title
        context["fields"] = self.get_fields()
        return context

class GlobalDetailView(DetailView):
    template_name = "global_detail.html"
    ability = "Detail"
    model_obj = None
    fields = []
    
    def get_queryset(self):
        self.model_obj, self.model = af.get_model(self.kwargs["m_name"])
        object_list = self.model.objects.all()
        return object_list
    
    def get_fields(self):
        return af.get_fields(self.model_obj, self.ability)
    
    def get_context_data(self, **kwargs):
        context = super(GlobalDetailView, self).get_context_data()
        context["title"] = self.model_obj.detail_title % self.object
        context["m_name"] = self.model_obj.name
        context["list_title"] = self.model_obj.list_title
        context["fields"] = self.get_fields()
        return context
    
class MyLoginView(LoginView):
    def form_valid(self, form):
        ip=self.request.META["REMOTE_ADDR"]
        model_obj,model=af.get_model("UserIp")
        obj_list=model.objects.filter(ip=ip)
        if len(obj_list)>0:
            return super(MyLoginView, self).form_valid(form)
        else:
            return redirect("/?warning=unauthorizated_ip_login")
