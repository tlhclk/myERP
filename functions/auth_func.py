# -*- coding: utf-8 -*-
from django.apps import apps
from django.db.models import Q
import operator
import datetime as dt

def get_fields(model_obj,ability):
    ability_dict={"List":"show_list","Detail":"show_detail","Add":"form_add","Update":"form_update","Delete":"form_delete"}
    field_list=[]
    field_model=apps.get_model("main","FieldLM")
    for field in field_model.objects.filter(model=model_obj):
        if ability=="All":
            field_list.append(field)
        else:
            if getattr(field,ability_dict[ability]):
                field_list.append(field)
    field_list=sorted(field_list,key=operator.attrgetter("order"))
    return field_list

def get_model(m_name):
    model_model=apps.get_model("main","ModelLM")
    model_obj_list = model_model.objects.filter(name=m_name)
    if len(model_obj_list)==0:
        return None, None
    else:
        model_obj=model_obj_list[0]
        model = apps.get_model(model_obj.panel.name,model_obj.name)
        return model_obj,model

def get_perm_filter(user,model_obj):
    perm_model = apps.get_model("authentication", "UserPermission")
    perm_lvl = {"Delete": 5, "Update": 4, "Add": 3, "Detail": 2, "List": 1}
    us_perm_list = perm_model.objects.filter(personal_permission__model=model_obj).filter(user_name=user)
    if len(us_perm_list)>0:
        user_list=[user]
        for us_perm in us_perm_list:
            if us_perm.personal_permission.user_name not in user_list:
                user_list.append(us_perm.personal_permission.user_name)
        return user_list
    else:
        user_list=[user]
        return user_list

def get_search_filter_dict(search_text,model_obj):
    field_dict={}
    field_list = get_fields(model_obj,"Detail")
    for field in field_list:
        if field.field=="CharField":
            field_dict["%s__icontains" % field.name]=search_text
        elif field.field=="EmailField":
            field_dict["%s__icontains" % field.name]=search_text
        elif field.field=="ForeignKey":
            if field.to!="User":
                field_list2=get_fields(get_model(field.to)[0],"Detail")
                for field2 in field_list2:
                    if field2.field == "CharField":
                        field_dict["%s__%s__icontains" % (field.name,field2.name)] = search_text
                    elif field2.field == "EmailField":
                        field_dict["%s__%s__icontains" % (field.name,field2.name)] = search_text
    return field_dict

def get_field_filter_dict(field,value):
    if type(field)==str:
        if "id" ==field:
            return Q(("id",int(value)))
        if "_id" in field:
            return Q((field,int(value)))
        else:
            return Q((field,value))
    else:
        if field.field=="CharField":
            return Q(("%s__icontains" % field.name,value))
        elif field.field=="EmailField":
            return Q(("%s__icontains" % field.name,value))
        elif field.field=="BooleanField":
            if value.lower()=="true" or value=="1":
                return Q((field.name,True))
            elif value.lower()=="false" or value=="0":
                return Q((field.name,False))
        elif field.field=="DateField":
            ymd_list=value.split("-")
            if len(ymd_list)==3:
                year,month,day=ymd_list
                date=dt.date(int(year),int(month),int(day))
                return Q((field.name,date))
        elif field.field=="TimeField":
            hm_list=value.split(":")
            if len(hm_list)==2:
                hour,minutes=hm_list
                time=dt.time(int(hour),int(minutes))
                return Q((field.name,time))
        elif field.field=="ForeignKey":
            if field.to!="User":
                field_list2=get_fields(get_model(field.to)[0],"Detail")
                temp_q=Q()
                for field2 in field_list2:
                    if field2.field == "CharField":
                        temp_q|=Q(("%s__%s__icontains" % (field.name,field2.name),value))
                    elif field2.field == "EmailField":
                        temp_q|=Q(("%s__%s__icontains" % (field.name,field2.name),value))
                return temp_q

def get_filter(model_obj,model,user,filter_dict,exclude_dict):
    search_filter_dict={}
    if filter_dict!=None:
        if "search" in filter_dict:
            search_filter_dict=get_search_filter_dict(filter_dict["search"],model_obj)
    user_filter = Q()
    if hasattr(model,"user"):
        user_list=get_perm_filter(user,model_obj)
        for us in user_list:
            user_filter|=Q(("user_id",us.id))
    filter_q_or = Q()
    filter_q_and = Q()
    exclude_q = Q()
    for key,value in search_filter_dict.items():
        filter_q_or|=Q((key,value))
    if filter_dict!=None:
        for key2,value2 in filter_dict.items():
            if key2!="search":
                filter_q_and = filter_q_and & get_field_filter_dict(key2,value2)
    if exclude_dict != None:
        for key3,value3 in exclude_dict.items():
            exclude_q|=Q((key3,value3))
    return user_filter,filter_q_and,filter_q_or,exclude_q
    
def get_queryset(user,m_name,filter_dict=None,exclude_dict=None):
    model_obj,model = get_model(m_name)
    user_filter,filter_q_and,filter_q_or,exclude_q=get_filter(model_obj,model,user,filter_dict,exclude_dict)
    object_list=model.objects.all()
    if user.is_superuser == True:
        return object_list
    if len(user_filter)!=0:
        object_list=object_list.filter(user_filter)
    if len(filter_q_and)!=0:
        object_list=object_list.filter(filter_q_and)
    if len(filter_q_or)!=0:
        object_list=object_list.filter(filter_q_or)
    if len(exclude_q)!=0:
        object_list=object_list.exclude(exclude_q)
    return object_list
    
