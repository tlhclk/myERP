# -*- coding: utf-8 -*-
### import_part
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from main.models import *
from people.models import *
from financial.models import *
from functions.model import AttrDict


### models_part
class Event(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	event_type = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=EventTypeLM,verbose_name='Etkinlik Tipi')
	date = models.DateField(null=True,blank=True,default=datetime.today,verbose_name='Tarih')
	time = models.TimeField(null=True,blank=True,max_length=5,verbose_name='Saat')
	duration = models.CharField(null=True,blank=True,max_length=5,verbose_name='Süre')
	loc = models.CharField(null=True,blank=True,max_length=200,verbose_name='Konum')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='event_m'
		ordering = ["-date","-time"]
	## def 1
	def __str__(self):
		return str(self.date)+" - "+str(self.name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class Repetitive(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	period_rate = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=PeriodLM,verbose_name='Periyot Sıkılığı')
	period_amount = models.CharField(null=True,blank=True,max_length=50,verbose_name='Periyot Miktarı')
	type = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=RepetitiveTypeLM,verbose_name='Tekrarlı Olay Türü')
	person = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Person,verbose_name='Sahibi')
	corporation = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=CorporationLM,verbose_name='Firma')
	id_no = models.CharField(null=True,blank=True,max_length=50,verbose_name='Hesap No')
	change = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Change,verbose_name='Aldım - Verdim')
	code = models.CharField(null=True,blank=True,max_length=100,verbose_name='Kısa Kod')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	is_active = models.BooleanField(default=True,verbose_name='Aktif Mi?')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='repetitive'
		ordering=["name"]
	## def 1
	def __str__(self):
		return str(self.name)+" - "+str(self.person)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class RepetitiveRecord(models.Model):
	## fields
	repetitive = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Repetitive,verbose_name='Tekrarlı Olay')
	start_date = models.DateField(null=True,blank=True,verbose_name='Başlama Tarihi')
	end_date = models.DateField(null=True,blank=True,verbose_name='Bitiş Tarihi')
	last_date = models.DateField(null=True,blank=True,verbose_name='Son Ödeme Tarihi')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	transaction = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Transaction,verbose_name='İşlem')
	is_active = models.BooleanField(default=True,verbose_name='Aktif Mi?')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='repetitive_record'
		ordering=["-is_active","last_date"]
	## def 1
	def __str__(self):
		return str(self.repetitive)+" - "+str(self.end_date)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()
