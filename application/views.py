from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def product_backlog_view (request,*args,**kwargs):
    return render(request,"pb.html",{})

def sprint_backlog_view (request,*args,**kwargs):
    return render(request,"SB.html",{})

def sprint_1_view (request,*args,**kwargs):
    return render(request,"Sprint1.html",{})