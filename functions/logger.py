# -*- coding: utf-8 -*-
from django.shortcuts import redirect
import datetime,logging
from django.utils.deprecation import MiddlewareMixin
from functions.auth_func import ModelFunc
import datetime as dt
from authentication.models import ModelPermission
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
        model=self.get_model("HistoryLog")
        last_record=model.objects.create(date=date,time=time,ip=ip,action=method,web_address=path,user_name_id=user_id,session=session,csrftoken=csrftoken)
        message = last_record.logger_str()
        auth=self.ip_check(ip,request.user)
        if auth =="NoIPNoUser":
            pass
            request_logger.info(message+" ://NoIPNoUser")
        elif auth =="NoIP":
            pass
            request_logger.info(message+" ://NoIP")
        elif auth =="NoUser":
            pass
            request_logger.info(message+" ://NoUser")
        elif auth =="NoUserNoIP":
            pass
            request_logger.info(message+" ://NoUserNoIP")
        elif auth:
            request_logger.info(message)
        else:
            request_logger.info(message+" ://denied_permission")
        
    def ip_check(self,ip,user):
        model=self.get_model("UserIp")
        obj_ip_list=model.objects.filter(ip=ip)
        if user.is_anonymous:
            obj_user_list=[]
            obj_list=[]
        else:
            obj_user_list=model.objects.filter(user_name=user)
            obj_list=model.objects.filter(user_name=user).filter(ip=ip)
        authority_types=["NoIP","NoUser","NoIPNoUser"]
        error_types=[]
        if len(obj_user_list)==0:
            error_types.append("NoUser")
        if len(obj_ip_list)==0:
            error_types.append("NoIP")
        if len(obj_list)==0 and len(obj_ip_list)==0:
            error_types.append("NoIPNoUser")

        if "NoIPNoUser" in error_types:
            return "NoIPNoUser"
        else:
            if "NoUser" in error_types:
                if "NoIp" in error_types:
                    return "NoUserNoIP"
                else:
                    return "NoUser"
            else:
                if "NoIp" in error_types:
                    return "NoIP"
                else:#user ve ip var
                    for obj in obj_list:
                        if obj.permission:
                            return True
                    return False
    
    def process_response(self,request,response):
        ip = request.META["REMOTE_ADDR"]
        path = request.META["PATH_INFO"].split("?")[0]
        auth=self.ip_check(ip,request.user)
        valid_pages=["/404", "/500", "/400", "/300", "/", "/register/", "/login/","/register_validation/","/password_reset/","/password_reset/done/","/password_change/","/password_change/done/","/reset/done/","/logout/"]
        if path in valid_pages:
            if not request.user.is_anonymous:
                if path=="/register/" or path=="/login/":
                    return redirect("/home")
            return response
        if auth == "NoIPNoUser":
            return redirect("/register/?warning=NoIPNoUser")
        elif auth == "NoUser" or auth == "NoIP" or auth == "NoUserNoIP":
            return redirect("/login/?warning=NoUser")
        elif auth:
            return response
        else:
            return redirect("/?warning=denied_permission")

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
        if user!=None and not user.is_anonymous:
            if ability!=None:
                if ability=="function":
                    permision_list = ModelPermission.objects.filter(user=user,desc=m_name)
                elif ability=="report":
                    permision_list = ModelPermission.objects.filter(user=user, desc=m_name)
                else:
                    permision_list = ModelPermission.objects.filter(user=user, model__name=m_name)
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
            
            
            
            
