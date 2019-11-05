from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from application.models import PBI, Project, Task
from django.urls import reverse, reverse_lazy, resolve
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.generic.edit import DeleteView




class InSprintView(TemplateView):
    template_name = "Sprint1v2.html"
    _pbi_id = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _pbi_id = self.kwargs['pbi_id']
        context['current_pbi'] = []
        context['current_pbi'].append(PBI.objects.get(pk = _pbi_id))
        context['pbi_tasks'] = Task.objects.filter(pbi_id = _pbi_id)
    

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


