# -*- coding: utf-8 -*-
from django.apps import apps
from django.db.models import Q
import operator
import datetime as dt


class ModelFunc:
    def __init__(self):
        self.panel_model=apps.get_model("main","PanelLM")
        self.model_model=apps.get_model("main","ModelLM")
        self.field_model=apps.get_model("main","FieldLM")
        self.path_model=apps.get_model("main","PathLM")
        
    def get_model_fields(self,model_obj,ability):
        field_list = []
        if type(model_obj)==str:
            model_obj=self.get_model_obj(model_obj)
        if type(model_obj)==self.model_model:
            ability_dict = {"List": "show_list", "Detail": "show_detail", "Add": "form_add", "Update": "form_update",
                            "Delete": "form_delete"}
            for field in self.field_model.objects.filter(model=model_obj):
                if ability == "All":
                    field_list.append(field)
                else:
                    if getattr(field, ability_dict[ability]):
                        field_list.append(field)
            field_list = sorted(field_list, key=operator.attrgetter("order"))
        else:
            print("Model Objesi Bulunamadı(Field) %s" % model_obj)
        return field_list
    
    def get_model_obj(self,m_name):
        if type(m_name)==str:
            model_obj_list = self.model_model.objects.filter(name=m_name)
            if len(model_obj_list)==1:
                return model_obj_list[0]
        print("Model Objesi Bulunamadı(Model Obj) %s" % m_name)
        return None
    
    def get_model(self,model_obj):
        if type(model_obj)==str:
            model_obj=self.get_model_obj(model_obj)
        if type(model_obj)==self.model_model:
            return apps.get_model(model_obj.panel.name, model_obj.name)
        else:
            print("Model Objesi Bulunamadı(Model) %s" % model_obj)
        return None
    
    def get_panel(self,p_name):
        if type(p_name)==str:
            panel_obj_list = self.panel_model.objects.filter(name=p_name)
            if len(panel_obj_list)==1:
                return panel_obj_list[0]
        print("Panel Bulunamadı %s" % p_name)
        return None
    
    def get_path(self,p_name):
        if type(p_name)==str:
            path_obj_list = self.path_model.objects.filter(name=p_name)
            if len(path_obj_list)==1:
                return path_obj_list[0]
        print("Güzergah Bulunamadı %s" % p_name)
        return None

  
class ModelQueryset(ModelFunc):
    def __init__(self, request):
        super(ModelQueryset, self).__init__()
        self.request = request
        self.user = request.user
        self.url_name = request.resolver_match.url_name
        self.search_text = ""
        self.get_kwargs(request.resolver_match.kwargs)
        self.extra_dict = self.get_extra_dict()

    def get_model_info(self, m_name):
        self.model_obj = self.get_model_obj(m_name)
        self.model = self.get_model(self.model_obj)
        self.field_list = self.get_model_fields(self.model_obj, "All")

    def get_extra_dict(self):
        extra_dict = {}
        for key in self.request.GET:
            if key != "page":
                if key == "search":
                    self.search_text = self.request.GET[key]
                else:
                    extra_dict[key] = self.request.GET[key]
        return extra_dict

    def get_kwargs(self, kwargs_dict):
        for key, value in kwargs_dict.items():
            setattr(self, key, value)

    def get_field_data(self, ftype, f1, value, f2=None):
        key_str = None
        value_str = None
        if f2:
            f1 = "%s__%s" % (f1, f2)
        if ftype == "CharField" or ftype == "EmailField":
            key_str = "%s__%s" % (f1, "icontains")
            value_str = value
        elif ftype == "BooleanField":
            key_str = "%s" % f1
            if value.lower() == "true" or value == "1":
                value_str = True
            elif value.lower() == "false" or value == "0":
                value_str = False
        elif ftype == "DateField":
            key_str = "%s" % f1
            ymd_list = value.split("-")
            try:
                year, month, day = ymd_list
                date = dt.date(int(year), int(month), int(day))
                value_str = date
            except ValueError:
                pass
        elif ftype == "TimeField":
            key_str = "%s" % f1
            hm_list = value.split(":")
            try:
                hour, minutes = hm_list
                time = dt.time(int(hour), int(minutes))
                value_str = time
            except ValueError:
                pass
        elif ftype == "id":
            key_str = "%s_id" % f1
            value_str = int(value)
        return (key_str, value_str)

    def get_search_filter_data(self):
        sfor = Q()
        for field in self.field_list:
            if field.field == "ForeignKey":
                field_list2 = self.get_model_fields(field.to, "All")
                for field2 in field_list2:
                    key, value = self.get_field_data(field2.field, field.name, self.search_text, field2.name)
                    if key != None and value != None:
                        sfor |= Q((key, value))
            else:
                key, value = self.get_field_data(field.field, field.name, self.search_text)
                if key != None and value != None:
                    sfor |= Q((key, value))
        return sfor

    def get_field_filter_data(self):
        ffand = Q()
        for field in self.field_list:
            if field.name in self.extra_dict or "%s_id" % field.name in self.extra_dict:
                if "%s_id" % field.name in self.extra_dict:
                    key, value = self.get_field_data("id", field.name, self.extra_dict["%s_id" % field.name])
                    if key != None and value != None:
                        ffand &= Q((key, value))
                else:
                    if field.field == "ForeignKey":
                        field_list2 = self.get_model_fields(field.to, "All")
                        for field2 in field_list2:
                            key, value = self.get_field_data(field2.field, field.name, self.extra_dict[field.name],
                                                             field2.name)
                            if key != None and value != None:
                                ffand |= Q((key, value))
                    else:
                        key, value = self.get_field_data(field.field, field.name, self.extra_dict[field.name])
                        if key != None and value != None:
                            ffand |= Q((key, value))
        return ffand

    def get_filter_data(self, filter_dict):
        fdand = Q()
        for key, value in filter_dict.items():
            fdand &= Q((key, value))
        return fdand

    def get_exclude_data(self, exclude_dict):
        edor = Q()
        for key, value in exclude_dict.items():
            edor |= Q((key, value))

    def get_queryset(self, m_name, fd={}, ed={}):
        self.get_model_info(m_name)
        object_list = self.model.objects.all()
        for key, value in fd:
            self.extra_dict[key] = value
        if len(self.extra_dict) > 0:
            if self.search_text != "":
                ffand = self.get_field_filter_data()
                object_list = object_list.filter(ffand)

                sfor = self.get_search_filter_data()
                object_list = object_list.filter(sfor)
            else:
                ffand = self.get_field_filter_data()
                object_list = object_list.filter(ffand)
        else:
            if self.search_text != "":
                sfor = self.get_search_filter_data()
                object_list = self.model.objects.filter(sfor)
        if len(ed) > 0:
            edor = self.get_exclude_data(ed)
            object_list = object_list.exclude(edor)

        return object_list