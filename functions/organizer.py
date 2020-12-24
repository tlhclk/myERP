# -*- coding: utf-8 -*-
import functions.auth_func as af
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
    tra_obj,transaction_model=af.get_model("Transaction")
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
        
    