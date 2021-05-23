# -*- coding: utf-8 -*-
from django.core.mail import EmailMessage


class MailService:
	def __init__(self,from_email):
		self.my_email=EmailMessage()
		self.my_email.from_email=from_email
	
	def set_recipient_list(self,recipient_list):
		self.my_email.to=recipient_list
		
	def set_subject(self,subject):
		self.my_email.subject=subject
	def set_body(self,body):
		self.my_email.body=body
	def set_cc(self,cc):
		self.my_email.cc=cc
	def set_bcc(self,bcc):
		self.my_email.bcc=bcc
	def set_connection(self,connection):
		self.my_email.connection=connection
	def set_attachment(self,attachment):
		self.my_email.attach_file(attachment)
	def set_headers(self,headers):
		self.my_email.headers=headers
	def set_reply_to(self,reply_to):
		self.my_email.reply_to=reply_to
	def message(self):
		return self.my_email.message()
	
	def send_email(self):
		self.my_email.send()
#
#
# class PermissionControl(ModelFunc):
# 	def __init__(self):
# 		super(PermissionControl, self).__init__()
# 		self.panel_perm_model = apps.get_model("authentication", "PanelPermission")
# 		self.model_perm_model = apps.get_model("authentication", "ModelPermission")
# 		self.path_perm_model = apps.get_model("authentication", "PathPermission")
# 		self.group_model = apps.get_model("authentication", "MyGroup")
# 		self.user_group_model = apps.get_model("authentication", "UserGroup")
# 		self.user_profile_model = apps.get_model("authentication", "MyUserProfile")
#
# 	def PanelCheck(self, user, panel_obj):
# 		if type(panel_obj) == str:
# 			panel_obj = self.get_panel(panel_obj)
# 		if type(panel_obj) == self.panel_model:
# 			perm_list = self.panel_perm_model.objects.filter(user_name=user).filter(panel=panel_obj)
# 			if len(perm_list) == 1:
# 				perm = perm_list[0]
# 				if perm.permission == True:
# 					return True
# 				else:
# 					print("Panel Yetki Yok %s" % perm)
# 			else:
# 				print("Panel Yetkisi Bulunamadı %s" % panel_obj)
# 		else:
# 			print("Panel Bulunamadı(PanelCheck) %s" % panel_obj)
# 		return False
#
# 	def ModelCheck(self, user, model_obj):
# 		if type(model_obj) == str:
# 			model_obj = self.get_model(model_obj)
# 		if type(model_obj) == self.model_model:
# 			perm_list = self.model_perm_model.objects.filter(user_name=user).filter(model=model_obj)
# 			if len(perm_list) == 1:
# 				perm = perm_list[0]
# 				if perm.permission == True:
# 					return True
# 				else:
# 					print("Model Yetki Yok %s" % perm)
# 			else:
# 				print("Model Yetkisi Bulunamadı %s" % model_obj)
# 		else:
# 			print("Model Bulunamadı %s" % model_obj)
# 		return False
#
# 	def PathCheck(self, user, path_obj):
# 		if type(path_obj) == str:
# 			path_obj = self.get_path(path_obj)
# 		if type(path_obj) == self.path_model:
# 			perm_list = self.path_perm_model.objects.filter(user_name=user).filter(path=path_obj)
# 			if len(perm_list) == 1:
# 				perm = perm_list[0]
# 				if perm.permission == True:
# 					return True
# 				else:
# 					print("Güzergah Yetki Yok %s" % perm)
# 			else:
# 				print("Güzergah Yetkisi Bulunamadı %s" % path_obj)
# 		else:
# 			print("Güzergah Bulunamadı %s" % path_obj)
# 		return False
#
# 	def GroupCheck(self, user, group_obj):
# 		if type(group_obj) == str:
# 			group_obj = self.get_group_obj(group_obj, self.get_user_corporation(user))
# 		if type(group_obj) == self.group_model:
# 			perm_list = self.user_group_model.objects.filter(user_name=user).filter(group=group_obj)
# 			if len(perm_list) > 0:
# 				return True
# 			else:
# 				if group_obj.id != 3:
# 					print("Group Yetki Yok %s" % group_obj)
# 		else:
# 			print("Grup Bulunamadı(GroupCheck) %s" % group_obj)
# 		return False
#
# 	def get_group_obj(self, g_name, corporation):
# 		if type(g_name) == str:
# 			group_list = self.group_model.objects.filter(name=g_name).filter(corporation=corporation)
# 			if len(group_list) == 1:
# 				return group_list[0]
# 		print("Grup Bulunamadı(Group Obj) %s" % g_name)
# 		return None
#
# 	def get_user_corporation(self, user):
# 		profile_list = self.user_profile_model.objects.filter(user_name=user)
# 		if len(profile_list) == 1:
# 			profile = profile_list[0]
# 			return profile.corporation
# 		print("Profil Bulunamadı %s" % user)
# 		return None
#