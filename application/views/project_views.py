from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from application.models import *
from django.urls import reverse
from django.core.mail import send_mail
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

        return HttpResponseRedirect(reverse('application:invite_team', args=(newProject.project_id,)))

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

class inviteTeamPage(TemplateView):
    template_name = "invite.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['project_id']
        project = Project.objects.get(pk = project_id)
        current_working_dev = []
        current_project_SM = []
        current_working_dev = (list(WorksOnProject.objects.filter(user_id__role = 'D').values_list('user_id__user_id', flat = True)))
        current_project_SM = (list(WorksOnProject.objects.filter(user_id__role = 'SM').filter(project_id__project_id = project_id).values_list('user_id__user_id', flat = True)))
        current_invited_dev = []
        current_invited_SM = []
        for ele in list(Notification.objects.filter(project_id = project)):
            if ele.user_id.role == "SM":
                current_invited_SM.append(ele.user_id.user_id)
            else:
                current_invited_dev.append(ele.user_id.user_id)

        if (len(current_project_SM) == 0):
            context['scrum_master_exist'] = ""
        else:
            context['scrum_master_exist'] = User.objects.get(user_id = current_project_SM[0])

        if (len(current_invited_SM) == 0):
            context['scrum_master_invited'] = ""
        else:
            context['scrum_master_invited'] = User.objects.get(user_id = current_invited_SM[0])

        #User.objects.exclude(user_id__in = current_project_SM).filter(role = 'SM')
        context['scrum_master'] = User.objects.filter(role = 'SM').exclude(user_id__in = current_project_SM)
        context['dev'] = User.objects.exclude(user_id__in = current_working_dev).exclude(user_id__in = current_invited_dev).filter(role = 'D')
        context['dev_invited'] = User.objects.filter(user_id__in = current_invited_dev)
        context['dev_exist'] = User.objects.filter(user_id__in = current_working_dev)
        context['project_id'] = project_id

        user_id_ = self.request.COOKIES.get('user_id')
        context['notification'] = Notification.objects.filter(user_id = user_id_)

        return context

def addToTeam(request):
    project_id = 0
    user_ids = eval(request.POST['user_id_s'])
    project_id = request.POST['project_id']
    project = Project.objects.get(pk = project_id)
    project_name = project.project_name
    current_project_PO = []
    current_project_PO = (list(WorksOnProject.objects.filter(user_id__role = 'PO').filter(project_id__project_id = project_id).values_list('user_id__user_id', flat = True)))
    current_project_PO_userObject = User.objects.get(user_id = current_project_PO[0])
    user_emails = []
    standard_messages = "You are invited to join the following project: " + project_name + " by " + current_project_PO_userObject.name + '.'
    
    present_noti_uid = [ele.user_id.user_id for ele in list(Notification.objects.filter(project_id = project))]
    print(present_noti_uid)

    for user_id in user_ids:
        user = User.objects.get(user_id = int(user_id))
        if (not (user.user_id in present_noti_uid)):
            Notification.objects.create_Notification(user, project, standard_messages)
            user_emails.append(user.email)

    send_mail(
        'Project invitation',
        'You are invited to join the following project: ' + project_name + ' by ' + current_project_PO_userObject.name + '.',
        current_project_PO_userObject.email,
        user_emails,
        fail_silently= True
    )
    context = {}
    context['success'] = 1
    return JsonResponse(context)