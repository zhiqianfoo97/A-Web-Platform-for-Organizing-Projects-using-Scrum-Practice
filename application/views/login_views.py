from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from application.models import *
from django.urls import reverse

from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.generic.edit import DeleteView
import datetime
import json

class loginPage(TemplateView):
    template_name = "loginPage.html"

def login_auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user_username = "1"
    user_password = "0"
    try:
        user_username = User.objects.get(username = username)
        user_password = User.objects.get(password = password)
    except:
        pass

    isInProject = []
    

    if(user_username == user_password):
        try:
            isInProject = list(WorksOnProject.objects.filter(user_id = user_username).values_list('project_id__project_id', flat=True))
        except:
            isInProject = []
        
        if(isInProject): # if involved in project
            return HttpResponseRedirect(reverse('application:product_backlog', args=(isInProject[0],)))
        else:
            return HttpResponseRedirect(reverse('application:all_project_list'))

    else:
        return HttpResponseRedirect(reverse('application:login_page'))


        
    
