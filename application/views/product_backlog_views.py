from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from application.models import *
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.generic.edit import DeleteView

# Create your views here.
def invite_view (request,*args,**kwargs):
    return render(request,"invite.html",{})

def nonProductOwner_dashboard_view (request,*args,**kwargs):
    return render(request,"dashboardNonProductOwner.html",{})

def nonDevteam_SB_view (request,*args,**kwargs):
    return render(request,"NonDevTeamSB.html",{})

def login_view (request,*args,**kwargs):
    return render(request,"index.html",{})

def sprint_backlog_view (request,*args,**kwargs):
    return render(request,"SB.html",{})

def sprint_page_view (request,*args,**kwargs):
    return render(request,"Sprint1.html",{})

def in_sprint_view (request,*args,**kwargs):
    return render(request,"Sprint1v2.html",{})

def sprint_list_view (request,*args,**kwargs):
    return render(request,"sprintList.html",{})

def pastSprint_view (request,*args,**kwargs):
    return render(request,"pastSprint.html",{})


class BackLogList(TemplateView):
    template_name = "pb.html"
    _project_id = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _project_id = self.kwargs['project_id']
        uniquePriority()
        notCompletedPBI = []
        for pbi_completed in PBI.objects.filter(project_id = _project_id).order_by('priority'):
            if (pbi_completed.getStatus() != "Completed"):
                notCompletedPBI.append(pbi_completed)
        
        user_id = self.request.COOKIES.get('user_id')
        user = User.objects.get(pk = user_id)

        # _project = Project.objects.get(pk = _project_id)

        context['user_role'] = user.role
        context['current_view_pbi'] = notCompletedPBI
        context['normal_pbi'] = PBI.objects.all()
        context['project_id'] = _project_id

        # BacklogList.authenticate_user(user, _project)
        
        return context

        

class BackLogListFullView(TemplateView):
    template_name = "pbAll.html"
    _project_id = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _project_id = self.kwargs['project_id']
        completedPBI = []
        for pbi_not_completed in PBI.objects.filter(project_id= _project_id).order_by('priority').exclude(story_point = 0):
            completedPBI.append(pbi_not_completed)

        for pbi_completed in PBI.objects.filter(project_id = _project_id, story_point = 0):
            completedPBI.append(pbi_completed)

        user_id = self.request.COOKIES.get('user_id')
        user = User.objects.get(pk = user_id)

        context['user_role'] = user.role
        context['pbi_priority_list'] = completedPBI
        context['project_id'] = _project_id
        return context


def addData(request):
    _priority_points = request.POST['prioritypts']
    _user_story = request.POST['userstory']
    _story_point = request.POST['storypts']
    _sprint = None
    
    _project_id = Project.objects.get(pk = request.POST["project_id"])
    
    PBI.objects.create_pbi(_user_story, _sprint, _project_id, _story_point, _priority_points)
    uniquePriority()
    return HttpResponseRedirect(reverse('application:product_backlog', args=(request.POST['project_id'],)))

def addDataAll(request):
    _priority_points = request.POST['prioritypts']
    _user_story = request.POST['userstory']
    _story_point = request.POST['storypts']
    _sprint = None
    
    _project_id = Project.objects.get(pk = request.POST["project_id"])
    
    PBI.objects.create_pbi(_user_story, _sprint, _project_id, _story_point, _priority_points)
    uniquePriority()
    return HttpResponseRedirect(reverse('application:product_backlog_all', args=(request.POST['project_id'],)))
    
def delData(request):
    _pbi_id = request.POST['pbi_id']
    pbi = PBI.objects.get(pk = _pbi_id)
    pbi.delete()
    uniquePriority()
    return HttpResponseRedirect(reverse('application:product_backlog', args=(request.POST['project_id'],)))

def delDataAll(request):
    _pbi_id = request.POST['pbi_id']
    pbi = PBI.objects.get(pk = _pbi_id)
    pbi.delete()
    uniquePriority()
    return HttpResponseRedirect(reverse('application:product_backlog_all', args=(request.POST['project_id'],)))


def editData(request):
    _pbi_id = request.POST['pbi_id']
    pbi = PBI.objects.get(pk = _pbi_id)
    pbi.user_story = request.POST['user_story']
    if (request.POST['sprint_num'] == ''):
        pbi.sprint_number = None
    else:
        pbi.sprint_number = Sprint.objects.get(sprint_number =request.POST['sprint_num'])
    pbi.priority = request.POST['priority_points']
    pbi.story_point = request.POST['story_points']
    pbi.save()
    uniquePriority()
    return HttpResponseRedirect(reverse('application:product_backlog', args=(request.POST['project_id'],)))


def editDataAll(request):
    _pbi_id = request.POST['pbi_id']
    pbi = PBI.objects.get(pk = _pbi_id)
    pbi.user_story = request.POST['user_story']
    try:
        if (request.POST['sprint_num'] == ''):
            pbi.sprint_number = None
        else:
            pbi.sprint_number = Sprint.objects.get(sprint_number =request.POST['sprint_num'])
        pbi.priority = request.POST['priority_points']
        pbi.story_point = request.POST['story_points']
    except Exception as e:
        pass
    
    pbi.save()
    uniquePriority()
    return HttpResponseRedirect(reverse('application:product_backlog_all', args=(request.POST['project_id'],)))

def increasePriority(request, pbi_id, project_id):
    
    pbi = PBI.objects.get(pk = pbi_id)

    pbi_prev = None

    for _pbi in PBI.objects.order_by('priority').exclude(story_point = 0):
        if(pbi ==  _pbi):
            break
        pbi_prev = _pbi

    temp_pbi = pbi.priority
    pbi.priority = pbi_prev.priority
    pbi.save()
    pbi_prev.priority = temp_pbi
    pbi_prev.save()
    uniquePriority()

    return JsonResponse({"message": "increment operation done"})

def decreasePriority(request, pbi_id, project_id):
    pbi = PBI.objects.get(pk = pbi_id)

    pbi_current = pbi

    check = 0
    for _pbi in PBI.objects.order_by('priority').exclude(story_point = 0):
        if(check == 1):
            pbi_current = _pbi
            break
        if(pbi ==  _pbi):
            check = 1

    temp_pbi = pbi.priority
    pbi.priority = pbi_current.priority
    pbi.save()
    pbi_current.priority = temp_pbi
    pbi_current.save()
    uniquePriority()

    return JsonResponse({"message": "decrement operation done"})
    
def uniquePriority():
    priority = 1
    for _pbi in PBI.objects.order_by('priority').exclude(story_point = 0):
        _pbi.priority = priority
        _pbi.save()
        priority += 1