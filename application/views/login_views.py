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
    user_password = []
    user_authenticated = 0
    
    

    try:
        user_username = User.objects.get(username = username)
        user_password = list(User.objects.filter(password = password))
    except:
        pass

    if user_username in user_password:
        user_authenticated = 1
    

    if(user_authenticated):
        response =  HttpResponseRedirect(reverse('application:all_project_list'))
        response.set_cookie('user_id', user_username.user_id )
        
        return response

    else:
        messages.error(request, 'Incorrect username/password!')
        return HttpResponseRedirect(reverse('application:login_page'))


        
    
