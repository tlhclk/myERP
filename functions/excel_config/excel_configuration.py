import xlrd,xlwt,datetime,os
from functions.auth_func import *
from django.shortcuts import render,redirect

class ExcelConfig:
	def __init__(self,path):
		self.path=path
		self.wb0=xlrd.open_workbook(path)
		self.all_model_req={}
		
	def get_sheet_data(self,sht):
		data_list=[]
		variable_list=[]
		for x in range(sht.ncols):
			variable_list.append(sht.cell(0,x).value)
		for y in range(1,sht.nrows):
			row_dict={}
			for x in range(sht.ncols):
				row_dict[variable_list[x]]=sht.cell(y,x).value
			data_list.append(row_dict)
		return variable_list,data_list
	
	
	def get_model_data(self):
		model_sht=self.wb0.sheet_by_name("model")
		return self.get_sheet_data(model_sht)
	
	def get_field_data(self):
		field_sht=self.wb0.sheet_by_name("field")
		return self.get_sheet_data(field_sht)
	
	def check_fields(self,field_list,var_list):
		for field in field_list:
			if field["name"] in var_list:
				var_list.remove(field["name"])
			elif field["name"]+"_id" in var_list:
				var_list.remove(field["name"]+"_id")
			else:
				print("%s field not in %s model" % (field["name"],field["model"]))
		print("%s variables is not in %s model field list" % (', '.join(var_list),field_list[0]["model"]))
	
	def filter_field_list(self,field_list,model_name):
		result_list=[]
		model_req=[]
		for field in field_list:
			if field["model"]==model_name:
				result_list.append(field)
				if field["to"]!="" and field["to"]!=None:
					model_req.append(field["to"])
		self.all_model_req[model_name]=model_req
		print("%s modeli gereksinimler: %s" % (model_name,", ".join(model_req)))
		return result_list
		
	def start_flow(self):
		model_var_list,model_data_list=self.get_model_data()
		field_var_list,field_data_list=self.get_field_data()
		
		for model in model_data_list:
			if model["sheet_name"] in self.wb0.sheet_names():
				field_list=self.filter_field_list(field_data_list,model["name"])
				new_sht=self.wb0.sheet_by_name(model["sheet_name"])
				var_list,data_list=self.get_sheet_data(new_sht)
				self.check_fields(field_list,var_list)
			else:
				print("%s model is not in sheet list" % model["name"])
				
		
path="d:\\Talha\\Masaüstü\\databse1.xlsx"
#exc=ExcelConfig(path)
#exc.start_flow()


class ExcelToDatabase:
	all_data={}
	all_model_req={}
	finished_models=["User","ModelLM","PanelLM","FieldLM","ContinentLM"]
	def __init__(self,path):
		self.path=path
		self.wb0=xlrd.open_workbook(self.path)
		self.model_var_list,self.model_data_list=self.get_model_data()
		self.field_var_list,self.field_data_list=self.get_field_data()
	
	def get_sheet_data(self,sht):
		data_list=[]
		variable_list=[]
		for x in range(sht.ncols):
			variable_list.append(sht.cell(0,x).value)
		for y in range(1,sht.nrows):
			row_dict={}
			for x in range(sht.ncols):
				row_dict[variable_list[x]]=sht.cell(y,x).value
			data_list.append(row_dict)
		return variable_list,data_list
	
	def get_model_data(self):
		model_sht=self.wb0.sheet_by_name("model")
		return self.get_sheet_data(model_sht)
	
	def get_field_data(self):
		field_sht=self.wb0.sheet_by_name("field")
		return self.get_sheet_data(field_sht)
	
	def filter_field_list(self,field_list,model_name):
		result_list=[]
		model_req=[]
		for field in field_list:
			if field["model"]==model_name:
				result_list.append(field)
				if field["to"]!="" and field["to"]!=None:
					model_req.append(field["to"])
		self.all_model_req[model_name]=model_req
		print("%s modeli gereksinimler: %s" % (model_name,", ".join(model_req)))
		return result_list
	
	def get_model(self,model_name):
		model=None
		for mdl in self.model_data_list:
			if mdl["name"]==model_name:
				model=mdl
		return model
	
	def start_flow(self):
		for model in self.model_data_list:
			if model["sheet_name"] in self.wb0.sheet_names():
				if model["name"]=="RepetitiveRecord":
					self.transfer_data(model)
			else:
				print("%s model is not in sheet list" % model["name"])

	def transfer_data(self,model):
		model_obj,model_cls=self.get_model(model["name"])
		cls_sht=self.wb0.sheet_by_name(model["sheet_name"])
		var_list,data_list=self.get_sheet_data(cls_sht)
		field_list=self.filter_field_list(self.field_data_list,model["name"])
		for data in data_list:
			new_cls=model_cls()
			setattr(new_cls,"id",int(data["id"]))
			for i,var in enumerate(field_list):
				var=var["name"]
				if var in var_list or var+"_id" in var_list:
					if field_list[i]["field"]=="ForeignKey":
						if data[var+"_id"]!="":
							value=int(data[var+"_id"])
							if not hasattr(new_cls,var+"_id"):
								print(new_cls,var)
							setattr(new_cls,var+"_id",value)
					elif field_list[i]["field"]=="BooleanField":
						print(var,data[var],field_list[i]["field"])
						value=int(data[var])
						setattr(new_cls,var,value)
					elif field_list[i]["field"]=="CharField":
						print(var,data[var],field_list[i]["field"])
						value=str(data[var])
						setattr(new_cls,var,value)
					elif field_list[i]["field"]=="DateField":
						if data[var]!="":
							value_list=str(data[var]).split(".")
							print(var,data[var],field_list[i]["field"])
							value=datetime.date(day=int(value_list[0]),)
							#value=datetime.date(day=int(value_list[0]),month=int(value_list[1]),year=int(value_list[2]))
							print(value)
							setattr(new_cls,var,value)
					else:
						print(var,data[var],field_list[i]["field"])
						value=data[var]
						#setattr(new_cls,var,value)
			#new_cls.save()


def temptry2(request):
	etd=ExcelToDatabase(path)
	etd.start_flow()
	return redirect("home")

class CodeToExcel:
	def __init__(self):
		self.excel_path="\\ExcelConfigFile.xls"
		self.model_data={}
		self.path_data={}
		self.import_data={}
		self.file_path_data={}
		self.panel_data=[]
		
	def get_file_path_data(self,base_path):
		banned_folders=["migrations","templates","static","media","logger"]
		obj_list=os.listdir(base_path)
		self.file_path_data[base_path]=obj_list
		for obj in obj_list:
			path="%s\\%s" % (base_path,obj)
			if obj not in banned_folders:
				if os.path.isdir(path):
					self.get_file_path_data(path)
				else:
					extention=path.split(".")[-1]
					if extention=="py":
						if obj=="models.py":
							print(path)
		
		
def temptry(request):
	cte=CodeToExcel()
	cte.get_file_path_data(os.getcwd())
	return redirect("home")
