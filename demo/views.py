# -*- coding: utf-8 -*-
from django.shortcuts import render
from functions.demo import SerialListener
from django.http import JsonResponse


def listen_comport(request):
    template_name="demo/comport_listener.html"
    comport_list=SerialListener().get_comport_list()
    context_data={}
    context_data["comport_list"]=comport_list
    context_data["title"]="Com Port Dinleme"
    return render(request, template_name, context=context_data)
    
def port_listener(request):
    if "p_name" not in request.GET:
        data="None"
    else:
        p_name=request.GET["p_name"]
        sp = SerialListener(p_name)
        sp.set_timeout(sp.serial_port,3)
        data = sp.get_data(sp.serial_port)
        sp.close_port(sp.serial_port)
    return JsonResponse({"data":data})
    
def demo(request):
    sp=SerialListener()
    sp.demo()
    return render(request, "demo/demo.html")