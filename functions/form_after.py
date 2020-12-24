# -*- coding: utf-8 -*-
from django.shortcuts import redirect,reverse
import datetime as dt
import functions.model as mdl
import functions.auth_func as af
from django.apps import apps
from operator import attrgetter as atg


class TransactionFormAfter:
    ability=None
    category=None
    object=None
    person=None
    pk=None
    ability_list=["detail","list","delete","add","update"]
    def __init__(self,request):
        self.request=request
        self.tra_obj,self.tra_model=af.get_model("Transaction")
        self.parse_href()
        self.get_object()
        self.parse_desc()
            
    def parse_href(self):
        if "HTTP_REFERER" in self.request.META:
            prev_href=self.request.META["HTTP_REFERER"].split("/")
            self.ability=prev_href[3]
            if self.ability=="detail" or self.ability=="update" or self.ability=="delete":
                self.pk=prev_href[5]
    
    def get_object(self):
        if self.pk!=None:
            self.object=self.tra_model.objects.get(pk=self.pk)
        else:
            self.object=sorted(af.get_queryset(self.request.user,self.tra_obj.name,"Add"),key=atg("id"))[-1]
    
    def parse_desc(self):
        person_obj,person_model=af.get_model("Person")
        person_list=person_model.objects.filter(user=self.request.user)
        if self.object!=None:
            if self.object.desc!=None:
                desc_list=self.object.desc.split("-")
                for item in desc_list:
                    people_filter=person_list.filter(full_name__contains=item.strip())
                    if len(people_filter)==1:
                        self.person=people_filter[0]
                        break
                
    def account_revise(self,amount_dict):
        account_obj,account_model=af.get_model("Account")
        for id_no in amount_dict:
            account = account_model.objects.get(pk=id_no)
            if account.is_active == True:
                account.amount = amount_dict[id_no]
                account.save()

    def set_new_amount(self):
        if self.ability == "add":
            if self.object.type == 1:
                self.object.account_amount = float(self.object.account.amount) + float(self.object.amount)
            else:
                self.object.account_amount = float(self.object.account.amount) - float(self.object.amount)
            self.object.save()
            return {self.object.account.id: float(self.object.account_amount)}
        elif self.ability == "update":
            #return build_transaction_history([self.object.account])
            return {}
        elif self.ability == "delete":
            return {}
            
    def repetitiverecord_direction(self):
        rep_obj,rep_model=af.get_model("Repetitive")
        reprec_obj,reprec_model=af.get_model("RepetitiveRecord")
        repetitive_list = rep_model.objects.filter(code=self.object.desc.strip()).filter(user=self.request.user)
        if len(repetitive_list)==1:
            return redirect("global_list",m_name=reprec_obj.name,kwargs={"repetitive":repetitive_list[0].id,"is_active":True,"search":""})
        else:
            if self.person!=None:
                return redirect("global_list", m_name=reprec_obj.name,kwargs={"person":self.person.id,"corporation":self.object.corporation.id,"is_active":True,"search":""})
            else:
                return redirect("global_list", m_name=reprec_obj.name,kwargs={"corporation":self.object.corporation.id,"is_active":True,"search":""})
    
    def change_direction(self):
        change_obj,change_model=af.get_model("Change")
        if self.object.category.id==49:
            if self.person!=None:
                opt_param={"person":self.person.id,"purpose":6, "transaction": self.object.id}
            else:
                opt_param={"purpose": 6, "transaction": self.object.id}
        else:
            if self.object.category.id==40:
                if self.object.corporation.id==154:
                    if self.person!=None:
                        opt_param={"person":self.person.id,"transaction":self.object.id}
                    else:
                        opt_param={"transaction": self.object.id}
                else:
                    opt_param={"transaction": self.object.id}
            else:
                opt_param={"transaction": self.object.id}
        base_href=reverse("global_add", args=[change_obj.name])
        param_list=["%s=%s" %(key,value) for key,value in opt_param.items()]
        if len(param_list)>0:
            param_href="?%s" % ("&".join(param_list))
        else:
            param_href=""
        return redirect(base_href+param_href)
            
    def get_direction(self):
        last_amount = self.set_new_amount()
        self.account_revise(last_amount)
        if self.object.category.id==16:
            return self.repetitiverecord_direction()
        #elif self.object.category.id==49 or self.object.category.id==40:
            #return self.change_direction()
        else:
            if self.ability=="add":
                return redirect("global_detail",m_name=self.tra_obj.name,pk=self.object.id)
            if self.ability=="update":
                return redirect("global_detail",m_name=self.tra_obj.name,pk=self.object.id)
            else:
                return redirect("global_list",m_name=self.tra_obj.name)
        
class RepetitiveRecordFormAfter:
    ability=None
    pk=None
    object=None
    ability_list=["detail","list","delete","add","update"]
    def __init__(self,request):
        self.request=request
        self.rep_obj,self.rep_model=af.get_model("Repetitive")
        self.reprec_obj,self.reprec_model=af.get_model("RepetitiveRecord")
        self.parse_href()
        self.get_object()
        
    def parse_href(self):
        if "HTTP_REFERER" in self.request.META:
            prev_href=self.request.META["HTTP_REFERER"].split("/")
            self.ability=prev_href[3]
            if self.ability=="detail" or self.ability=="update" or self.ability=="delete":
                self.pk=prev_href[5]
                
    def get_object(self):
        if self.pk!=None:
            self.object=self.reprec_model.objects.get(pk=self.pk)
        else:
            self.object=sorted(af.get_queryset(self.request.user,self.reprec_obj.name,"Add"),key=atg("id"))[-1]
        
    def get_direction(self):
        last_obj=self.reprec_model.objects.filter(repetitive=self.object.repetitive).order_by("last_date").last()
        if last_obj.is_active==False and int(last_obj.repetitive.period_rate.day)>0:
            period_time = self.get_additional_time()
            new_record = self.reprec_model.objects.create(
                repetitive=self.object.repetitive,
                start_date=self.object.start_date + period_time,
                end_date=self.object.end_date + period_time,
                last_date=self.object.last_date + period_time,
                user=self.object.user
            )
            return redirect("global_detail", m_name="RepetitiveRecord", pk=new_record.id)
        else:
            return redirect("global_detail", m_name="RepetitiveRecord", pk=last_obj.id)
        
    def get_additional_time(self):
        period_amount=self.object.repetitive.period_amount
        period_rate=self.object.repetitive.period_rate.day
        day=float(period_amount)*float(period_rate)
        return dt.timedelta(days=day)

class CloneForm:
    def __init__(self,request):
        self.request=request
    
    def start_flow(self):
        object=self.get_object()
        initial_dict=self.get_initials(object)
        model_name=object.__clas__.__name__
        return redirect("global_detail", m_name=model_name,kwargs=initial_dict)
        
    def get_attr_dict(self,object):
        return mdl.AttrDict(object).get_attr_dict("form_add")
    
    def get_initials(self,object):
        initial_dict={}
        attr_dict=self.get_attr_dict(object)
        for field_name in attr_dict:
            if len(attr_dict[field_name])==3:
                if attr_dict[field_name][2]=="":
                    initial_dict[field_name]=attr_dict[field_name][0]
                else:
                    initial_dict["%s_id" % field_name]=attr_dict[field_name][0].id
        return initial_dict

    def get_object(self):
        previous_url=self.request.META["HTTP_REFERER"]
        url_list=previous_url.split("/")
        if url_list[3]=="detail" or url_list[3]=="update":
            pk=int(url_list[-2])
            model_obj,model_class=af.get_model(url_list[4])
            return model_class.objects.get(pk=pk)
        else:
            return None
        
        
class MultiTransactionFormAfter:
    pass