# -*- coding: utf-8 -*-
from functions.general import HomeData
from django import template
from series.models import Series
import functions.model as mdl

register = template.Library()


### template support functions
@register.filter(name='get_attr_value')
def get_attr_value(obj,field):
    attr_dict=obj.attr_dict("Detail")
    if field.to=="" or field.to==None:
        return attr_dict[field.name]
    return attr_dict[field.name]

@register.simple_tag
def get_attr_value2(obj,field,ability,key=""):
    attr_dict=obj.attr_dict(ability)
    if key!="" and attr_dict[field.name]!=None:
        return getattr(attr_dict[field.name],key)
    return attr_dict[field.name]

@register.inclusion_tag("sidebar.html")
def get_sidebar():
    hd=HomeData()
    sidebar_dict=hd.get_model_list_path()
    func_list=hd.get_func_list_path()
    rep_list=hd.get_report_list_path()
    return {"sidebar_dict":sidebar_dict,"func_list":func_list,"rep_list":rep_list}

@register.inclusion_tag("page_list.html")
def get_page_list(request):
    pm=mdl.PageManagement(request)
    return {"page_info":pm.get_page(),"ability":pm.ability}

@register.simple_tag
def dict_value(dict,key):
    return dict[key]

@register.inclusion_tag("series/series_box.html")
def get_series_list(state):
    series_list=Series.objects.filter(state=state)
    return {"state":state,"s_object_list":series_list}
