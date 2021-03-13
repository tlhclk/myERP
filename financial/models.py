# -*- coding: utf-8 -*-
### import_part
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from people.models import *
from main.models import *
from functions.model import AttrDict
from constant.models import *


### models_part
class Currency(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Para Birimi')
	symbol = models.CharField(null=True,blank=True,max_length=10,verbose_name='Sembolü')
	rate = models.CharField(null=True,blank=True,max_length=10,verbose_name='Endeksi')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='currency_m'
		ordering=["name"]
	## def 1
	def __str__(self):
		return str(self.name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)

class Account(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Hesap Adı')
	owner = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Person,verbose_name='Sahibi')
	corporation = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=CorporationLM,verbose_name='Bankası')
	account_no = models.CharField(null=True,blank=True,max_length=20,verbose_name='Hesap No')
	iban = models.CharField(null=True,blank=True,max_length=26,verbose_name='IBAN')
	currency = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Currency,verbose_name='Para Birimi')
	internet_pass = models.CharField(null=True,blank=True,max_length=20,verbose_name='İnternet Şifresi')
	mobile_pass = models.CharField(null=True,blank=True,max_length=50,verbose_name='Mobil Şifresi')
	card_type = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=CardTypeLM,verbose_name='Kart Tipi')
	cart_no = models.CharField(null=True,blank=True,max_length=26,verbose_name='Kart Numarası')
	last_month = models.CharField(null=True,blank=True,max_length=2,verbose_name='Son Kullanım Ayı')
	last_year = models.CharField(null=True,blank=True,max_length=4,verbose_name='Son Kullanım Tarihi')
	csv = models.CharField(null=True,blank=True,max_length=3,verbose_name='CSV')
	card_pass = models.CharField(null=True,blank=True,max_length=10,verbose_name='Kart Şifresi')
	secret_phrase = models.CharField(null=True,blank=True,max_length=50,verbose_name='Gizli Kelime')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	update_date = models.DateField(null=True,blank=True,default=datetime.today,verbose_name='Güncelleme Tarihi')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	amount = models.DecimalField(null=True,blank=True,verbose_name='Miktar',max_digits=20,decimal_places=3)
	is_active = models.BooleanField(default=True,verbose_name='Aktif Mi?')
	## class
	class Meta:
		db_table='account_m'
		ordering=["corporation","name"]
	## def 1
	def __str__(self):
		return str(self.name) + " - " + str(self.corporation)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class Transaction(models.Model):
	## fields
	account = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Account,verbose_name='Hesap')
	date = models.DateField(null=True,blank=True,default=datetime.now,verbose_name='Tarih')
	time = models.TimeField(null=True,blank=True,verbose_name='Saat')
	category = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=TransactionCategoryLM,verbose_name='İşlem Kategorisi')
	corporation = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=CorporationLM,verbose_name='İşlem Yeri')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	type = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=TransactionTypeLM,verbose_name='İşlem Tipi')
	amount = models.DecimalField(null=True,blank=True,verbose_name='Miktar',max_digits=10,decimal_places=3)
	account_amount = models.DecimalField(null=True,blank=True,verbose_name='Hesap Miktarı',max_digits=20,decimal_places=3)
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='transaction_m'
		ordering=["-date","-time"]
	## def 1
	def __str__(self):
		if self.corporation_id==154:
			return str(self.desc) + " - " + str(self.account) +  " - " + str(self.amount)
		else:
			return str(self.corporation) + " - " + str(self.account) +  " - " + str(self.amount)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class Change(models.Model):
	## fields
	person = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Person,verbose_name='Kime - Kimden')
	purpose = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=ChangePurposeLM,verbose_name='Aldım - Verdim Amacı')
	name=models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	is_active = models.BooleanField(default=True,verbose_name='Aktif Mi?')
	date = models.DateField(null=True,blank=True,default=datetime.today,verbose_name='Ekleme Tarihi')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	
	## class
	class Meta:
		db_table='change_m'
		ordering=["-is_active","-date"]
	## def 1
	def __str__(self):
		if self.name==None:
			return str(self.person) + " - " + str(self.purpose)
		else:
			return str(self.name) + " - " + str(self.purpose)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()
	
class ChangeTransaction(models.Model):
	## fields
	change=models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Change,verbose_name="Aldım - Verdim")
	transaction=models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Transaction,verbose_name="İşlem")
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='change_transaction_m'
		ordering=["change"]
	## def 1
	def __str__(self):
		return str(self.change)+" - "+str(self.transaction)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class CurrencyHistory(models.Model):
	## fields
	currency = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Currency,verbose_name='Para Birimi')
	date = models.DateField(null=True,blank=True,default=datetime.today,verbose_name='Tarih')
	start_rate = models.CharField(null=True,blank=True,max_length=10,verbose_name='Başlama Oranı')
	end_rate = models.CharField(null=True,blank=True,max_length=10,verbose_name='Bitme Oranı')
	max_rate = models.CharField(null=True,blank=True,max_length=10,verbose_name='En Fazla Oran')
	min_rate = models.CharField(null=True,blank=True,max_length=10,verbose_name='En Az Oran')
	avg_rate = models.CharField(null=True,blank=True,max_length=10,verbose_name='Ortalama Oran')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='currencyhistory_m'
		ordering=["-date"]
	## def 1
	def __str__(self):
		return str(self.currency) + " - " + str(self.date)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()
