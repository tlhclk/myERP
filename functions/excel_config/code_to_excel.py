# -*- coding: utf-8 -*-
import xlrd,xlwt,datetime,os,re
import functions.excel_config.class_database as cd
from main.models import PanelLM,FieldLM,ModelLM
from django.apps import apps
import functions.auth_func as af


class CodeToDb:
	def __init__(self):
		self.db=cd.Database()
		self.excel_path = "\\ExcelConfigFile.xls"
		self.models_data = {}
		self.urls_data = {}
		self.import_data = {}
		self.file_path_data = {}
		self.models_py_list=[]
		self.urls_py_list=[]
		self.other_py_list=[]
	
		
	def get_file_path_data(self, base_path):
		banned_folders = ["migrations", "templates", "static", "media", "logger"]
		obj_list = os.listdir(base_path)
		panel_name=base_path.split("\\")[-1]
		self.file_path_data[base_path] = obj_list
		for obj in obj_list:
			path = "%s\\%s" % (base_path, obj)
			if obj not in banned_folders:
				if os.path.isdir(path):
					self.get_file_path_data(path)
				else:
					extention = path.split(".")[-1]
					if extention == "py":
						print(panel_name)
						if obj == "models.py":
							self.models_py_list.append(path)
						elif obj== " urls.py":
							self.urls_py_list.append(path)
						else:
							self.other_py_list.append(path)
	
	def new_field(self,field,field_obj_list):
		new_flm = FieldLM()
		new_flm.order = len(field_obj_list) + 1
		new_flm.field = field.__class__.__name__
		new_flm.show_detail = True
		new_flm.show_list = True
		new_flm.form_add = True
		new_flm.form_update = True
		new_flm.form_delete = True
		new_flm.model = af.get_model(field.model.__name__)[0]
		new_flm.name = field.name
		new_flm.null = field.null
		new_flm.blank = field.blank
		new_flm.max_length = field.max_length
		new_flm.default = field.default
		new_flm.verbose_name = field.verbose_name
		if field=="ForeignKey":
			new_flm.to =  field.related_model.__name
		if hasattr(field,"on_delete"):
			new_flm.on_delete=field.on_delete
		if hasattr(field,"max_digits"):
			new_flm.max_digits=field.max_digits
		if hasattr(field,"decimal_places"):
			new_flm.decimal_places=field.decimal_places
		return new_flm.save()
	
	def new_model(self,model):
		new_mlm = ModelLM()
		new_mlm.name = model._meta.model_name
		new_mlm.db_table = model._meta.db_table
		new_mlm.panel = self.get_panel_obj(model._meta.apps)
		new_mlm.ordering = model._meta.ordering
		new_mlm.verbose_name = model._meta.verbose_name
		new_mlm.verbose_name_plural = model._meta.verbose_name_plural
		return new_mlm.save(),model
	
	def get_panel_obj(self,panel_name):
		for panel in PanelLM.objects.all():
			if panel.name==panel_name:
				return panel
		return None
		
	def get_field_obj(self,field,field_obj_list):
		model_name=field.model.__name__
		field_name=field.name
		for field_obj in field_obj_list:
			if field_obj.name==field_name and field_obj.model.name==model_name:
				return field_obj
		return self.new_field(field,field_obj_list)
	
	def get_model_data(self):
		for model in apps.get_models():
			if model.__name__=="ModelLM":
				field_list=model._meta.get_fields()
				model_obj,model_other = af.get_model(model.__name__)
				if model_obj==None:
					model_obj,model_other=self.new_model(model)
					field_obj_list=[]
				else:
					field_obj_list=af.get_fields(model_obj,"All")
				for field in field_list:
					field_type=field.__class__.__name__
					if field_type!="AutoField" and field_type!="ManyToOneRel":
						#field_attr_key_list=["_db_tablespace","_error_messages","_unique","_validators","_verbose_name","attname","auto_created","auto_now","auto_now_add","blank","choices","column","concrete","creation_counter","db_column","db_constraint","db_index","default","editable","error_messages","field","field_name","foreign_related_fields","from_fields","help_text","hidden","is_relation","limit_choices_to","max_length","model","multiple","name","null","on_delete","opts","parent_link","primary_key","related_fields","related_model","related_name","related_query_name","remote_field","serialize","swappable","symmetrical","to_fields","unique_for_date","unique_for_month","unique_for_year","validators","verbose_name","decimal_places","max_digits"]
						#valid_field_attr_key_list=["order","field","null","blank","max_length","on_delete","to","default","verbose_name","max_digits","show_list","form","form_add","form_update","form_delte","show_detail","model","name","decimal_places"]
						update_flm = self.get_field_obj(field, field_obj_list)
						if update_flm!=None:
							update_flm.field = field.__class__.__name__
							update_flm.null = field.null
							update_flm.blank = field.blank
							update_flm.max_length = field.max_length
							update_flm.default = field.default
							update_flm.verbose_name = field.verbose_name
							if field == "ForeignKey":
								update_flm.to = field.related_model.__name__
							if hasattr(field, "on_delete"):
								update_flm.on_delete = field.on_delete
							if hasattr(field, "max_digits"):
								update_flm.max_digits = field.max_digits
							if hasattr(field, "decimal_places"):
								update_flm.decimal_places = field.decimal_places
							update_flm.save()
						
					

				
	