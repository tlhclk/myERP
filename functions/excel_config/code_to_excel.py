# -*- coding: utf-8 -*-
import xlrd,xlwt,datetime,os,re
import functions.excel_config.class_database as cd
from main.models import PanelLM,FieldLM,ModelLM,PathLM
from django.apps import apps
import functions.auth_func as af
from functions.auth_func import ModelFunc
from django import urls



class CodeToDb(ModelFunc):
	def __init__(self):
		super(CodeToDb, self).__init__()
		self.db=cd.Database()
		self.excel_path = "\\ExcelConfigFile.xls"
		self.models_data = {}
		self.urls_data = {}
		self.import_data = {}
		self.file_path_data = {}
		self.models_py_list=[]
		self.urls_py_list=[]
		self.other_py_list=[]
	
		
	def get_file_path_data(self, base_path):#iş yapmıyor şuan
		non_panel_list=[panel.name for panel in PanelLM.objects.exclude(type="panel")]
		folder_list = os.listdir(base_path)
		self.file_path_data[base_path] = folder_list
		for folder_name in folder_list:
			folder_path = "%s\\%s" % (base_path, folder_name)
			if folder_name not in non_panel_list:
				if self.folder_check(folder_path):
					file_list = os.listdir(folder_path)
					self.file_path_data[folder_path] = file_list
					for file_name in file_list:
						file_path = "%s\\%s" % (folder_path, file_name)
						extention = file_path.split(".")[-1]
						if extention == "py":
							if file_name == "models.py":
								self.models_py_list.append(file_path)
							elif file_name== " urls.py":
								self.urls_py_list.append(file_path)
							else:
								self.other_py_list.append(file_path)
								
	def folder_check(self,folder_path):
		if os.path.isdir(folder_path):
			folder_name = os.path.basename(folder_path)
			panel_list=PanelLM.objects.filter(type="panel").filter(name=folder_name)
			if len(panel_list)==0:
				PanelLM.objects.create(name=folder_name,type="panel",title=folder_name)
			return True
		return False
		
	def get_database_info(self):
		for model in apps.get_models():
			panel_name=model.__module__.split(".")[-2]
			panel=self.get_panel(panel_name)
			if panel!=None:
				field_list=model._meta.get_fields()
				model_obj = self.get_model_obj(model.__name__)
				model = self.get_model(model_obj)
				if model_obj==None:
					model_obj,model_other=self.new_model(model)
					field_obj_list=[]
					for field in field_list:
						field_type=field.__class__.__name__
						if field_type!="AutoField" and field_type!="ManyToOneRel" and field_type!="ManyToManyField":
							field_obj=self.field_edit(field,FieldLM(),len(field_obj_list)+1,model_obj)
							field_obj_list.append(field_obj)
				else:
					field_obj_list=self.get_model_fields(model_obj,"All")
					for field in field_list:
						field_type=field.__class__.__name__
						if field_type!="AutoField" and field_type!="ManyToOneRel" and field_type!="ManyToManyField":
							field_obj=self.get_field_obj(field,field_obj_list)
							if field_obj not in field_obj_list:
								field_obj_list.append(field_obj)
						
	def field_edit(self,field,field_obj,fol,model_obj):
		new_flm = field_obj
		new_flm.order = fol
		new_flm.field = field.__class__.__name__
		new_flm.model = model_obj
		new_flm.name = field.name
		if hasattr(field,"null"):
			new_flm.null = field.null
		if hasattr(field,"blank"):
			new_flm.blank = field.blank
		if hasattr(field,"max_length"):
			new_flm.max_length = field.max_length
		if hasattr(field,"default"):
			if hasattr(field.default,"__name__"):
				if hasattr(field.default,"__dict__"):
					new_flm.default = field.default.__doc__
				else:
					new_flm.default = field.default.__qualname__
			else:
				new_flm.default = field.default
		if hasattr(field,"verbose_name"):
			new_flm.verbose_name = field.verbose_name
		if field=="ForeignKey":
			new_flm.to =  field.related_model.__name
		if hasattr(field,"on_delete"):
			new_flm.on_delete=field.on_delete
		if hasattr(field,"max_digits"):
			new_flm.max_digits=field.max_digits
		if hasattr(field,"decimal_places"):
			new_flm.decimal_places=field.decimal_places
		new_flm.save()
		return new_flm
	
	def new_model(self,model):
		new_mlm = ModelLM.objects.create(name = model._meta.model_name,
		                                 db_table = model._meta.db_table,
		                                 panel = self.get_panel(model._meta.apps),
		                                 ordering = model._meta.ordering,
		                                 verbose_name = model._meta.verbose_name,
		                                 verbose_name_plural = model._meta.verbose_name_plural)
		return new_mlm,model
		
	def get_field_obj(self,field,field_obj_list):
		model_name=field.model.__name__
		field_name=field.name
		for field_obj in field_obj_list:
			if field_obj.name==field_name and field_obj.model.name==model_name:
				return self.field_edit(field,field_obj,field_obj.order,field_obj.model)
		return self.field_edit(field,FieldLM(),len(field_obj_list)+1,self.get_model_obj(model_name))
	
	
	def get_urls(self):
		url_list=urls.get_resolver().url_patterns
		for url in url_list:
			if hasattr(url,"url_patterns"):
				for sub_url in url.url_patterns:
					if not hasattr(sub_url,"url_patterns"):
						if hasattr(sub_url.pattern,"_route"):
							key=url.pattern._route[:-1]+":"+sub_url.name
							value=url.pattern._route+sub_url.pattern._route
							if key not in self.urls_data:
								self.urls_data[key]=value
							else:
								self.urls_data[key]+=value
			else:
				if hasattr(url.pattern,"_route"):
					if url.pattern.name not in self.urls_data:
						self.urls_data[url.pattern.name]=url.pattern._route
					else:
						self.urls_data[url.pattern.name]+=url.pattern._route
	
	def urls_parting(self):
		for key,value in self.urls_data.items():
			if "global_"==key[:7]:
				print("GLOBALLER",key)
			elif "_report"==key[-7:]:
				#print("RAPORLAR",key)
				self.check_urls("report",key,value)
			elif "_function"==key[-9:]:
				#print("FONKSİYONLAR",key)
				self.check_urls("function",key,value)
			elif "_ajax"==key[-5:]:
				#print("AJAX",key)
				self.check_urls("ajax",key,value)
			elif ("password" in key or "login" in key or "register" in key or "logout" in key) and ("admin" not in key):
				print("REGISTER",key)
			elif "home" ==key:
				print("HOME",key)
			elif "admin/"==key[:6]:
				print("ADMİN",key)
			else:
				print("Diğer",key)
			
	def check_urls(self,type_text,name,url):
		short_name = name.split(":")[-1]
		path_list=PathLM.objects.filter(type=type_text).filter(name=short_name)
		base_path="/".join(url.split("/")[1:])
		panel_name=name.split(":")[0]
		panel=PanelLM.objects.filter(name=panel_name)
		if panel==None:
			panel=[PanelLM.objects.get(pk=9)]
		if len(path_list)==0:
			PathLM.objects.create(name=short_name,
			                      path=base_path,
			                      location="/"+url,
			                      panel=panel[0],
			                      type=type_text)
