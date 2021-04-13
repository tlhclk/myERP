# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.db.models import Q
import datetime,logging
from django.utils.deprecation import MiddlewareMixin
from functions.auth_func import ModelFunc
import datetime as dt
from authentication.models import PathPermission,UserIp,HistoryLog,UserGroup
from main.models import PathLM

request_logger = logging.getLogger('django')

class RequestMessageMiddleware(MiddlewareMixin,ModelFunc):
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
        model=HistoryLog
        last_record=model.objects.create(date=date,time=time,ip=ip,action=method,web_address=path,user_name_id=user_id,session=session,csrftoken=csrftoken)
        message = last_record.logger_str()
        auth=self.ip_check(ip,request.user)
        if auth:
            request_logger.info(message)
        else:
            request_logger.info(message+" ://unauthorized_ip")
        
    def ip_check(self,ip,user):
        model=UserIp
        if user.is_anonymous:
            obj_list=model.objects.filter(ip=ip)
            for obj in obj_list:
                if obj.user_name.is_superuser:
                    return True
        else:
            obj_list=model.objects.filter(ip=ip).filter(user_name=user)
            for obj in obj_list:
                if obj.permission:
                    return True
        return False
            
    def process_response(self,request,response):
        ip = request.META["REMOTE_ADDR"]
        path = request.META["PATH_INFO"].split("?")[0]
        valid_pages=["/404", "/500", "/400", "/300", "/", "/register/", "/login/","/register_validation/","/password_reset/","/password_reset/done/","/password_change/","/password_change/done/","/reset/done/","/logout/"]
        if path in valid_pages:
            if not request.user.is_anonymous:
                if path=="/register/" or path=="/login/":
                    return redirect("/home")
            return response
        else:
            auth=self.ip_check(ip,request.user)
            if auth==True and request.user.is_authenticated:
                return response
            else:
                return redirect("/?warning=unauthorized_ip")
