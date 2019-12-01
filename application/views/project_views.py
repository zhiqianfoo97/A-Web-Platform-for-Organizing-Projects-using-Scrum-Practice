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

class ProjectList(TemplateView):
    template_name = "dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.COOKIES.get('user_id')

        data = ProjectList.get_data()
        context["project_list"] = data["project_list"]
        context['notification'] = Notification.objects.filter(user_id = user_id)
        

        return context
  

    @staticmethod
    def get_data():
        listOfProject = Project.objects.all()
        data = {}
        projects = []
        for project in listOfProject:
            projects.append(project.simple_serialise())
        data["project_list"] = projects
        return data
    
    @staticmethod
    def createProject(request):
        newProject = Project(project_name = request.POST["project_name"], project_description = request.POST["project_desc"])
        newProject.save()
        return HttpResponseRedirect(reverse('application:all_project_list'))

    

    