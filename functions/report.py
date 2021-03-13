# -*- coding: utf-8 -*-
import datetime as dt
from django.db.models import *
from django.http import JsonResponse
from calendarr.models import *
from people.models import *
from series.models import *
from django.utils.safestring import SafeString
from functions.auth_func import ModelQueryset


class SeriesReport:
    def __init__(self,request):
        self.request=request
    
    def get_series_data(self):
        header_list=["SeriesTypeLM","main_name","name","second_name","web_address","start_date","current_eps","total_eps","rate","SeriesDownloadLM"]
        label_list=["Seri Tipi","Ana AdÄ±","AdÄ±","Ä°kinci AdÄ±","Web Adresi","YayÄ±n Tarihi","Mevcut BÃ¶lÃ¼m","Toplam BÃ¶lÃ¼m","PuanÄ±","Ä°ndirilebilirliÄŸi"]
        series_list=self.get_series_list()
        series_data=[]
        for series in series_list:
            temp_data=[]
            for header in header_list:
                temp_data.append(getattr(series,header))
            series_data.append(tuple(temp_data))
        return JsonResponse({"series_data":series_data,"label_list":label_list})
    
    def get_state(self):
        if "status" in self.request.GET:
            status_value=self.request.GET.get("status")
        else:
            status_value=None
        return status_value
    
    def get_object_list(self,m_name):
        mq=ModelQueryset(self.request)
        return mq.get_queryset(m_name)
            
    def get_series_list(self):
        state=self.get_state()
        object_list=self.get_object_list("Series")
        if state is not None:
            series_list=object_list.filter(state=state)
        else:
            series_list=object_list
        return series_list
        
    def get_related_series(self,series):
        series_list=Series.objects.filter(user=self.request.user).filter(main_name=series.main_name)
        return series_list

class CalendarrReport:
    def __init__(self,request,*args,**kwargs):
        self.request=request
        self.args=args
        self.kwargs=kwargs
    
    def get_object_list(self,m_name):
        mq=ModelQueryset(self.request)
        return mq.get_queryset(m_name)

    def get_repetitiverecord_data(self):
        repetitiverecord_list=self.get_object_list("RepetitiveRecord").filter(transaction__isnull=True).filter(repetitive__is_active=True)
        return repetitiverecord_list
        
    def get_comingevent_data(self):
        comingevent_list=self.get_object_list("Event").filter(date__gte=dt.datetime.today())
        return comingevent_list

class TransactionReport:
    ability="List"
    data="amount"
    def __init__(self,request,**kwargs):
        self.request=request
        self.user=request.user
        self.exclude_dict={"corporation_id__in":[],"category_id__in":[40]}
        self.filter_dict = {}
        self.kwargs=kwargs
        self.param_dict={}
        for item in request.GET:
            self.param_dict[item]=request.GET[item]
            
    def get_date(self,today=None):
        if today!=None:
            if today.day<6:
                date=dt.datetime(today.year,today.month-1,5)
            else:
                date=dt.datetime(today.year,today.month,5)
            return date
        else:
            today=dt.datetime.today()
            if today.day<6:
                date=dt.datetime(today.year,today.month-1,5)
            else:
                date=dt.datetime(today.year,today.month,5)
            return date
        
    def get_filter_data(self):
        self.filter_dict={"date__gte":self.get_date(),"type_id":int(self.param_dict["type_id"])}
        filter_data=Q()
        for key1,value1 in self.filter_dict.items():
            filter_data&=Q(("%s" % key1 ,value1))
        exclude_data=Q()
        for key,value in self.exclude_dict.items():
            exclude_data |= Q(("%s" % key ,value))  # dahil olmayamn idler
        return filter_data,exclude_data
    
    def get_object_list(self,m_name):
        mq=ModelQueryset(self.request)
        return mq.get_queryset(m_name)
    
    def group_info(self):
        filter_data,exclude_data=self.get_filter_data()
        object_list=self.get_object_list("Transaction").filter(filter_data).exclude(exclude_data)
        info_dict={}
        for obj in object_list:
            gr=getattr(obj,self.param_dict["field"])
            if gr not in info_dict:
                info_dict[gr]=[obj]
            else:
                info_dict[gr] += [obj]
        result_list=[]
        for key, value_list in info_dict.items():
            sum_amount = 0.0
            for value in value_list:
                sum_amount += float(getattr(value, self.data))
            result_list.append((key.id,str(key),sum_amount))
        result_list=sorted(result_list,key=lambda tup:tup[2],reverse=True)[:10]
        return result_list
    
    def gather_info(self):
        group_info=self.group_info()
        id_list=[]
        name_list=[]
        data_list=[]
        link_list=[]
        for item  in group_info:
            id_list.append(item[0])
            name_list.append(item[1])
            data_list.append(item[2])
            link_list.append(item[2])
        return id_list,name_list,data_list
    
    def get_rep_model(self):
        field=FieldLM.objects.filter(model_id=10,name=self.param_dict["field"])[0]
        return field.to
    
class AccountReport:
    def __init__(self,request,**kwargs):
        self.request=request
        self.kwargs=kwargs

    def get_object_list(self, m_name):
        mq = ModelQueryset(self.request)
        return mq.get_queryset(m_name)
    
    def gather_info(self):
        object_list = self.get_object_list("Account").filter(is_active=True)
        result_list=[]
        for obj in object_list:
            result_list.append((obj.id,str(obj),obj.amount))
        result_list=sorted(result_list,key=lambda tup:tup[2],reverse=True)[:10]
        id_list = []
        name_list = []
        data_list = []
        for item in result_list:
            id_list.append(item[0])
            name_list.append(item[1])
            data_list.append(item[2])
        return id_list, name_list, data_list

    def get_rep_model(self):
        return "Account"
    
class PeopleReport:
    def __init__(self,request):
        self.request=request
        self.related_list=[]
        self.people_relation_dict={}

    def get_object_list(self, m_name):
        mq = ModelQueryset(self.request)
        return mq.get_queryset(m_name)

    def get_favorites_data(self):
        people_list=self.get_object_list("Person").filter(favorite=True)
        fav_list=[]
        for person in people_list:
            photo_url=PersonPhoto.objects.filter(person=person)
            if len(photo_url)>0:
                fav_list.append((person,photo_url[0].web_address))
            else:
                fav_list.append((person, False))
        return fav_list
    
    def get_relation_data_advanced(self,person):
        result_dict={}
        p_rel=self.get_primal_relations(person)
        self.people_relation_dict[person]=p_rel
        for pr in self.related_list:
            if pr not in self.people_relation_dict:
                p_rel2=self.get_primal_relations(pr)
                self.people_relation_dict[pr]=p_rel2
        for pr2 in self.related_list:
            if pr2 not in self.people_relation_dict:
                p_rel3=self.get_primal_relations(pr2)
                self.people_relation_dict[pr2]=p_rel3
        return result_dict
            
            
    def get_reverse_relation(self,r_id):
        reverse_dict={36:38,37:37,38:36,39:39,12:12,11:11}
        return RelationshipLM.objects.get(pk=reverse_dict[r_id])
    
    def get_relation(self,r_id):
        return RelationshipLM.objects.get(pk=r_id)
    
    def get_basic_relation(self,rel,pr,bd):
        r_id=rel.id
        gender=pr.gender.id
        if r_id == 36: #Ebeveyn
            if gender==1: # Baba
                return self.get_relation(1)
            else: # Anne
                return self.get_relation(2)
        elif r_id == 38: # Evlat
            if gender==1: # Erkek Çocuk
                return self.get_relation(4)
            else: # Kız Çocuk
                return self.get_relation(3)
        elif r_id == 39: # Eş
            if gender==1: # Koca
                return self.get_relation(9)
            else: # Karı
                return self.get_relation(10)
        elif r_id == 37: # Kardeş
            if gender==1: # Erkek
                if bd: # Abi
                    return self.get_relation(8)
                else: # Erkek Kardeş
                    return self.get_relation(6)
            else: # Kız
                if bd: # Abla
                    return self.get_relation(7)
                else: # Kız Kardeş
                    return self.get_relation(5)
        else:
            return rel
    
    def get_indirect_relations(self,person):
        relation_dict={}
        indirect_relation_list=RelationTreePerson.objects.filter(person=person)
        for indirect_relation in indirect_relation_list:
            rel=indirect_relation.relation_tree.relation
            rev_rel=self.get_reverse_relation(rel.id)
            if rev_rel not in relation_dict:
                pr= indirect_relation.relation_tree.person
                if pr not in self.related_list:
                    self.related_list.append(pr)
                    relation_dict[self.get_basic_relation(rev_rel,pr,pr.dateofbirth>person.dateofbirth)]=[pr]
            else:
                pr= indirect_relation.relation_tree.person
                if pr not in self.related_list:
                    self.related_list.append(pr)
                    relation_dict[self.get_basic_relation(rev_rel,pr,pr.dateofbirth>person.dateofbirth)].append(pr)
        return relation_dict
    
    def get_direct_relations(self,person):
        relation_dict={}
        direct_relation_list=RelationTree.objects.filter(person=person)
        for direct_relation in direct_relation_list:
            related_people=RelationTreePerson.objects.filter(relation_tree=direct_relation)
            rel=direct_relation.relation
            for rel_pr in related_people:
                pr=rel_pr.person
                if pr not in self.related_list:
                    self.related_list.append(pr)
                    if rel not in relation_dict:
                        relation_dict[self.get_basic_relation(rel,pr,pr.dateofbirth<person.dateofbirth)]=[pr]
                    else:
                        relation_dict[self.get_basic_relation(rel,pr,pr.dateofbirth<person.dateofbirth)].append(pr)
        return relation_dict

    def combine_relation_data(self,old_data,new_data):
        for key,value in new_data.items():
            for key2,value2 in value.items():
                if key not in old_data:
                    old_data[key]=value
                else:
                    if key2 not in old_data[key]:
                        old_data[key][key2]=value2
                    else:
                        for item in value2:
                            if item not in old_data[key][key2]:
                                old_data[key][key2].append(item)
        return old_data
    
    def get_primal_relations(self,person):
        rel1=self.get_direct_relations(person)
        rel2=self.get_indirect_relations(person)
        return {**rel1,**rel2}
    
    
    def get_relation_data(self,person):
        result_dict={}
        p_rel=self.get_primal_relations(person)
        return p_rel
    
class RepetitiveReport:
    def __init__(self,request):
        self.request=request

    def get_object_list(self, m_name):
        mq = ModelQueryset(self.request)
        return mq.get_queryset(m_name)
        
    def get_repetitive(self,r_code):
        if type(r_code)==str:
            repetitive_list=Repetitive.objects.filter(code=r_code)
            if len(repetitive_list)==1:
                return repetitive_list[0]
        return None
        
    def gather_info(self,repetitive):
        if type(repetitive)==str:
            repetitive=self.get_repetitive(repetitive)
        if type(repetitive)==Repetitive:
            repetitive_record_list=RepetitiveRecord.objects.filter(repetitive=repetitive)
            item_list=[]
            for item in repetitive_record_list:
                if item.transaction!=None:
                    item_list.append((item.id,str(item),item.transaction.date,item.transaction.amount))
            item_list=sorted(item_list,key=lambda tup:tup[2])[-12:]
            id_list=[]
            name_list=[]
            data_list=[]
            for item in item_list:
                id_list.append(item[0])
                name_list.append(str(item[2]))
                data_list.append(float(item[3]))
            return id_list,name_list,data_list
        return [],[],[]


class TransactionCategoryReport:
    def __init__(self, request):
        self.request = request
    
    def get_object_list(self, m_name):
        mq = ModelQueryset(self.request)
        return mq.get_queryset(m_name)
    
    def get_category(self, c_id):
        if type(c_id) == str:
            category_list = TransactionCategoryLM.objects.filter(id=c_id)
            if len(category_list) == 1:
                return category_list[0]
        return None
    
    def get_keys(self):
        today=dt.datetime.today()
        key_list=[]
        for i in range(12):
            month=today.month
            year=today.year
            new_month=month-i
            if new_month<=0:
                new_month+=12
                year-=1
            key="%d-%d" % (year,new_month)
            key_list.append(key)
        return key_list
    
    def gather_info(self, category):
        if type(category) == str:
            category = self.get_category(category)
        if type(category) == TransactionCategoryLM:
            transaction_list = Transaction.objects.filter(category=category)
            item_dict = {}
            for key in self.get_keys():
                item_dict[key]=0.0
            for transaction in transaction_list:
                ym = "%d-%d" % (transaction.date.year,transaction.date.month)
                if ym in item_dict:
                    item_dict[ym] += float(transaction.amount)
            name_list=[]
            data_list=[]
            item_list=sorted(list(item_dict.items())[:12],key=lambda tup:tup[0])
            for key,value in item_list:
                name_list.append(key)
                data_list.append(value)
            return name_list,data_list
        return [],[]