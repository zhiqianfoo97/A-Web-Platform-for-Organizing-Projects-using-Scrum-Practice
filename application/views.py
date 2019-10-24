from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def product_backlog_view (request,*args,**kwargs):
    return render(request,"PB.html",{})

def sprint_backlog_view (request,*args,**kwargs):
    return render(request,"SB.html",{})

def sprint_1_view (request,*args,**kwargs):
    return render(request,"Sprint1.html",{})

def sprint_1_view_v2 (request,*args,**kwargs):
    return render(request,"Sprint1v2.html",{}) 