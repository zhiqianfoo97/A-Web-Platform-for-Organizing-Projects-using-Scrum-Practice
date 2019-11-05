from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from application.models import *
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.generic.edit import DeleteView
import datetime

class sprintBackLogList(TemplateView):
    template_name = "backend_test/sprint_backlog.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notCompletedPBI = []
        for pbi_completed in PBI.objects.order_by('priority'):
            if (pbi_completed.getStatus() != "In progress"):
                notCompletedPBI.append(pbi_completed)
        context['in_progress_pbi'] = notCompletedPBI
        
        current_sprint_id = self.get_current_sprint_id()
        context['current_sprint_pbi'] = []
        if current_sprint_id:
            for pbi in PBI.objects.filter(sprint_number = current_sprint_id):
                context['current_sprint_pbi'].append(pbi)
        return context
    
    def get_current_sprint_id(self):
        today = datetime.datetime.today()
        sprints = Sprint.objects.filter(start_date__lte = today, end_date__gte = today)
        if sprints:
            return (sprints[0].pk)
        else:
            return None
    
def add_to_sprint(request):
    print (request.POST)
    return HttpResponseRedirect(reverse('application:product_backlog_all'))