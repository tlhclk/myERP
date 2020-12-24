# -*- coding: utf-8 -*-
from django.shortcuts import redirect
import datetime,logging
from django.utils.deprecation import MiddlewareMixin
import functions.auth_func as af
import datetime as dt
from authentication.models import PersonalPermission
from main.models import PathLM

request_logger = logging.getLogger('django')

class RequestMessageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if "sessionid" in request.COOKIES:
            session = request.COOKIES["sessionid"]
        else:
            session = None
        if "csrftoken" in request.COOKIES:
            csrftoken = request.COOKIES["csrftoken"]
        else:
            csrftoken = None
        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            user_id = None
        ip = request.META["REMOTE_ADDR"]
        path = request.META["PATH_INFO"]
        method = request.method
        date=dt.datetime.now()
        time=dt.datetime.now()
        model_obj,model=af.get_model("HistoryLog")
        model.objects.create(date=date,time=time,ip=ip,action=method,web_address=path,user_name_id=user_id,session=session,csrftoken=csrftoken)
        message = "[%s] method: %s ,ip: %s,\tpath: %s,\tuser_id: %s,\tsesion_id: %s\t" % (method,date.strftime("%Y-%m-%d %H:%M:%S"),ip, path, user_id, session)
        if not self.ip_check(ip):
            request_logger.info(message+" ://Unauthorizated IP")
        else:
            request_logger.info(message)
        
    def ip_check(self,ip):
        model_obj,model=af.get_model("UserIp")
        obj_list=model.objects.filter(ip=ip)
        if len(obj_list)>0:
            return True
        else:
            return False
    
    def process_response(self,request,response):
        ip = request.META["REMOTE_ADDR"]
        path = request.META["PATH_INFO"].split("?")[0]
        if not self.ip_check(ip):
            if path=="/" or path=="/login" or "/authentication/grant/user/ip/" in path:
                return response
            else:
                return redirect("/?warning=unauthorizated_ip")
        else:
            if path=="/" or path=="/login" or "/authentication/grant/user/ip/" in path:
                return response
            else:
                return response
                #if self.permission_check(request.user,path):
                #    return response
                #else:
                #    return redirect("/?warning=unauthorizated_user")

    def parse_path(self,path):
        path_list=path.split("/")
        ability=path_list[1]
        if "list" == ability:
            m_name=path_list[2]
            id_no = None
            extra_text=path_list[3]
        elif "detail" == ability:
            m_name=path_list[2]
            id_no=path_list[3]
            if len(path_list)>4:
                extra_text=path_list[4]
            else:
                extra_text = None
        elif "add" == ability:
            m_name=path_list[2]
            id_no = None
            extra_text=path_list[3]
        elif "delete" == ability:
            m_name=path_list[2]
            id_no=path_list[3]
            if len(path_list)>4:
                extra_text=path_list[4]
            else:
                extra_text = None
        elif "update" == ability:
            m_name=path_list[2]
            id_no=path_list[3]
            if len(path_list)>4:
                extra_text=path_list[4]
            else:
                extra_text = None
        elif "media" == ability:
            m_name=path_list[2]
            id_no=path_list[3]
            if len(path_list)>4:
                extra_text=path_list[4]
            else:
                extra_text = None
        elif "static" == ability:
            m_name=path_list[2]
            id_no=path_list[3]
            if len(path_list)>4:
                extra_text=path_list[4]
            else:
                extra_text = None
        else:
            path_object_list=PathLM.objects.filter(location=path.split("?")[0])
            if len(path_object_list)>0:
                m_name=path_object_list[0].panel.name
                id_no=path_object_list[0].path
                ability=path_object_list[0].type
                if "?" in path:
                    extra_text = "?" + path.split("?")[1]
                else:
                    extra_text = None
            else:
                m_name=None
                id_no = None
                ability = None
                extra_text=None
        return m_name,id_no,extra_text,ability

    def permission_check(self,user,path):
        m_name,id_no,extra_text,ability = self.parse_path(path)
        if user!=None and str(user)!="AnonymousUser":
            if ability!=None:
                if ability=="function":
                    permision_list = PersonalPermission.objects.filter(user=user,desc=m_name)
                elif ability=="report":
                    permision_list = PersonalPermission.objects.filter(user=user, desc=m_name)
                else:
                    permision_list = PersonalPermission.objects.filter(user=user, model__name=m_name)
            else:
                return False
        else:
            return False
        if len(permision_list)>0:
            return True
        else:
            if user.is_superuser:
                return True
            else:
                return False