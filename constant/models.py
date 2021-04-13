# -*- coding: utf-8 -*-
### import_part
from django.db import models
from functions.model import AttrDict


### models_part
class ContinentLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='continent_lm'
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

class CountryLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	code = models.CharField(null=True,blank=True,max_length=5,verbose_name='Kodu')
	continent = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=ContinentLM,verbose_name='Kıtası')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='country_lm'
		ordering=["continent","name"]
	## def 1
	def __str__(self):
		return str(self.name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class CityLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	code = models.CharField(null=True,blank=True,max_length=5,verbose_name='Kodu')
	country = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=CountryLM,verbose_name='Ülkesi')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='city_lm' 
		ordering=["country","name"]
	## def 1
	def __str__(self):
		return str(self.name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class TownLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	code = models.CharField(null=True,blank=True,max_length=5,verbose_name='Kodu')
	city = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=CityLM,verbose_name='İli')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='town_lm' 
		ordering=["city","name"]
	## def 1
	def __str__(self):
		return str(self.city)+" - "+str(self.name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class CardTypeLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='cardtype_lm' 
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

class ChangePurposeLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='changepurpose_lm' 
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

class RepetitiveTypeLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='repetitivetype_lm' 
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

class CorporationTypeLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='corporationtype_lm' 
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

class EmailTypeLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='emailtype_lm' 
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

class EventTypeLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='eventtype_lm' 
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

class GenderLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='gender_lm' 
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

class MediaTypeLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	base_url = models.CharField(null=True,blank=True,max_length=50,verbose_name='Kaynak Url')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='mediatype_lm' 
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

class PeriodLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	day = models.CharField(null=True,blank=True,max_length=4,verbose_name='Gün')
	## class
	class Meta:
		db_table='period_lm' 
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

class PhoneTypeLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='phonetype_lm' 
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

class RelationshipLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	code = models.CharField(null=True,blank=True,max_length=50,verbose_name='Kod')
	## class
	class Meta:
		db_table='relationship_lm' 
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

class SchoolTypeLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='schooltype_lm' 
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

class SeriesDownloadLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='seriesdownload_lm' 
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

class SeriesGenreLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='seriesgenre_lm' 
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

class SeriesStateLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='seriesstate_lm' 
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

class SeriesTypeLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='seriestype_lm' 
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

class TransactionCategoryLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='transactioncategory_lm' 
		ordering=["name"]
	## def 1
	def __str__(self):
		return str(self.name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)

class TransactionTypeLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='transactiontype_lm' 
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

class MarketLM(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='market_lm' 
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
