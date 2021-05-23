# -*- coding: utf-8 -*-
from main.models import ModelLM,PathLM
from authentication.models import MyUserProfile

class HomeData:
    def __init__(self,request):
        self.user=request.user
        
    def get_context_data(self):
        context_data={}
        context_data["title"]="Ana Sayfa"
        context_data["profile_pic_path"]=self.get_profile_pic_path()
        return context_data
        
    def get_profile_pic_path(self):
        if not self.user.is_anonymous:
            profile_list=MyUserProfile.objects.filter(user_name=self.user)
            if len(profile_list)>0:
                return profile_list[0].profile_pic
        return ""
        
    def get_model_list_path(self):
        path_dict={}
        model_list=ModelLM.objects.all()
        for model in model_list:
            if model.panel not in path_dict:
                path_dict[model.panel]=[model]
            else:
                path_dict[model.panel].append(model)
        return path_dict
    
    def get_func_list_path(self):
        path_list=PathLM.objects.filter(type="function")
        return path_list
    
    def get_report_list_path(self):
        path_list=PathLM.objects.filter(type="report")
        return path_list
