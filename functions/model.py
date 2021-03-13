# -*- coding: utf-8 -*-
from django.apps import apps
from functions.auth_func import ModelFunc,ModelQueryset
from django.shortcuts import redirect
from operator import attrgetter as atg


class AttrDict(ModelFunc):
    def __init__(self,object):
        super(AttrDict, self).__init__()
        self.m_name=object.__class__.__name__
        self.model_obj=self.get_model_obj(self.m_name)
        self.model=self.get_model(self.model_obj)
        self.object=object

    def get_attr_dict(self,type):
        attr_dict={}
        for field in self.get_model_fields(self.model_obj,type):
            attr_dict[field.name]=getattr(self.object,field.name)
        return attr_dict

    def get_remote_attr_dict(self):
        remote_attr_dict={}
        field_model=apps.get_model("main","FieldLM")
        remote_model_list=[field for field in field_model.objects.filter(to=self.model_obj.name)]
        for field in remote_model_list:
            remote_attr_dict[field]=[value for value in getattr(self.object,"%s_set" % field.model.name.lower()).all()][:10]
        return remote_attr_dict

class PageManagement(ModelFunc):
    current_href=""
    base_href=""
    
    def __init__(self,request):
        super(PageManagement, self).__init__()
        self.request=request
        self.current_href=self.request.META["PATH_INFO"]
        self.m_name=request.resolver_match.kwargs["m_name"]
        self.ability=self.get_ability()
        self.model=self.get_model(self.m_name)
        self.parameter_dict=self.get_parameter_dict()
        self.current_id=self.get_current_id()
        self.object_list=self.get_object_list()
        
    def get_object_list(self):
        mq=ModelQueryset(self.request)
        return mq.get_queryset(self.m_name)
    
    def get_ability(self):
        if "list" in self.current_href:
            return "List"
        elif "detail" in self.current_href:
            return "Detail"
        elif "update" in self.current_href:
            return "Update"
        elif "delete" in self.current_href:
            return "Delete"
        elif "add" in self.current_href:
            return "Add"
        else:
            return None
        
    def get_search_data(self):
        if "search" in self.request.GET:
            return self.request.GET["search"]
        else:
            return ""
        
    def get_parameter_dict(self):
        parameter_dict={}
        for key in self.request.GET:
            parameter_dict[key]=self.request.GET[key]
        return parameter_dict
        
        
    def get_current_id(self):
        if "Detail" == self.ability or "Update" == self.ability or "Delete" == self.ability:
            return int(self.current_href.split("/")[3])
        elif "List"==self.ability:
            if "page" in self.parameter_dict:
                page_no=int(self.parameter_dict["page"])
                del self.parameter_dict["page"]
                return page_no
            else:
                return 1
        else:
            return None
    
    def get_detail_index_stats(self):
        obj_list=sorted(self.object_list,key=atg("id"))
        if len(obj_list)!=0:
            last=obj_list[-1].id
            first=obj_list[0].id
            if last==self.current_id:
                next=last
            else:
                next=self.go_up(self.model,self.current_id+1,last)
            if first==self.current_id:
                prev=self.current_id
            else:
                prev=self.go_down(self.model,self.current_id-1,last)
            return first,prev,next,last
        return 0,0,0,0
            
    def go_up(self,model,pk,last):
        if self.object_list.filter(id=pk).exists() or pk==last:
            return pk
        else:
            return self.go_up(model,pk+1,last)
        
    def go_down(self,model,pk,last):
        if self.object_list.filter(id=pk).exists() or pk==last:
            return pk
        else:
            return self.go_down(model,pk-1,last)
    
    def get_detail_page(self):
        first,prev,next,last=self.get_detail_index_stats()
        page_info = []
        page_info.append("/detail/%s/%d" % (self.m_name, first))
        page_info.append("/detail/%s/%d" % (self.m_name, prev))
        page_info.append(self.current_id)
        page_info.append("/detail/%s/%d" % (self.m_name, next))
        page_info.append("/detail/%s/%d" % (self.m_name, last))
        return page_info
        
    def get_list_index_stats(self):
        total=len(self.object_list)
        last=int(total//50)+1
        first=1
        return first,last
        
    def get_list_page(self):
        first,last=self.get_list_index_stats()
        parameters=""
        for key, value in self.parameter_dict.items():
            parameters+="&%s=%s" % (str(key), str(value))
        page_info=[]
        if first!=self.current_id:
            page_info.append(("/list/%s/?page=%d%s" % (self.m_name,first,parameters),first,"İlk"))
        if first<self.current_id-3:
            page_info.append(("/list/%s/?page=%d%s" % (self.m_name,self.current_id-3,parameters),self.current_id-3,self.current_id-3))
        if first<self.current_id-2:
            page_info.append(("/list/%s/?page=%d%s" % (self.m_name,self.current_id-2,parameters),self.current_id-2,self.current_id-2))
        if first<self.current_id-1:
            page_info.append(("/list/%s/?page=%d%s" % (self.m_name,self.current_id-1,parameters),self.current_id-1,self.current_id-1))
        if first<=self.current_id and self.current_id<=last:
            page_info.append(("#",self.current_id,self.current_id))
        if self.current_id+1<last:
            page_info.append(("/list/%s/?page=%d%s" % (self.m_name,self.current_id+1,parameters), self.current_id + 1, self.current_id + 1))
        if self.current_id+2<last:
            page_info.append(("/list/%s/?page=%d%s" % (self.m_name,self.current_id+2,parameters), self.current_id + 2, self.current_id + 2))
        if self.current_id+3<last:
            page_info.append(("/list/%s/?page=%d%s" % (self.m_name,self.current_id+3,parameters), self.current_id + 3, self.current_id + 3))
        if self.current_id!=last:
            page_info.append(("/list/%s/?page=%d%s" % (self.m_name,last,parameters), last,"Son"))
        return page_info
    
    def get_page(self):
        if "Detail" == self.ability or "Update" == self.ability or "Delete" == self.ability:
            return self.get_detail_page()
        elif self.ability=="List":
            return self.get_list_page()
        else:
            return redirect("global_detail",m_name=self.m_name)