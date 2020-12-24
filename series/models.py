# -*- coding: utf-8 -*-
### import_part
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from constant.models import *
from main.models import *
from functions.model import AttrDict


### models_part
class Series(models.Model):
	## fields
	main_name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Ana Seri Adı')
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Seri Adı')
	second_name = models.CharField(null=True,blank=True,max_length=50,verbose_name='İkincil Adı')
	series_type = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=SeriesTypeLM,verbose_name='Seri Tipi')
	web_address = models.CharField(null=True,blank=True,max_length=100,verbose_name='Web Adresi')
	rate = models.CharField(null=True,blank=True,max_length=5,verbose_name='Puanı')
	current_eps = models.CharField(null=True,blank=True,max_length=3,verbose_name='Mevcut Bölüm')
	total_eps = models.CharField(null=True,blank=True,max_length=3,verbose_name='Toplam Bölüm')
	season = models.CharField(null=True,blank=True,max_length=2,verbose_name='Sezon Adedi')
	state = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=SeriesStateLM,verbose_name='Durumu')
	download = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=SeriesDownloadLM,verbose_name='İndirilebilirliği')
	start_date = models.DateField(null=True,blank=True,default=datetime.today,verbose_name='Başlama Tarihi')
	country = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=CountryLM,verbose_name='Ülkesi')
	director = models.CharField(null=True,blank=True,max_length=50,verbose_name='Yönetmeni')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='series_m'
		ordering=["name","season","current_eps"]
	## def 1
	def __str__(self):
		if self.second_name:
			return str(self.name) + " - " + str(self.second_name)
		elif self.season:
			return str(self.name) + " (" + str(self.season) + ". Sezon)"
		elif self.current_eps:
			return str(self.name) + " (" + str(self.current_eps) + ". Bölüm)"
		else:
			return str(self.name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class SeriesGenre(models.Model):
	## fields
	series = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Series,verbose_name='Seri')
	genre = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=SeriesGenreLM,verbose_name='Seri Türü')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='seriesgenre_m'
		ordering=["series"]
	## def 1
	def __str__(self):
		return str(self.series) + "-" +str(self.genre)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class RelatedSeries(models.Model):
	## fields
	series1 = models.CharField(null=True,blank=True,max_length=50,verbose_name='Seri 1')
	series2 = models.CharField(null=True,blank=True,max_length=50,verbose_name='Seri 2')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='relatedseries_m'
		ordering=["series1","series2"]
	## def 1
	def __str__(self):
		return str(self.series1) + "-" +str(self.series2) + "-" + str(self.desc)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()
