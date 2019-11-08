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
        sprint_id = -1
        try:
            sprint_id = self.kwargs['sprint_id']
        except:
            pass
        data = {}
        if sprint_id == -1:
            data = SprintBacklogList.get_data(self.kwargs['project_id'])
        else:
            data = SprintBacklogList.get_data(self.kwargs['project_id'], sprint_id)
        context["in_progress_pbi"] = data["in_progress_pbi"]
        context["current_sprint_pbi"] = data["current_sprint_pbi"]
        context["number_of_stories"] = data["number_of_stories"]
        context["total_story_points"] = data["total_story_points"]
        context["current_sprint_number"] = data["current_sprint_number"]
        context["project_id"] = self.kwargs['project_id']
        return context
    
    @staticmethod
    def get_data(project_id, sprint_id = -1):
        current_sprint_id = -1
        if sprint_id == -1:
            current_sprint_id = SprintBacklogList.get_current_sprint_id(project_id)
        else:
            current_sprint_id = sprint_id

        notCompletedPBI = []
        current_sprint_pbi = []
        data = {}
        number_of_stories = 0
        total_story_points = 0
        if current_sprint_id:
            for pbi in PBI.objects.order_by('priority'):
                if pbi.sprint_number == None:
                    if (pbi.getStatus() != "Completed"):
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
        
        data["current_sprint_number"] = Sprint.objects.get(pk=current_sprint_id).sprint_number
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
        allTask = Task.objects.exclude(status = "Done")
        if current_sprint_id:
            for pbi in PBI.objects.filter(pk__in = pbi_id):
                for task in allTask.filter(pbi_id = pbi):
                    task.delete()
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
    template_name = "sprintList.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.sprintCompleteHandler(self.kwargs['project_id'])
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

    @staticmethod
    def sprintCompleteHandler(project_ID):
        current_sprint_id = SprintBacklogList.get_current_sprint_id(project_ID)
        all_sprint = Sprint.objects.filter(project_id = project_ID)
        in_progress_sprint = all_sprint.filter(status="Progress")
        if in_progress_sprint:
            in_progress_sprint = in_progress_sprint[0]
        else:
            in_progress_sprint = None

        if (in_progress_sprint == None or in_progress_sprint.pk == current_sprint_id):
            print ("nothing happened")
            return
        
        in_progress_sprint.status = "Done"
        in_progress_sprint.save()

        for pbi in PBI.objects.filter(status = "Not"):
            pbi.status = "New"
            pbi.save()

        insprint_pbi = PBI.objects.filter(sprint_number = in_progress_sprint)
        for pbi in insprint_pbi:
            if pbi.getStatus() == "Completed":
                pbi.status = "Done"
                pbi.priority = None
                pbi.story_point = 0
                pbi.save()
            else:
                all_task_inPbi = Task.objects.filter(pbi_id = pbi)
                for task in all_task_inPbi:
                    if task.status != "Done":
                        task.delete()
                        pass
                    else:
                        task.effort_hour = 0
                        task.save()
                pbi.status = "Not"
                pbi.sprint_number = None
                pbi.priority = None
                pbi.save()

    @staticmethod
    def createSprint(request):
        current_project = Project.objects.get(pk = request.POST["project_id"])
        _start_date = datetime.datetime.today().date()
        _end_date = datetime.datetime.strptime(request.POST["sprint_end_date"], '%Y-%m-%d').date()
        all_sprint = Sprint.objects.filter(project_id=current_project)
        sprint_num = all_sprint.count() + 1
        max_hour = int(request.POST["max_effort_hour"])
        new_sprint = Sprint(sprint_number = sprint_num, project_id = current_project, start_date = _start_date, end_date = _end_date, max_effort_hour = max_hour)
        new_sprint.save()
        return HttpResponseRedirect(reverse('application:sprint_list', args=(request.POST["project_id"],)))

class InSprintView(TemplateView):
    template_name = "Sprint1v2.html"
    _pbi_id = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _pbi_id = self.kwargs['pbi_id']
        _sprint_num = self.kwargs['sprint_num']
        _project_id = self.kwargs['project_id']
        project = Project.objects.get(pk = _project_id)
        sprint = Sprint.objects.get(sprint_number = _sprint_num, project_id = project)
        pbi = PBI.objects.get(pk = _pbi_id, sprint_number = sprint, project_id = project)

        context['current_pbi'] = []
        context['current_pbi'].append(PBI.objects.get(pk = _pbi_id, project_id = project, sprint_number = sprint))
        context['pbi_tasks'] = Task.objects.filter(pbi_id = pbi)
        context['new_tasks'] = Task.objects.filter(pbi_id = pbi, status= 'New')
        context['progress_tasks'] = Task.objects.filter(pbi_id = pbi, status= 'Progress')
        context['finished_tasks'] = Task.objects.filter(pbi_id = pbi, status= 'Done')
        context['progress_bar'] = 0 if len(context['pbi_tasks']) == 0 else int((len(context['progress_tasks'])/ len(context['pbi_tasks']) )*100)
        context['progress_bar_finished'] = 0 if len(context['pbi_tasks']) == 0 else int((len(context['finished_tasks'])/ len(context['pbi_tasks']) )*100)
        project_id = list(PBI.objects.filter(pk = _pbi_id).values_list('project_id', flat = True))[0]
        context['project_id'] = project_id
  

        return context

def createTask(request):
    pbi_id = request.POST['pbi_id']
    pbi = PBI.objects.get(pk= pbi_id)
    sprint_num = request.POST['sprint_num']
    project_id = request.POST['project_id']
    task_effort_point = request.POST['effortpts']

    sprint = Sprint.objects.get(project_id = project_id, sprint_number = sprint_num)
    current_sprint_pbi = []
    current_sprint_pbi=(list(PBI.objects.filter(sprint_number = sprint).values_list('pbi_id', flat = True)))
    task_total_hour = Task.objects.filter(pbi_id__in = current_sprint_pbi).aggregate(Sum('effort_hour'))

    if (task_total_hour["effort_hour__sum"] == None):
        task_total_hour["effort_hour__sum"] = 0

    if (( int(sprint.max_effort_hour) - int(task_total_hour['effort_hour__sum'])  - int(task_effort_point) )>= 0):
        task_description = request.POST['description']
        Task.objects.create_task(pbi, task_description, task_effort_point)

    return HttpResponseRedirect(reverse('application:insprint', args=(project_id, sprint_num,pbi_id,)))

def editTask(request):
    _task_id = request.POST['task_id']
    task = Task.objects.get(pk=_task_id)
    task.task_description = request.POST['task_description']
    task.effort_hour = request.POST['effort_hour'] 
    task.save()

    pbi_id = request.POST['pbi_id']
    sprint_num = request.POST['sprint_num']
    project_id = request.POST['project_id']
    return HttpResponseRedirect(reverse('application:insprint', args=(project_id, sprint_num,pbi_id, )))

def editTask2(request):
    _task_id = request.POST['task_id']
    task = Task.objects.get(pk=_task_id)
    task.task_description = request.POST['task_description']
    task.effort_hour = request.POST['effort_hour'] 
    task.save()

    sprint_num = request.POST['sprint_num']
    project_id = request.POST['project_id']
    return HttpResponseRedirect(reverse('application:sprint_page', args=(project_id, sprint_num )))

def deleteTask(request):
    _task_id = request.POST['task_id']
    pbi_id = request.POST['pbi_id']
    task = Task.objects.get(pk = _task_id)
    task.delete()
    project_id = request.POST['project_id']
    sprint_num = request.POST['sprint_num']
    return HttpResponseRedirect(reverse('application:insprint', args=(project_id, sprint_num, pbi_id, )))

def deleteTask2(request):
    _task_id = request.POST['task_id']
 
    task = Task.objects.get(pk = _task_id)
    task.delete()
    sprint_num = request.POST['sprint_num']
    project_id = request.POST['project_id_']
    return HttpResponseRedirect(reverse('application:sprint_page', args=(project_id, sprint_num, )))


def pickOrDropTask(request):
    _task_id = request.POST['task_id']
    pbi_id = request.POST['pbi_id']
    task_pickup_status = WorksOnTask.objects.filter(task_id = _task_id).count()
    task = Task.objects.get(pk = _task_id)
    
    if (task_pickup_status == 0):
        # task = Task.objects.get(pk = _task_id)
        # _user_id = request.POST['user_id']
        task.status = 'Progress'
        task.save()
        user = User.objects.get(pk = 4)
        WorksOnTask.objects.create_WorksOnTask(user, task)
    else:
        task.status = 'New'
        task.save()
        worksOn = WorksOnTask.objects.get(task_id = task)
        worksOn.delete()

    sprint_num = request.POST['sprint_num']
    project_id = request.POST['project_id']
    return HttpResponseRedirect(reverse('application:insprint', args=(project_id, sprint_num, pbi_id, )))



def markTaskAsDone(request):
    _task_id = request.POST['task_id']
    pbi_id = request.POST['pbi_id']
    task = Task.objects.get(pk = _task_id)
    # task_pickup_status = WorksOnTask.objects.filter(task_id = _task_id).count()
    if (task.status != 'Done'):
        task.status = 'Done'
    else:
        task.status = 'Progress'
    
    task.save()
    sprint_num = request.POST['sprint_num']
    project_id = request.POST['project_id']
    return HttpResponseRedirect(reverse('application:insprint', args=(project_id, sprint_num, pbi_id, )))



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
       
        if (context['in_progress_tasks_EH']['effort_hour__sum'] == None):
            context['in_progress_tasks_EH']['effort_hour__sum'] = 0

        if (context['completed_tasks_EH']['effort_hour__sum'] == None):
            context['completed_tasks_EH']['effort_hour__sum'] = 0

        context['max_sprint_hours'] = sprint
        remaining_hours_ = context['max_sprint_hours'].max_effort_hour - context['task_total_EH']['effort_hour__sum']
        context['remaining_hours'] = remaining_hours_
        context['remaining_hours_percent'] = int(((remaining_hours_)/(context['max_sprint_hours'].max_effort_hour))*100)

        context['existing_hour_percent'] = int(((context['task_total_EH']['effort_hour__sum'])/context['max_sprint_hours'].max_effort_hour)*100)
        
        

        return context

