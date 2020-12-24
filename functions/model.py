# -*- coding: utf-8 -*-
from .form_after import *
import functions.auth_func as af
from django.shortcuts import redirect
from operator import attrgetter as atg


class AttrDict:
    def __init__(self,object):
        self.m_name=object.__class__.__name__
        self.model_obj,self.model=af.get_model(self.m_name)
        self.object=object

    def get_attr_dict(self,type):
        attr_dict={}
        for field in af.get_fields(self.model_obj,type):
            attr_dict[field.name]=getattr(self.object,field.name)
        return attr_dict

    def get_remote_attr_dict(self):
        remote_attr_dict={}
        field_model=apps.get_model("main","FieldLM")
        remote_model_list=[field for field in field_model.objects.filter(to=self.model_obj.name)]
        for field in remote_model_list:
            remote_attr_dict[field]=[value for value in getattr(self.object,"%s_set" % field.model.name.lower()).all()][-10:]
        return remote_attr_dict

class PageManagement:
    current_href=""
    base_href=""
    cur=1
    first=1
    last=0
    prev=0
    next=0
    ability = None
    direction = None
    search = None
    
    def __init__(self,request):
        self.request=request
        self.current_href=self.request.META["PATH_INFO"]
        self.m_name=self.current_href.split("/")[2]
        self.get_ability()
        self.get_model_info()
        self.get_page_object_list()
    
    def get_page_object_list(self):
        self.page_object_list=af.get_queryset(self.request.user,self.m_name)
    def get_model_info(self):
        self.model_obj,self.model=af.get_model(self.m_name)
    
    def get_ability(self):
        if "list" in self.current_href:
            self.ability="List"
        elif "detail" in self.current_href:
            self.ability="Detail"
        elif "update" in self.current_href:
            self.ability="Update"
        elif "delete" in self.current_href:
            self.ability="Delete"
        elif "add" in self.current_href:
            self.ability="Add"
        
    def get_search_data(self):
        if "search" in self.request.GET:
            self.search= self.request.GET["search"]
        
    def get_obj_id(self):
        if "Detail" == self.ability or "Update" == self.ability or "Delete" == self.ability:
            self.cur=int(self.current_href.split("/")[3])
    
    def get_detail_index(self):
        obj_list=sorted(self.page_object_list,key=atg("id"))
        self.last=obj_list[-1].id
        self.first=obj_list[0].id
        if self.last==self.cur:
            self.next=self.last
        else:
            self.next=self.go_up(self.model,self.cur+1)
        if self.first==self.cur:
            self.prev=self.cur
        else:
            self.prev=self.go_down(self.model,self.cur-1)
            
    def go_up(self,model,pk):
        if self.page_object_list.exists():
            return pk
        else:
            return self.go_up(model,pk+1)
    def go_down(self,model,pk):
        if model.objects.filter(id=pk).exists():
            return pk
        else:
            return self.go_up(model,pk-1)
    
    def get_detail_page(self):
        self.direction=self.request.GET.get("direction")
        self.get_obj_id()
        self.get_detail_index()
        page_info = []
        page_info.append("/detail/%s/%d" % (self.m_name, self.first))
        page_info.append("/detail/%s/%d" % (self.m_name, self.prev))
        page_info.append(self.cur)
        page_info.append("/detail/%s/%d" % (self.m_name, self.next))
        page_info.append("/detail/%s/%d" % (self.m_name, self.last))
        return page_info
        
    def get_page_no(self):
        if "page" in self.request.GET:
            self.cur=int(self.request.GET["page"])
    
    def get_list_index(self):
        total=len(self.page_object_list)
        self.last=int((total + 49)/50)
        self.next=self.cur+1
        self.prev=self.cur-1
        if self.prev<self.first:
            self.prev=self.first
        if self.next>self.last:
            self.next=self.last
        
    def get_list_page(self):
        self.get_page_no()
        self.get_list_index()
        self.get_search_data()
        href=""
        if self.search!=None:
            href+="&search=%s" %self.search
        page_info=[]
        if self.first+4<=self.cur:
            page_info.append(("/list/%s/?page=%d%s" % (self.m_name,self.first,href),self.first,"İlk"))
        if self.first+3<=self.cur:
            page_info.append(("/list/%s/?page=%d%s" % (self.m_name,self.cur-3,href),self.cur-3,self.cur-3))
        if self.first+2<=self.cur:
            page_info.append(("/list/%s/?page=%d%s" % (self.m_name,self.cur-2,href),self.cur-2,self.cur-2))
        if self.first+1<=self.cur:
            page_info.append(("/list/%s/?page=%d%s" % (self.m_name,self.cur-1,href),self.cur-1,self.cur-1))
        if self.first<=self.cur and self.cur<=self.last:
            page_info.append(("#",self.cur,self.cur))
        if self.cur+1<=self.last:
            page_info.append(("/list/%s/?page=%d%s" % (self.m_name,self.cur+1,href), self.cur + 1, self.cur + 1))
        if self.cur+2<=self.last:
            page_info.append(("/list/%s/?page=%d%s" % (self.m_name,self.cur+2,href), self.cur + 2, self.cur + 2))
        if self.cur+3<=self.last:
            page_info.append(("/list/%s/?page=%d%s" % (self.m_name,self.cur+3,href), self.cur + 3, self.cur + 3))
        if self.cur+4<=self.last:
            page_info.append(("/list/%s/?page=%d%s" % (self.m_name,self.last,href), self.last,"Son"))
        return page_info
    
    def get_page(self):
        if self.ability=="Detail":
            return self.get_detail_page()
        elif self.ability=="List":
            return self.get_list_page()
        else:
            return redirect("global_detail",m_name=self.m_name)