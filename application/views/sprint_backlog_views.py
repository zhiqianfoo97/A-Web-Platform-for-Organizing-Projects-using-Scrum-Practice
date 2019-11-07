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

class sprintBackLogList(TemplateView):
    template_name = "SB.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = sprintBackLogList.get_data()
        context["in_progress_pbi"] = data["in_progress_pbi"]
        context["current_sprint_pbi"] = data["current_sprint_pbi"]
        return context
    
    @staticmethod
    def get_data():
        current_sprint_id = sprintBackLogList.get_current_sprint_id()
        notCompletedPBI = []
        current_sprint_pbi = []
        data = {}
        for pbi in PBI.objects.order_by('priority'):
            if (pbi.getStatus() == "Not yet started"):
                if pbi.sprint_number == None:
                    notCompletedPBI.append(pbi.simple_serialise())
                elif pbi.sprint_number.pk == current_sprint_id:
                    current_sprint_pbi.append(pbi.simple_serialise())
                else:
                    notCompletedPBI.append(pbi.simple_serialise())
        data["in_progress_pbi"] = notCompletedPBI
        data["current_sprint_pbi"] = current_sprint_pbi
        return data
    
    @staticmethod
    def get_current_sprint_id():
        today = datetime.datetime.today()
        sprints = Sprint.objects.filter(start_date__lte = today, end_date__gte = today)
        if sprints:
            return (sprints[0].pk)
        else:
            return None
    
    @staticmethod
    def add_to_sprint(request): 
        pbi_id = eval(request.POST["pbi"])
        current_sprint = Sprint.objects.get(pk = sprintBackLogList.get_current_sprint_id())
        for pbi in PBI.objects.filter(pk__in = pbi_id):
            pbi.sprint_number = current_sprint
            pbi.save()
        data = sprintBackLogList.get_data()
        context = {}
        context["in_progress_pbi"] = data["in_progress_pbi"]
        context["current_sprint_pbi"] = data["current_sprint_pbi"]
        return JsonResponse(context)
    
    @staticmethod
    def remove_from_sprint(request): 
        pbi_id = eval(request.POST["pbi"])
        for pbi in PBI.objects.filter(pk__in = pbi_id):
            pbi.sprint_number = None
            pbi.save()
        data = sprintBackLogList.get_data()
        context = {}
        context["in_progress_pbi"] = data["in_progress_pbi"]
        context["current_sprint_pbi"] = data["current_sprint_pbi"]
        return JsonResponse(context)


class InSprintView(TemplateView):
    template_name = "Sprint1v2.html"
    _pbi_id = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _pbi_id = self.kwargs['pbi_id']
        context['current_pbi'] = []
        context['current_pbi'].append(PBI.objects.get(pk = _pbi_id))
        context['pbi_tasks'] = Task.objects.filter(pbi_id = _pbi_id)
        context['new_tasks'] = Task.objects.filter(pbi_id = _pbi_id, status= 'New')
        context['progress_tasks'] = Task.objects.filter(pbi_id = _pbi_id, status= 'Progress')
        context['finished_tasks'] = Task.objects.filter(pbi_id = _pbi_id, status= 'Done')
        context['progress_bar'] = int((len(context['finished_tasks'])/ len(context['pbi_tasks']) )*100)

        return context

def createTask(request):
    pbi_id = request.POST['pbi_id_']
    pbi = PBI.objects.get(pk= pbi_id)
    
    task_description = request.POST['description']
    task_effort_point = request.POST['effortpts']
    Task.objects.create_task(pbi, task_description, task_effort_point)

    return HttpResponseRedirect(reverse('application:insprint', args=(pbi_id,)))

def editTask(request):
    _task_id = request.POST['task_id']
    task = Task.objects.get(pk=_task_id)
    task.task_description = request.POST['description']
    task.effort_hour = request.POST['effortpts']
    pbi_id = request.POST['pbi_id']

    task.save()
    return HttpResponseRedirect(reverse('application:insprint', args=(pbi_id, )))

def deleteTask(request):
    _task_id = request.POST['task_id']
    pbi_id = request.POST['pbi_id']
    task = Task.objects.get(pk = _task_id)
    task.delete()
    return HttpResponseRedirect(reverse('application:insprint', args=(pbi_id, )))


def pickOrDropTask(request):
    _task_id = request.POST['task_id']
    pbi_id = request.POST['pbi_id']
    task_pickup_status = WorksOnTask.objects.filter(task_id = _task_id).count()
    if (task_pickup_status != 0):
        task = Task.objects.get(pk = _task_id)
        _user_id = request.POST['user_id']
        user = User.objects.get(pk = _user_id)
        WorksOnTask.objects.create_WorksOnTask(user, task)
    else:
        worksOn = WorksOnTask.objects.get(task_id = _task_id)
        worksOn.delete()

    return HttpResponseRedirect(reverse('application:insprint', args=(pbi_id, )))



def markTaskAsDone(request):
    _task_id = request.POST['task_id']
    pbi_id = request.POST['pbi_id']
    task = Task.objects.get(pk = _task_id)
    task_pickup_status = WorksOnTask.objects.filter(task_id = _task_id).count()
    if (task.status != 'Done'):
        task.status = 'Done'
    else:
        if(task_pickup_status != 0):
            task.status = 'Progress'
        else:
            task.status = 'New'

    return HttpResponseRedirect(reverse('application:insprint', args=(pbi_id, )))

