# -*- coding: utf-8 -*-
from main.models import ModelLM,PathLM


class HomeData:
    def get_context_data(self):
        context_data={}
        context_data["title"]="Ana Sayfa"
        return context_data
        
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
 