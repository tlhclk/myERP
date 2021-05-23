# -*- coding: utf-8 -*-
from django import forms
from .models import *
from constant.models import TransactionCategoryLM,TransactionTypeLM
from people.models import Person
from calendarr.models import RepetitiveRecord
import datetime as dt
from functions.auth_func import ModelQueryset

class MultiTransactionAddForm(forms.Form):
	
	account=forms.ModelChoiceField(queryset=Account.objects.all(),empty_label="Hesap",label="Hesap",widget=forms.Select(attrs={"class":"form-control select2"}))
	date=forms.DateField(input_formats=["%Y-%m-%d"],initial=dt.datetime.today(),label="Tarih",widget=forms.DateInput(attrs={"class":"form-control datetimepicker date","data-toggle":"datetimepicker","data-target":"#id_date"},format="%Y-%m-%d"))
	time=forms.TimeField(input_formats=["%H:%M"],initial=dt.datetime.now(),label="Zaman",widget=forms.DateInput(attrs={"class":"form-control datetimepicker time","data-toggle":"datetimepicker","data-target":"#id_time"},format="%H:%M"))
	category=forms.ModelChoiceField(queryset=TransactionCategoryLM.objects.all(),empty_label="Kategori",label="Kategori",widget=forms.Select(attrs={"class":"form-control select2"}))
	corporation=forms.ModelChoiceField(queryset=CorporationLM.objects.all(),empty_label="Firma",label="Firma",widget=forms.Select(attrs={"class":"form-control select2"}))
	desc=forms.CharField(label="Açıklama",widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
	tr_type=forms.ModelChoiceField(queryset=TransactionTypeLM.objects.all(),empty_label="İşlem Tipi",label="İşlem Tipi",widget=forms.Select(attrs={"class":"form-control select2"}))
	amount=forms.DecimalField(label="Miktar",widget=forms.NumberInput(attrs={"class":"form-control"}))
	person=forms.ModelChoiceField(queryset=Person.objects.all(),empty_label="Kişi",label="Kişi",widget=forms.Select(attrs={"class":"form-control select2"}),required=False)
	change=forms.ModelChoiceField(queryset=Change.objects.filter(is_active=True),empty_label="Aldım - Verdim",label="Aldım - Verdim",widget=forms.Select(attrs={"class":"form-control select2"}),required=False)
	repetitive_record=forms.ModelChoiceField(queryset=RepetitiveRecord.objects.filter(is_active=True),empty_label="Tekrarlı İşlem Kaydı",label="Tekrarlı İşlem Kaydı",widget=forms.Select(attrs={"class":"form-control select2"}),required=False)
	
	class Meta:
		fields=["account","date","time","category","corporation","desc","type","amount","person","change","repetitive_record",]
	
	def transaction_save(self):
		account=self.cleaned_data["account"]
		date=self.cleaned_data["date"]
		time=self.cleaned_data["time"]
		category=self.cleaned_data["category"]
		corporation=self.cleaned_data["corporation"]
		desc=self.cleaned_data["desc"]
		tr_type=self.cleaned_data["tr_type"]
		amount=self.cleaned_data["amount"]
		person=self.cleaned_data["person"]
		if person!=None:
			if len(desc)>0:
				desc+=" - "+str(person)
			else:
				desc=str(person)
		if tr_type.id==1:
			account_amount = account.amount - amount
		else:
			account_amount = account.amount + amount
		account.amount=account_amount
		account.save()
		new_transaction=Transaction.objects.create(account=account,date=date,time=time,category=category,corporation=corporation,desc=desc,type=tr_type,amount=amount,account_amount=account_amount)
		return new_transaction
	
	def change_save(self,transaction):
		change=self.cleaned_data["change"]
		if change!=None and transaction!=None:
			new_change=ChangeTransaction.objects.create(change=change,transaction=transaction)
			return new_change
		return None
	
	def repetitive_record_save(self,transaction):
		repetitive_record=self.cleaned_data["repetitive_record"]
		if repetitive_record!=None:
			repetitive_record.transaction=transaction
			repetitive_record.is_active=False
			repetitive_record.save()
			self.create_new_repetitive_record(repetitive_record)
			return repetitive_record
		return None
	
	def create_new_repetitive_record(self,record):
		new_record=RepetitiveRecord()
		new_record.repetitive=record.repetitive
		new_record.start_date=self.get_record_new_date(record.start_date,record.repetitive.period_rate,int(record.repetitive.period_amount))
		new_record.end_date=self.get_record_new_date(record.end_date,record.repetitive.period_rate,int(record.repetitive.period_amount))
		new_record.last_date=self.get_record_new_date(record.last_date,record.repetitive.period_rate,int(record.repetitive.period_amount))
		new_record.amount=self.get_record_new_amount(int(record.amount),record.repetitive.period_rate,int(record.repetitive.period_amount))
		new_record.is_active=True
	
	def get_record_new_date(self,date,rep_type,rep_count):
		if rep_type.id==1:#yıllık
			return dt.datetime(year=date.year+rep_count,month=date.month,day=date.day)
		elif rep_type.id==2:#aylik
			if date.month+rep_count>12:
				year_sum=(rep_count+12)//12
				month_sum=(rep_count+12)%12
				return dt.datetime(year=date.year + year_sum, month=month_sum, day=date.day)
			else:
				return dt.datetime(year=date.year,month=date.month+rep_count,day=date.day)
		elif rep_type.id==3:#hafta
			return date+dt.timedelta(days=7*rep_count)
		elif rep_type.id==4:#gün
			return date+dt.timedelta(days=rep_count)
		else:
			return None
	
	def get_record_new_amount(self,amount,rep_type,rep_count):
		if rep_type.id==6:#km
			return amount+rep_count
		else:
			return None