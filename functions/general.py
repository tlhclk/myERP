# -*- coding: utf-8 -*-
from main.models import *


class HomeData:
    def get_context_data(self):
        context_data={}
        context_data["title"]="Ana Sayfa"
        return context_data

    def get_model_list_path(self):
        panel_list=PanelLM.objects.filter(type="panel")
        model_list=ModelLM.objects.all()
        path_dict={}
        for panel in panel_list:
            path_dict[panel]=[]
        for model in model_list:
            path_dict[model.panel].append(model)
        return path_dict
    
    def get_func_list_path(self):
        func_list=PathLM.objects.filter(type="function")
        return func_list
    
    def get_report_list_path(self):
        rep_list=PathLM.objects.filter(type="report")
        return rep_list