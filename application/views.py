from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from application.models import PBI, Project
from django.urls import reverse

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

def addData(request):
    _user_story = request.POST['userstory']
    _sprint = request.POST['sprint']
    if (_sprint == ''):
        _sprint = None
    _story_point = request.POST['storypts']
    _priority_points = request.POST['prioritypts']
    _project_id = Project.objects.get(pk=3)
    p = PBI(user_story = _user_story, sprint_number = _sprint,epic = " ", project_id = _project_id, story_point = _story_point, priority = _priority_points)
    p.save()

    return HttpResponseRedirect(pb)