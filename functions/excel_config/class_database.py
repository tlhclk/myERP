# -*- coding: utf-8 -*-
from datetime import datetime


class Panel:
	def __init__(self):
		self.name = None
		self.type = None
		self.title = None
		self.desc = None


class Model:
	def __init__(self):
		self.panel = None
		self.name = None
		self.order = None
		self.ordering = None
		self.db_table = None
		self.list_title = None
		self.form_title = None
		self.detail_title = None
		self.desc = None

class Field:
	def __init__(self):
		self.model = None
		self.name = None
		self.order = None
		self.field = None
		self.null = None
		self.blank = None
		self.max_length = None
		self.on_delete = None
		self.to = None
		self.default = None
		self.verbose_name = None
		self.max_digits = None
		self.decimal_places = None
		self.show_list = None
		self.form = None
		self.form_add = None
		self.form_delete = None
		self.form_update = None
		self.show_detail = None

class Path:
	def __init__(self):
		self.title = None
		self.path = None
		self.view_func = None
		self.name = None
		self.panel = None
		self.type = None
		self.location = None
		self.desc = None
		
		
class Database:
	def __init__(self):
		self.panel_list=[]
		self.model_list=[]
		self.field_list=[]
		self.path_list=[]
		
	def get(self, class_type,by,value):
		class_dict={"panel":self.panel_list,"model":self.model_list,"field":self.field_list,"path":self.path_list}
		class_list=class_dict[class_type]
		for obj in class_list:
			if hasattr(obj,by):
				obj_value=getattr(obj,by)
				if value==obj_value:
					return obj
		return None
	
