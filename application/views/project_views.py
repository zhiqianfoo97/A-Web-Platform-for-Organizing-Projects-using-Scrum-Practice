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
        user = User.objects.get(pk= user_id)
        inProject = []
        inProject = list(WorksOnProject.objects.filter(user_id = user))
        
        data = ProjectList.get_data()
        context["project_list"] = data["project_list"]
        context['notification'] = Notification.objects.filter(user_id = user_id)
        context['in_project'] = inProject


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
        user_id = request.COOKIES.get('user_id')
        user = User.objects.get(pk = user_id)
        user.role = 'PO'
        user.save()
        WorksOnProject.objects.create_WorksOnProject(user, newProject)

        return HttpResponseRedirect(reverse('application:all_project_list'))

    

def rejectInvitation(request):
    notification_1 = Notification.objects.get(pk = request.POST['_id'])
    notification_1.delete()
    return HttpResponseRedirect(reverse('application:all_project_list'))

def acceptInvitation(request):
    user_id = request.COOKIES.get('user_id')
    user = User.objects.get(pk = user_id)
    
    notification_1 = Notification.objects.get(pk = request.POST['_id'])
    project = notification_1.project_id
    notification_1.delete()
    WorksOnProject.objects.create_WorksOnProject(user, project)
    
    if(user.role != 'SM'):
        notification_2 = Notification.objects.filter(user_id = user)
        for noti_2 in notification_2:
            noti_2.delete()

    return HttpResponseRedirect(reverse('application:all_project_list'))