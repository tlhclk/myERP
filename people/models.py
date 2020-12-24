# -*- coding: utf-8 -*-
### import_part
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from main.models import *
from functions.model import AttrDict
from constant.models import *


### models_part
class Person(models.Model):
	## fields
	code = models.CharField(null=True,blank=True,max_length=5,verbose_name='Kişi Kodu')
	full_name = models.CharField(null=True,blank=True,max_length=100,verbose_name='Tam Adı')
	id_number = models.CharField(null=True,blank=True,max_length=11,verbose_name='Kimlik Numarası')
	first_name = models.CharField(null=True,blank=True,max_length=50,verbose_name='İlk Adı')
	second_name = models.CharField(null=True,blank=True,max_length=50,verbose_name='İkinci Adı')
	middle_name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Ek Adı')
	last_name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Soyadı')
	nickname = models.CharField(null=True,blank=True,max_length=50,verbose_name='Takma Adı')
	title = models.CharField(null=True,blank=True,max_length=50,verbose_name='Ünvanı')
	gender = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=GenderLM,verbose_name='Cinsiyeti')
	group = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=PersonGroupLM,verbose_name='Grubu')
	dateofbirth = models.DateField(null=True,blank=True,default=datetime.today,verbose_name='Doğum Tarihi')
	hometown = models.CharField(null=True,blank=True,max_length=50,verbose_name='Memleketi')
	country = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=CountryLM,verbose_name='Ülkesi')
	city = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=CityLM,verbose_name='İli')
	address = models.CharField(null=True,blank=True,max_length=100,verbose_name='Adresi')
	dateofdeath = models.DateField(null=True,blank=True,verbose_name='Ölüm Tarihi')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	favorite = models.BooleanField(default=False,verbose_name='Favori')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='person_m'
		ordering=["full_name"]
	## def 1
	def __str__(self):
		return str(self.full_name)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class Education(models.Model):
	## fields
	person = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Person,verbose_name='Kim')
	school_type = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=SchoolTypeLM,verbose_name='Okul Tipi')
	school = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=SchoolLM,verbose_name='Okul')
	department = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=DepartmentLM,verbose_name='Bölümü')
	graduation_year = models.CharField(null=True,blank=True,max_length=4,verbose_name='Mezuniyet Yılı')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='education_m'
		ordering=["person"]
	## def 1
	def __str__(self):
		return str(self.school_type) + " - " + str(self.school)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class PersonEmail(models.Model):
	## fields
	person = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Person,verbose_name='Kimin')
	email_type = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=EmailTypeLM,verbose_name='E-Mail Tipi')
	email = models.EmailField(null=True,blank=True,max_length=50,verbose_name='E-Mail Adresi')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='personemail_m'
		ordering=["person"]
	## def 1
	def __str__(self):
		return str(self.email_type) + " - " + str(self.email)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class PersonPhone(models.Model):
	## fields
	person = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Person,verbose_name='Kimin')
	phone_type = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=PhoneTypeLM,verbose_name='Telefon Tipi')
	phone_number = models.CharField(null=True,blank=True,max_length=20,verbose_name='Telefon Numarası')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='personphone_m'
		ordering=["person"]
	## def 1
	def __str__(self):
		return str(self.phone_type) + " - " + str(self.phone_number)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class PersonPhoto(models.Model):
	## fields
	person = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Person,verbose_name='Kimin')
	name = models.CharField(null=True,blank=True,max_length=50,verbose_name='Adı')
	web_address = models.CharField(null=True,blank=True,max_length=200,verbose_name='Fotoğraf Adresi')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='personphoto_m'
		ordering=["person"]
	## def 1
	def __str__(self):
		return str(self.person) + " - " + str(self.desc)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class PersonSocial(models.Model):
	## fields
	person = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Person,verbose_name='Kimin')
	media_type = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=MediaTypeLM,verbose_name='Sosyal Medya Tipi')
	username = models.CharField(null=True,blank=True,max_length=50,verbose_name='Kullanıcı Adı')
	web_address = models.CharField(null=True,blank=True,max_length=100,verbose_name='Adresi')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='personsocial_m'
		ordering=["person"]
	## def 1
	def __str__(self):
		return str(self.media_type) + " - " + str(self.username)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class RelationTree(models.Model):
	## fields
	person = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Person,verbose_name='Kişi')
	relation = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=RelationshipLM,verbose_name='İlişki')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='relationtree_m'
		ordering=["person","relation"]
	## def 1
	def __str__(self):
		return str(self.person) + " - " + str(self.relation)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()

class RelationTreePerson(models.Model):
	## fields
	person = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=Person,verbose_name='Kişi')
	relation_tree = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=RelationTree,verbose_name='İlişki Ağacı')
	desc = models.CharField(null=True,blank=True,max_length=500,verbose_name='Açıklaması')
	user = models.ForeignKey(null=True,blank=True,on_delete=models.SET_NULL,to=User,verbose_name='Kullanıcı')
	## class
	class Meta:
		db_table='relationtree_person'
		ordering=["person","relation_tree"]
	## def 1
	def __str__(self):
		return str(self.person) + " - " + str(self.relation_tree)
	## def 2
	def attr_dict(self,data_type):
		return AttrDict(self).get_attr_dict(data_type)
	## def 3
	def remote_attr_dict(self):
		return AttrDict(self).get_remote_attr_dict()
