# -*- coding: utf-8 -*-
from main.models import *
from authentication.models import *
from django.db.models import Q


class HomeData:
    def __init__(self,request):
        #self.request=request
        self.user=request.user
        
    def get_user_perms(self,user):
        return None
    
    def get_context_data(self):
        context_data={}
        context_data["title"]="Ana Sayfa"
        return context_data
    
    def get_filter_q(self):
        filter_q=Q()
        filter_q|=Q(("user_name_id",self.user.id))
        group_list=UserGroup.objects.filter(user_name=self.user)
        for ug in group_list:
            filter_q|=Q(("group_id",ug.group.id))
        return filter_q
        
    def get_model_list_path(self):
        path_dict={}
        filter_q=self.get_filter_q()
        valid_panel_list=PanelPermission.objects.filter(panel__type="panel").filter(filter_q)
        for panel_perm in valid_panel_list:
            valid_model_list=ModelPermission.objects.filter(model__panel=panel_perm.panel).filter(filter_q)
            path_dict[panel_perm.panel]=[]
            for model_perm in valid_model_list:
                if model_perm.model not in path_dict[panel_perm.panel]:
                    path_dict[panel_perm.panel].append(model_perm.model)
        return path_dict
    
    def get_func_list_path(self):
        func_list=[]
        filter_q=self.get_filter_q()
        valid_path_list=PathPermission.objects.filter(path__type="function").filter(filter_q)
        for path_perm in valid_path_list:
            func_list.append(path_perm.path)
        return func_list
    
    def get_report_list_path(self):
        rep_list=[]
        filter_q=self.get_filter_q()
        valid_path_list=PathPermission.objects.filter(path__type="report").filter(filter_q)
        for path_perm in valid_path_list:
            rep_list.append(path_perm.path)
        return rep_list
    
    def get_sidebar_data(self):
        panel_list_by_user=PanelPermission.objects.filter(panel__type="panel").filter(user_name=self.user)
        group_list=UserGroup.objects.filter(user_name=self.user)
        panel_list_by_group=[]
        for ug in group_list:
            panel_list_by_group+=list(PanelPermission.objects.filter(panel__type="panel").filter(group=ug.group))
        model_list_by_user=ModelPermission.objects.filter()
        modell_list_by_group=ModelPermission
        func_list_by_user=PathPermission.objects.filter(path__type="function")
        report_list_by_user=PathPermission.objects.filter(path__type="report")
        path_list_by_group=PathPermission