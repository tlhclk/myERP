# -*- coding: utf-8 -*-
### import_part
from django.db import models
from django.contrib.auth.models import User
from main.models import ModelLM, CorporationLM,PanelLM,FieldLM,PathLM
from datetime import datetime
from functions.model import AttrDict
from django.contrib.auth.hashers import make_password

### models_part

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
	group = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=MyGroup,verbose_name='Grup')
	user_name = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı*')
	## class
	class Meta:
		db_table='user_group'
		ordering=["group","user_name"]
	## def 1
	def __str__(self):
		return str(self.group) + " - " + str(self.user_name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class PanelPermission(models.Model):
	## fields
	group = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=MyGroup,verbose_name='Grup')
	user_name = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı*')
	panel = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=PanelLM,verbose_name='Panel Adı')
	permission = models.BooleanField(null=True,blank=True,default=False,verbose_name='Yetki')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='panel_permission'
		ordering=["user_name","panel"]
	## def 1
	def __str__(self):
		if self.group:
			return str(self.group) + " - " + str(self.panel)
		else:
			return str(self.user_name) + " - " + str(self.panel)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()
	
class ModelPermission(models.Model):
	## fields
	group = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=MyGroup,verbose_name='Grup')
	user_name = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı*')
	model = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=ModelLM,verbose_name='Model Adı')
	permission = models.BooleanField(null=True,blank=True,default=False,verbose_name='Yetki')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='model_permission'
		ordering=["user_name","model"]
	## def 1
	def __str__(self):
		if self.group:
			return str(self.group) + " - " + str(self.model)
		else:
			return str(self.user_name) + " - " + str(self.model)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()
	
class FieldPermission(models.Model):
	## fields
	group = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=MyGroup,verbose_name='Grup')
	user_name = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı*')
	field = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=FieldLM,verbose_name='Model Alanı Adı')
	permission = models.BooleanField(null=True,blank=True,default=False,verbose_name='Yetki')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='field_permission'
		ordering=["user_name","field"]
	## def 1
	def __str__(self):
		if self.group:
			return str(self.group) + " - " + str(self.field)
		else:
			return str(self.user_name) + " - " + str(self.field)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()
	
class PathPermission(models.Model):
	## fields
	group = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=MyGroup,verbose_name='Grup')
	user_name = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı*')
	path = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=PathLM,verbose_name='Güzergah Adı')
	permission = models.BooleanField(null=True,blank=True,default=False,verbose_name='Yetki')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='path_permission'
		ordering=["user_name","path"]
	## def 1
	def __str__(self):
		if self.group:
			return str(self.group) + " - " + str(self.path)
		else:
			return str(self.user_name) + " - " + str(self.path)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class UserPermission(models.Model):
	## fields
	group = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=MyGroup,verbose_name='Grup')
	user_name = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı*')
	model_permission = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=ModelPermission,verbose_name='Kişisel İzinler')
	permission = models.BooleanField(null=True,blank=True,default=False,verbose_name='Yetki')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	## class
	class Meta:
		db_table='user_permission'
		ordering=["user_name","model_permission"]
	## def 1
	def __str__(self):
		return str(self.user_name) + " - " + str(self.model_permission)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class MyUserProfile(models.Model):
	## fields
	user_name = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı*')
	profile_pic = models.CharField(null=True,blank=True,max_length=200,verbose_name='Profil Fotoğrafı')
	corporation = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=CorporationLM,verbose_name='Firma')
	## def 1
	def __str__(self):
		return str(self.user_name) + " - " + str(self.corporation)
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
	## def 4
	def logger_str(self):
		return "[%s] method: %s ,ip: %s,\tpath: %s,\tuser_id: %s,\tsesion_id: %s\t" % (self.action, self.date.strftime("%Y-%m-%d %H:%M:%S"), self.ip, self.web_address, self.user_name_id, self.session)

class UserIp(models.Model):
	## fields
	user_name = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	ip = models.CharField(null=True,blank=True,max_length=50,verbose_name='Ip Adresi')
	permission = models.BooleanField(null=True,blank=True,default=False,verbose_name="Yetki")
	auth_key = models.CharField(null=True,blank=True,max_length=200,verbose_name='Auth Key')
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
	## def 4
	def create_auth_key(self):
		ip_list=self.ip.split(".")
		auth_key_text="%s_%s-%s-%s-%s" % (self.user_name.username,ip_list[0],ip_list[1],ip_list[2],ip_list[3])
		auth_key=make_password(auth_key_text)
		#self.auth_key=auth_key
		return auth_key
	