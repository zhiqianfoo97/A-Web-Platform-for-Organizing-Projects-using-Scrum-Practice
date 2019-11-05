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
    template_name = "backend_test/sprint_backlog.html"
    
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
                    notCompletedPBI.append(pbi.simple_deserialise())
                elif pbi.sprint_number.pk == current_sprint_id:
                    current_sprint_pbi.append(pbi.simple_deserialise())
                else:
                    notCompletedPBI.append(pbi.simple_deserialise())
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