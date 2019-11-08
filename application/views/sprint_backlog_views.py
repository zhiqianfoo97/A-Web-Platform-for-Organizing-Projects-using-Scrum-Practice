from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from application.models import *
from django.urls import reverse
from django.db.models import Avg, Count, Min, Sum

from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.generic.edit import DeleteView
from datetime import date
import datetime
import json

class SprintBacklogList(TemplateView):
    template_name = "SB.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = SprintBacklogList.get_data(self.kwargs['project_id'])
        context["in_progress_pbi"] = data["in_progress_pbi"]
        context["current_sprint_pbi"] = data["current_sprint_pbi"]
        context["number_of_stories"] = data["number_of_stories"]
        context["total_story_points"] = data["total_story_points"]
        context["project_id"] = self.kwargs['project_id']
        return context
    
    @staticmethod
    def get_data(project_id):
        current_sprint_id = SprintBacklogList.get_current_sprint_id(project_id)
        notCompletedPBI = []
        current_sprint_pbi = []
        data = {}
        number_of_stories = 0
        total_story_points = 0
        if current_sprint_id:
            for pbi in PBI.objects.order_by('priority'):
                if (pbi.getStatus() == "Not yet started"):
                    if pbi.sprint_number == None:
                        notCompletedPBI.append(pbi.simple_serialise())
                    elif pbi.sprint_number.pk == current_sprint_id:
                        current_sprint_pbi.append(pbi.simple_serialise())
                        number_of_stories += 1
                        total_story_points += pbi.story_point
                    # else:
                    #     notCompletedPBI.append(pbi.simple_serialise())
        data["in_progress_pbi"] = notCompletedPBI
        data["current_sprint_pbi"] = current_sprint_pbi
        data["number_of_stories"] = number_of_stories
        data["total_story_points"] = total_story_points
        return data
    
    @staticmethod
    def get_current_sprint_id(project_ID):
        today = datetime.datetime.today()
        listOfSprints = Sprint.objects.filter(project_id = project_ID)
        sprints = listOfSprints.filter(start_date__lte = today, end_date__gte = today)
        if sprints:
            return (sprints[0].pk)
        else:
            return None
    
    @staticmethod
    def add_to_sprint(request): 
        pbi_id = eval(request.POST["pbi"])
        current_sprint_id = SprintBacklogList.get_current_sprint_id(request.POST["project_id"])
        if current_sprint_id:
            current_sprint = Sprint.objects.get(pk = current_sprint_id)
            for pbi in PBI.objects.filter(pk__in = pbi_id):
                pbi.sprint_number = current_sprint
                pbi.save()
        data = SprintBacklogList.get_data(request.POST["project_id"])
        context = {}
        context["in_progress_pbi"] = data["in_progress_pbi"]
        context["current_sprint_pbi"] = data["current_sprint_pbi"]
        context["number_of_stories"] = data["number_of_stories"]
        context["total_story_points"] = data["total_story_points"]
        context["project_id"] = request.POST["project_id"]
        return JsonResponse(context)
    
    @staticmethod
    def remove_from_sprint(request): 
        pbi_id = eval(request.POST["pbi"])
        current_sprint_id = SprintBacklogList.get_current_sprint_id(request.POST["project_id"])
        if current_sprint_id:
            for pbi in PBI.objects.filter(pk__in = pbi_id):
                pbi.sprint_number = None
                pbi.save()
        data = SprintBacklogList.get_data(request.POST["project_id"])
        context = {}
        context["in_progress_pbi"] = data["in_progress_pbi"]
        context["current_sprint_pbi"] = data["current_sprint_pbi"]
        context["number_of_stories"] = data["number_of_stories"]
        context["total_story_points"] = data["total_story_points"]
        context["project_id"] = request.POST["project_id"]
        return JsonResponse(context)

class SprintList(TemplateView):
    template_name = "backend_test/sprint_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = SprintList.get_data(self.kwargs['project_id'])
        context["current_sprint"] = data["current_sprint"]
        context["sprint_list"] = data["sprint_list"]
        context["project_id"] = self.kwargs['project_id']
        return context
    
    @staticmethod
    def get_data(project_ID):
        current_sprint_id = SprintBacklogList.get_current_sprint_id(project_ID)
        current_sprint = None
        sprint_list = []
        data = {}
        for sprint in Sprint.objects.filter(project_id = project_ID):
            if current_sprint_id:
                if sprint.pk == current_sprint_id:
                    current_sprint = sprint.simple_serialise()
                    continue
            sprint_list.append(sprint.simple_serialise())
        data["current_sprint"] = current_sprint
        data["sprint_list"] = sprint_list
        return data

def sprintCompleteHandler():
    pass

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
        context['progress_bar'] = 0 if len(context['pbi_tasks']) == 0 else int((len(context['progress_tasks'])/ len(context['pbi_tasks']) )*100)
        context['progress_bar_finished'] = 0 if len(context['pbi_tasks']) == 0 else int((len(context['finished_tasks'])/ len(context['pbi_tasks']) )*100)

        return context

def checkSprintStatus(request):
    return None


def createTask(request):
    pbi_id = request.POST['pbi_id_']
    pbi = PBI.objects.get(pk= pbi_id)
    project_id = request.POST['project_id_']
    task_description = request.POST['description']
    task_effort_point = request.POST['effortpts']
    Task.objects.create_task(pbi, task_description, task_effort_point)

    return HttpResponseRedirect(reverse('application:insprint', args=(project_id,pbi_id,)))

def editTask(request):
    _task_id = request.POST['task_id']
    task = Task.objects.get(pk=_task_id)
    task.task_description = request.POST['description']
    task.effort_hour = request.POST['effortpts']
    pbi_id = request.POST['pbi_id']
    project_id = request.POST['project_id_']

    task.save()
    return HttpResponseRedirect(reverse('application:insprint', args=(project_id,pbi_id, )))

def deleteTask(request):
    _task_id = request.POST['task_id']
    pbi_id = request.POST['pbi_id']
    task = Task.objects.get(pk = _task_id)
    task.delete()

    project_id = request.POST['project_id_']
    return HttpResponseRedirect(reverse('application:insprint', args=(project_id, pbi_id, )))


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
    project_id = request.POST['project_id_']
    return HttpResponseRedirect(reverse('application:insprint', args=(project_id, pbi_id, )))



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
    project_id = request.POST['project_id_']
    return HttpResponseRedirect(reverse('application:insprint', args=(project_id, pbi_id, )))



class SprintPageView(TemplateView):
    template_name = "Sprint1.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _project_id = self.kwargs['project_id']
        _sprint_num = self.kwargs['sprint_num']
        project = Project.objects.get(project_id = _project_id)
        sprint = Sprint.objects.get(project_id = project, sprint_number = _sprint_num)
        current_sprint_pbi = []
        current_sprint_pbi=(list(PBI.objects.filter(sprint_number = sprint).values_list('pbi_id', flat = True)))
       
        # current_sprint_tasks = []
        # # current_sprint_tasks.append(Task.objects.filter(pbi_id__in = current_sprint_pbi))
        # for _pbi_id in current_sprint_pbi:
        #     current_sprint_tasks.append(Task.objects.filter(pbi_id = _pbi_id))

        # context['current_sprint_tasks'] =  current_sprint_tasks
        context['task_total_EH'] = Task.objects.filter(pbi_id__in = current_sprint_pbi).aggregate(Sum('effort_hour'))

        context['new_tasks'] = Task.objects.filter(pbi_id__in = current_sprint_pbi).filter(status = 'New')
        context['in_progress_tasks'] = Task.objects.filter(pbi_id__in = current_sprint_pbi).filter(status = 'Progress')
        context['completed_tasks'] = Task.objects.filter(pbi_id__in = current_sprint_pbi).filter(status = 'Done')

        context['new_tasks_EH'] = Task.objects.filter(pbi_id__in = current_sprint_pbi).filter(status = 'New').aggregate(Sum('effort_hour'))
        context['in_progress_tasks_EH'] = Task.objects.filter(pbi_id__in = current_sprint_pbi).filter(status = 'Progress').aggregate(Sum('effort_hour'))
        context['completed_tasks_EH'] = Task.objects.filter(pbi_id__in = current_sprint_pbi).filter(status = 'Done').aggregate(Sum('effort_hour'))


        return context

# sprintbacklog bugs : if a pbi is in progress, will disappear from sprint backlog
# sprint number is hardcoded