# -*- coding: utf-8 -*-
### import_part
from django.contrib.auth.models import User

from functions.model import AttrDict
from main.models import *
from people.models import *


### models_part
class MyPassword(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Uygulama Adı')
	web_address = models.CharField(null=True,blank=True,max_length=100,verbose_name='Web Adresi')
	person = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Person,verbose_name='Sahibi')
	username = models.CharField(null=True,blank=True,max_length=50,verbose_name='Kullanıcı Adı')
	email = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=PersonEmail,verbose_name='E-Mail Adresi')
	backup_email = models.EmailField(null=True,blank=True,max_length=50,verbose_name='Yedek E-Mail Adresi')
	pass1 = models.CharField(null=True,blank=True,max_length=20,verbose_name='1. Şifre')
	pass2 = models.CharField(null=True,blank=True,max_length=20,verbose_name='2. Şifre')
	secret_phrase = models.CharField(null=True,blank=True,max_length=50,verbose_name='Gizli Kelime')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	update_date = models.DateField(null=True,blank=True,default=datetime.today,verbose_name='Güncelleme Tarihi')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='mypassword_m'
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
