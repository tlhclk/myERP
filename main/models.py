# -*- coding: utf-8 -*-
### import_part
from datetime import datetime
from constant.models import *


### models_part
class PanelLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	type = models.CharField(null=True,blank=True,max_length=50,verbose_name='Türü')
	title = models.CharField(null=True,blank=True,max_length=50,verbose_name='Başlık')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='panel_lm'
		ordering=["name"]
	## def 1
	def __str__(self):
		return str(self.title)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class ModelLM(models.Model):
	## fields
	panel = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=PanelLM,verbose_name='Panel Adı')
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Model Adı')
	order = models.IntegerField(null=True,blank=True,verbose_name='Sıra No')
	ordering = models.CharField(null=True,blank=True,max_length=100,verbose_name='Sıralama')
	db_table = models.CharField(null=True,blank=True,max_length=50,verbose_name='Tablo Adı')
	list_title = models.CharField(null=True,blank=True,max_length=200,verbose_name='Liste Başlığı')
	form_title = models.CharField(null=True,blank=True,max_length=50,verbose_name='Form Başlığı')
	detail_title = models.CharField(null=True,blank=True,max_length=50,verbose_name='Detay Başlığı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	verbose_name = models.CharField(null=True,blank=True,max_length=200,verbose_name='Başlık')
	verbose_name_plural = models.CharField(null=True,blank=True,max_length=200,verbose_name='Çoğul Başlık')
	## class
	class Meta:
		db_table='model_lm'
		ordering=["panel","order"]
	## def 1
	def __str__(self):
		return str(self.panel) + " - " + str(self.name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class FieldLM(models.Model):
	## fields
	model = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=ModelLM,verbose_name='Model Adı')
	name = models.CharField(null=True,blank=True,max_length=100,verbose_name='Adı')
	order = models.IntegerField(null=True,blank=True,verbose_name='Sıra No')
	field = models.CharField(null=True,blank=True,max_length=100,verbose_name='Alan Türü')
	null = models.BooleanField(default=True,verbose_name='Null ?')
	blank = models.BooleanField(default=True,verbose_name='Blank ?')
	max_length = models.CharField(null=True,blank=True,max_length=50,verbose_name='En Fazla Karakter')
	on_delete = models.CharField(null=True,blank=True,max_length=100,verbose_name='Silinme Şekli')
	to = models.CharField(null=True,blank=True,max_length=50,verbose_name='İlişkili Tablo')
	default = models.CharField(null=True,blank=True,max_length=100,verbose_name='Varsayılan Değer')
	verbose_name = models.CharField(null=True,blank=True,max_length=100,verbose_name='Alan Başlığı')
	max_digits = models.CharField(null=True,blank=True,max_length=50,verbose_name='En Fazla Basamak')
	decimal_places = models.CharField(null=True,blank=True,max_length=50,verbose_name='Virgülden sonraki hane')
	show_list = models.BooleanField(default=True,verbose_name='Listede Gösterimi')
	form = models.CharField(null=True,blank=True,max_length=50,verbose_name='Form Özelliği')
	form_add = models.BooleanField(default=True,verbose_name='Eklenebilir')
	form_delete = models.BooleanField(default=True,verbose_name='Silinebilir')
	form_update = models.BooleanField(default=True,verbose_name='Değiştirilebilir')
	show_detail = models.BooleanField(default=True,verbose_name='Detayda Gösterimi')
	## class
	class Meta:
		db_table='field_lm'
		ordering=["model","order"]
	## def 1
	def __str__(self):
		return str(self.model)+"-"+str(self.name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class PathLM(models.Model):
	## fields
	title = models.CharField(null=True,blank=True,max_length=100,verbose_name='Başlık')
	path = models.CharField(null=True,blank=True,max_length=100,verbose_name='Güzergah')
	view_func = models.CharField(null=True,blank=True,max_length=100,verbose_name='View Fonksiyonu')
	name = models.CharField(null=True,blank=True,max_length=100,verbose_name='Adı')
	panel = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=PanelLM,verbose_name='Panel')
	type = models.CharField(null=True,blank=True,max_length=100,verbose_name='Türü')
	location = models.CharField(null=True,blank=True,max_length=100,verbose_name='Konumu')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='path_lm'
		ordering=["panel","name"]
	## def 1
	def __str__(self):
		return str(self.panel)+":"+str(self.name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class PersonGroupLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='persongroup_lm' 
	## def 1
	def __str__(self):
		return str(self.name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class SchoolLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Okul Adı')
	type = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=SchoolTypeLM,verbose_name='Okul Tipi')
	city = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=CityLM,verbose_name='İli')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='school_lm'
		ordering=["city","name"]
	## def 1
	def __str__(self):
		return str(self.type)+"-"+str(self.name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class CorporationLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Firma Adı')
	market = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=MarketLM,verbose_name='Market Tipi')
	start_date = models.DateField(null=True,blank=True,default=datetime.today,verbose_name='Eklenme Tarihi')
	category = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=TransactionCategoryLM,verbose_name='Firma Kategorisi')
	city = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=CityLM,verbose_name='İli')
	town = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=TownLM,verbose_name='İlçesi')
	web_address = models.CharField(null=True,blank=True,max_length=100,verbose_name='Web Adresi')
	address = models.CharField(null=True,blank=True,max_length=100,verbose_name='Adresi')
	phone_number = models.CharField(null=True,blank=True,max_length=20,verbose_name='Telefon Numarası')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='corporation_lm'
		ordering=["name"]
	## def 1
	def __str__(self):
		return str(self.name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class DepartmentLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='department_lm'
		ordering=["name"]
	## def 1
	def __str__(self):
		return str(self.name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()
