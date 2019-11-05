from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from application.models import PBI, Project, Task
from django.urls import reverse
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
        context['single_task'] = Task.objects.filter(pbi_id = _pbi_id)[0]

        return context

