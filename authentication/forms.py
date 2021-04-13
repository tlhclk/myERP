# -*- coding: utf-8 -*-
from django import forms
from .models import UserIp
import datetime as dt
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

UserModel = get_user_model()


class RegisterForm(forms.Form):
	email=forms.EmailField(label="E-Mail",widget=forms.EmailInput(attrs={"class":"form-control"}),required=True)
	username=forms.CharField(label="Kullanıcı Adı",widget=forms.TextInput(attrs={"class":"form-control"}),required=True)
	first_name=forms.CharField(label="Adı",widget=forms.TextInput(attrs={"class":"form-control"}),required=True)
	last_name=forms.CharField(label="Soyadı",widget=forms.TextInput(attrs={"class":"form-control"}),required=True)
	password=forms.CharField(label="Şifre",widget=forms.PasswordInput(attrs={"class":"form-control"}),required=True)
	
	class Meta:
		fields=["email","username","first_name","last_name","password"]
		
	def clean_email(self):
		email = self.cleaned_data['email']
		email_list = UserModel.objects.filter(email=email)
		if len(email_list)>0:
			raise ValidationError("Girdiğiniz Mail Adresi Kayıtlı!")
		return email
	
	def clean_username(self):
		username = self.cleaned_data["username"]
		username_list = UserModel.objects.filter(username=username)
		if len(username_list)>0:
			raise ValidationError("Girdiğiniz Kullanıcı Adı Kayıtlı!")
		return username
	
	def clean_password(self):
		password = self.cleaned_data["password"]
		int_list=["0","1","2","3","4","5","6","7","8","9"]
		l_str_list=["q","w","e","r","t","y","u","ı","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"]
		b_str_list=["Q","W","E","R","T","Y","U","I","O","P","L","K","J","H","G","F","D","S","A","Z","X","C","V","B","N","M"]
		sym_list=["_","-","*","+","?",".","/"]
		int_c=0
		l_str_c=0
		b_str_c=0
		sym_c=0
		for l in password:
			if l in int_list:
				int_c+=1
			if l in l_str_list:
				l_str_c+=1
			if l in b_str_list:
				b_str_c+=1
			if l in sym_list:
				sym_c+=1
		if int_c==0 or l_str_c==0 or b_str_c==0 or sym_c==0 or len(password)<8:
			raise ValidationError("Lütfen en az 1 rakam, en az 1 küçük harf, en az 1 büyük harf, en az 1 sembol (_-*+?./) ve en az 8 haneli bir şifre giriniz")
		return password
	
	def save(self,ip):
		email = self.cleaned_data["email"]
		username = self.cleaned_data["username"]
		first_name = self.cleaned_data["first_name"]
		last_name = self.cleaned_data["last_name"]
		password = self.cleaned_data["password"]
		user=UserModel.objects.create(username=username,email=email,password=make_password(password),first_name=first_name,last_name=last_name,is_superuser=False,is_active=False,is_staff=False)
		new_user_ip=UserIp.objects.create(user_name=user,ip=ip,permission=False)
		auth_key=new_user_ip.create_auth_key()
		new_user_ip.auth_key=auth_key
		new_user_ip.save()
		#send_ip_validation_mail(user,auth_key,ip)
		
		