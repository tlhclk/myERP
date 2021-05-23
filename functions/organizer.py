# -*- coding: utf-8 -*-
from functions.auth_func import ModelFunc
from django.shortcuts import redirect


def set_account_amount(transaction,account_amount):
    type_out=1
    type_in=2
    transaction.account_amount=account_amount
    if transaction.type_id==type_out:
        account_amount = account_amount + transaction.amount
    else:
        account_amount = account_amount - transaction.amount
    transaction.save()
    return account_amount
    
def revise_transaction(transaction_list,account_amount):
    for transaction in transaction_list:
        account_amount=set_account_amount(transaction,account_amount)
    return account_amount

def build_transaction_history(account_list):
    transaction_model=ModelFunc().get_model("Transaction")
    cur_account={}
    for account in account_list:
        if account not in cur_account:
            cur_account[account]=account.amount
        transaction_list=transaction_model.objects.filter(account=account).order_by("-date","-time","id")
        account_amount=revise_transaction(transaction_list,cur_account[account])
        cur_account[account]=cur_account[account]+account_amount
    if len(cur_account)==0:
        return redirect("global_list",m_name="Transaction",kwargs={"account_id":cur_account.keys()[0].id})
    else:
        return redirect("global_list",m_name="Transaction")
    
    
class CodeGenerator(ModelFunc):
    def __init__(self,item):
        super(CodeGenerator, self).__init__()
        self.item=item
        self.rep_model = self.get_model("Repetitive")
        self.person_model = self.get_model("Person")
        
    def transform_string(self,text):
        return text.lower().replace("ğ","g").replace("ü","u").replace("ş","s").replace("ı","i").replace("ö","o").replace("ç","c")

    def generate_person_code(self,pc=1):
        base_code = "%s-%d"
        fullname=self.item.full_name
        fn_list=fullname.split()
        new_code = ""
        for word in fn_list:
            new_code += word[0]
        new_code = self.transform_string(base_code % (new_code,pc))
        people_list = self.person_model.objects.filter(code=new_code)
        if len(people_list)!=0:
            return self.generate_person_code(pc+1)
        else:
            return new_code
        
    def generate_repetitive_code(self,rc=1):
        base_code = "%s_%s-%d"
        person_code = self.item.person.code
        type_code = self.item.type.code
        new_code = self.transform_string(base_code % (person_code,type_code,int(rc)))
        rep_list=self.rep_model.objects.filter(code=new_code)
        if len(rep_list)!=0:
            return self.generate_repetitive_code(rc+1)
        else:
            return new_code
    
    def generate_repetitive_record_code(self):
        base_code = "%s_%d-%d"
        base_code2 = "%s_%s"
        if self.item.transaction:
            year,week,weekday = self.item.transaction.date.isocalendar()
            if self.item.repetitive.period_rate.id == 1:#yıllık
                new_code = base_code2 % (self.item.repetitive.code,str(year))
            elif self.item.repetitive.period_rate.id == 2:#aylık
                new_code = base_code % (self.item.repetitive.code,year,self.item.transaction.date.month)
            elif self.item.repetitive.period_rate.id == 3:#haftalık
                new_code = base_code % (self.item.repetitive.code,year,week)
            elif self.item.repetitive.period_rate.id == 4:#günlük
                new_code = base_code % (self.item.repetitive.code,year,week*7+weekday)
            elif self.item.repetitive.period_rate.id == 6:#km
                new_code = base_code2 % (self.item.repetitive.code,self.item.amount)
            else:
                temp_list = self.item.repetitive.repetitiverecord_set.filter(last_date__year=year).order_by("last_date")
                new_code = base_code % (self.item.repetitive.code,year,len(temp_list))
        else:
            new_code=""
        return new_code
        

        

