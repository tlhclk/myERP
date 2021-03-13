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
        self.user_perm_model = apps.get_model("authentication", "UserPermission")
        
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

class PermissionControl(ModelFunc):
    def __init__(self):
        super(PermissionControl, self).__init__()
        self.panel_perm_model = apps.get_model("authentication", "PanelPermission")
        self.model_perm_model = apps.get_model("authentication", "ModelPermission")
        self.path_perm_model = apps.get_model("authentication", "PathPermission")
        self.group_model = apps.get_model("authentication", "MyGroup")
        self.user_group_model = apps.get_model("authentication", "UserGroup")
        self.user_profile_model = apps.get_model("authentication", "MyUserProfile")
    
    def PanelCheck(self,user,panel_obj):
        if type(panel_obj)==str:
            panel_obj=self.get_panel(panel_obj)
        if type(panel_obj)==self.panel_model:
            perm_list=self.panel_perm_model.objects.filter(user_name=user).filter(panel=panel_obj)
            if len(perm_list)==1:
                perm=perm_list[0]
                if perm.permission==True:
                    return True
                else:
                    print("Panel Yetki Yok %s" % perm)
            else:
                print("Panel Yetkisi Bulunamadı %s" % panel_obj )
        else:
            print("Panel Bulunamadı(PanelCheck) %s" % panel_obj)
        return False
    
    def ModelCheck(self,user,model_obj):
        if type(model_obj)==str:
            model_obj=self.get_model(model_obj)
        if type(model_obj)==self.model_model:
            perm_list=self.model_perm_model.objects.filter(user_name=user).filter(model=model_obj)
            if len(perm_list)==1:
                perm=perm_list[0]
                if perm.permission==True:
                    return True
                else:
                    print("Model Yetki Yok %s" % perm)
            else:
                print("Model Yetkisi Bulunamadı %s" % model_obj)
        else:
            print("Model Bulunamadı %s" % model_obj)
        return False
    
    def PathCheck(self,user,path_obj):
        if type(path_obj)==str:
            path_obj=self.get_path(path_obj)
        if type(path_obj)==self.path_model:
            perm_list=self.path_perm_model.objects.filter(user_name=user).filter(path=path_obj)
            if len(perm_list)==1:
                perm=perm_list[0]
                if perm.permission==True:
                    return True
                else:
                    print("Güzergah Yetki Yok %s" % perm)
            else:
                print("Güzergah Yetkisi Bulunamadı %s" % path_obj)
        else:
            print("Güzergah Bulunamadı %s" % path_obj)
        return False
    
    def GroupCheck(self,user,group_obj):
        if type(group_obj)==str:
            group_obj=self.get_group_obj(group_obj,self.get_user_corporation(user))
        if type(group_obj)==self.group_model:
            perm_list=self.user_group_model.objects.filter(user_name=user).filter(group=group_obj)
            if len(perm_list)>0:
                return True
            else:
                print("Group Yetki Yok %s" % group_obj)
        else:
            print("Grup Bulunamadı(GroupCheck) %s" % group_obj)
        return False
    
    def get_group_obj(self,g_name,corporation):
        if type(g_name)==str:
            group_list=self.group_model.objects.filter(name=g_name).filter(corporation=corporation)
            if len(group_list)==1:
                return group_list[0]
        print("Grup Bulunamadı(Group Obj) %s" % g_name)
        return None
    
    def get_user_corporation(self,user):
        profile_list=self.user_profile_model.objects.filter(user_name=user)
        if len(profile_list)==1:
            profile=profile_list[0]
            return profile.corporation
        print("Profil Bulunamadı %s" % user)
        return None
    
class ModelQueryset(ModelFunc):
    def __init__(self,request):
        super(ModelQueryset, self).__init__()
        self.request=request
        self.user=request.user
        self.url_name=request.resolver_match.url_name
        self.get_kwargs(request.resolver_match.kwargs)
        self.extra_dict=self.get_extra_dict()
    
    def get_model_info(self,m_name):
        self.model_obj=self.get_model_obj(m_name)
        self.model=self.get_model(self.model_obj)
        self.field_list = self.get_model_fields(self.model_obj, "All")
        
    def get_extra_dict(self):
        extra_dict={}
        for key in self.request.GET:
            if key!="page":
                extra_dict[key]=self.request.GET[key]
        return extra_dict
    
    def get_kwargs(self,kwargs_dict):
        for key,value in kwargs_dict.items():
            setattr(self,key,value)
            
    def get_user_perm_filter_list(self):
        user_perm_list = self.user_perm_model.objects.filter(model_permission__model=self.model_obj).filter(user_name=self.user)
        user_list = [self.user]
        if len(user_perm_list)> 0:
            for user_perm in user_perm_list:
                if user_perm.permission==True:
                    if user_perm.model_permission.user_name not in user_list:
                        user_list.append(user_perm.model_permission.user_name)
                    else:
                        print("%s yetki mevcut" % user_perm)
                else:
                    print("%s yetkisi iptal" % user_perm)
        return user_list
    
    def get_search_filter_dict(self):
        filter_dict = {}
        if "search" in self.extra_dict:
            search_text=self.extra_dict["search"]
            field_list = self.get_model_fields(self.model_obj, "Detail")
            for field in field_list:
                if field.field == "CharField":
                    filter_dict["%s__icontains" % field.name] = search_text
                elif field.field == "EmailField":
                    filter_dict["%s__icontains" % field.name] = search_text
                elif field.field == "ForeignKey":
                    if field.to != "User":
                        field_list2 = self.get_model_fields(field.to,"All")
                        for field2 in field_list2:
                            if field2.field == "CharField":
                                filter_dict["%s__%s__icontains" % (field.name, field2.name)] = search_text
                            elif field2.field == "EmailField":
                                filter_dict["%s__%s__icontains" % (field.name, field2.name)] = search_text
        return filter_dict
    
    def get_field_filter_dict(self):
        filter_dict={}
        for field in self.field_list:
            if field.name in self.extra_dict:
                key,value= self.get_field_filter_data(field,self.extra_dict[field.name])
                filter_dict[key]=value
        for key in self.extra_dict:
            if key[-3:]=="_id":
                filter_dict[key]=int(self.extra_dict[key])
        return filter_dict
    
    def get_field_filter_data(self,field,value):
        if field.field=="CharField":
            return ("%s__icontains" % field.name,value)
        elif field.field=="EmailField":
            return ("%s__icontains" % field.name,value)
        elif field.field=="BooleanField":
            if value.lower()=="true" or value=="1":
                return (field.name,True)
            elif value.lower()=="false" or value=="0":
                return (field.name,False)
        elif field.field=="DateField":
            ymd_list=value.split("-")
            if len(ymd_list)==3:
                year,month,day=ymd_list
                date=dt.date(int(year),int(month),int(day))
                return (field.name,date)
        elif field.field=="TimeField":
            hm_list=value.split(":")
            if len(hm_list)==2:
                hour,minutes=hm_list
                time=dt.time(int(hour),int(minutes))
                return (field.name,time)
        elif field.field=="ForeignKey":
            if field.to!="User":
                field_list2=self.get_model_fields(self.get_model_obj(field.to),"Detail")
                filter_list=[]
                for field2 in field_list2:
                    if field2.field == "CharField":
                        filter_list.append(("%s__%s__icontains" % (field.name,field2.name),value))
                    elif field2.field == "EmailField":
                        filter_list.append(("%s__%s__icontains" % (field.name,field2.name),value))
                return "%s__list"%field.name,filter_list
        return None
    
    def get_filter(self,filter_dict,exclude_dict):
        ufor=Q()
        fdand=Q()
        edor=Q()
        sfor=Q()
        ffand=Q()
        if hasattr(self.model,"user"):
            for user in self.get_user_perm_filter_list():
                ufor|=Q(("user",user))
        if self.url_name=="global_list":
            for key,value in filter_dict.items():
                fdand&=Q((key,value))
            for key,value in exclude_dict.items():
                edor|=Q((key,value))
            for key,value in self.get_search_filter_dict().items():
                sfor|=Q((key,value))
            for key,value in self.get_field_filter_dict().items():
                if "__list" == key[-6:]:
                    temp_q=Q()
                    for key2,value2 in value:
                        temp_q|=Q((key2,value2))
                    ffand&=temp_q
                else:
                    ffand&=Q((key,value))
        return fdand,edor,ufor,sfor,ffand
    
    def get_queryset(self,m_name,fd={},ed={}):
        self.get_model_info(m_name)
        fl=[field.name for field in self.field_list]
        filter_dict={}
        for key in fd:
            if key not in fl:
                filter_dict[key]=fd[key]
        fdand,edor,ufor,sfor,ffand=self.get_filter(filter_dict=filter_dict,exclude_dict=ed)
        object_list=self.model.objects.all()
        if self.user.is_superuser == True or PermissionControl().GroupCheck(self.user,"Admin"):
            return object_list
        if len(ufor)!=0:
            object_list=object_list.filter(ufor)
        if len(fdand)!=0:
            object_list=object_list.filter(fdand)
        if len(sfor)!=0:
            object_list=object_list.filter(sfor)
        if len(ffand)!=0:
            object_list=object_list.filter(ffand)
        if len(edor)!=0:
            object_list=object_list.exclude(edor)
        return object_list
