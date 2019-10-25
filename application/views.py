from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from application.models import PBI, Project
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.generic.edit import DeleteView


# Create your views here.

def product_backlog_view (request):
    return render(request,"pb.html")

def sprint_backlog_view (request,*args,**kwargs):
    return render(request,"SB.html",{})

class BackLogList(TemplateView):
    template_name = "pb.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pbi_priority_list'] = PBI.objects.order_by('priority')
        context['normal_pbi'] = PBI.objects.all()
        
        return context

class BackLogListFullView(TemplateView):
    template_Name = "pbAll.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        completedPBI = []
        for pbi_completed in PBI.objects.order_by('priority'):
            if (pbi_completed.getStatus() != "Completed"):
                completedPBI.append(pbi_completed)
        
        context['full_view_pbi'] = completedPBI
        return context


def addData(request):
    # if( PBI.objects.all().filter(priority = request.POST['prioritypts']).count() > 0):
    #    #return render(request, 'pb.html', {'priority_flag': True},)
    #    return HttpResponseRedirect(reverse('application:product-backlog-item'))
    # else:
    _priority_points = request.POST['prioritypts']
    _user_story = request.POST['userstory']
    _sprint = request.POST['sprint']

    if (_sprint == ''):
        _sprint = None

    _story_point = request.POST['storypts']
    _project_id = Project.objects.get(pk=3)
    
    # p = PBI(user_story = _user_story, sprint_number = _sprint,epic = " ", project_id = _project_id, story_point = _story_point, priority = _priority_points)
    # p.save()
    
    PBI.objects.create_pbi(_user_story, _sprint, _project_id, _story_point, _priority_points)
    return HttpResponseRedirect(reverse('application:product-backlog-item'))
    
def delData(request):
    _pbi_id = request.POST['pbi_id']
    pbi = PBI.objects.get(pk = _pbi_id)
    pbi.delete()
    return HttpResponseRedirect(reverse('application:product-backlog-item'))

def editData(request):
    _pbi_id = request.POST['pbi_id']
    pbi = PBI.objects.get(pk = _pbi_id)
    pbi.user_story = request.POST['user_story']
    if (request.POST['sprint_num'] == ''):
        pbi.sprint_number = None
    else:
        pbi.sprint_number = request.POST['sprint_num']
    pbi.priority = request.POST['priority_points']
    pbi.story_point = request.POST['story_points']
    pbi.save()
    return HttpResponseRedirect(reverse('application:product-backlog-item'))

# def viewAllPBI(request):
#     if (request.POST['fullview'] == '0'):
#         return HttpResponseRedirect(reverse('application:product-backlog-item'))
#     else:
#         return HttpResponseRedirect(reverse('application:BackLogListFullView'))





    