# -*- coding: utf-8 -*-
### import_part
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from main.models import ModelLM, CorporationLM
from datetime import datetime
from functions.model import AttrDict
from django.contrib.sessions.models import Session


### models_part
class PersonalPermission(models.Model):
	## fields
	user_name = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	model = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=ModelLM,verbose_name='Model Adı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='personealpermission'
		ordering=["user_name","model"]
	## def 1
	def __str__(self):
		return str(self.user_name) + " - " + str(self.model)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class UserPermission(models.Model):
	## fields
	user_name = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	personal_permission = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=PersonalPermission,verbose_name='Kişisel İzinler')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='user_permission'
		ordering=["user_name","personal_permission"]
	## def 1
	def __str__(self):
		return str(self.user_name) + " - " + str(self.personal_permission)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class MyUserProfile(models.Model):
	## fields
	profile_pic = models.CharField(null=True,blank=True,max_length=200,verbose_name='Profil Fotoğrafı')
	## def 1
	def __str__(self):
		return 
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class MyGroup(models.Model):
	## fields
	name = models.CharField(null=True,blank=True,max_length=200,verbose_name='Grup Adı')
	corporation = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=CorporationLM,verbose_name='Firma')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='my_group'
		ordering=["corporation","name"]
	## def 1
	def __str__(self):
		return str(self.corporation) + " - " + str(self.name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class UserGroup(models.Model):
	## fields
	user_name = models.CharField(null=True,blank=True,max_length=200,verbose_name='Kullanıcı')
	group = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=MyGroup,verbose_name='Grup')
	## class
	class Meta:
		db_table='user_group'
		ordering=["user_name"]
	## def 1
	def __str__(self):
		return str(self.group) + " - " + str(self.user_name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class HistoryLog(models.Model):
	## fields
	date = models.DateField(null=True,blank=True,default=datetime.today,verbose_name='Tarih')
	time = models.TimeField(null=True,blank=True,verbose_name='Saat')
	user_name = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	ip = models.CharField(null=True,blank=True,max_length=15,verbose_name='IP Adresi')
	session = models.CharField(null=True,blank=True,max_length=200,verbose_name='Oturum Kodu')
	csrftoken = models.CharField(null=True,blank=True,max_length=200,verbose_name='Csrf Token')
	action = models.CharField(null=True,blank=True,max_length=50,verbose_name='Eylem')
	web_address = models.CharField(null=True,blank=True,max_length=200,verbose_name='Web Adresi')
	## class
	class Meta:
		db_table='history_log'
		ordering=["-date","-time"]
	## def 1
	def __str__(self):
		return str(self.date)+" - "+str(self.time)+" - "+str(self.user_name)+" - "+str(self.session)+" - "+str(self.csrftoken)+" - "+str(self.action)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class UserIp(models.Model):
	## fields
	user_name = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	ip = models.CharField(null=True,blank=True,max_length=50,verbose_name='Ip Adresi')
	permission = models.BooleanField(null=True,blank=True,default=False,verbose_name="Yetki")
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='user_ip'
		ordering=["user_name","ip"]
	## def 1
	def __str__(self):
		return str(self.user_name) + " - " + str(self.ip)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()
	