from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from application.models import PBI

# Create your views here.

def product_backlog_view (request,*args,**kwargs):
    return render(request,"pb.html",{})

def sprint_backlog_view (request,*args,**kwargs):
    return render(request,"SB.html",{})

class BackLogList(TemplateView):
    template_name = "pb.html"
    
    def get_context_data(self, **kwargs):
        

        context = super().get_context_data(**kwargs)
        context['pbi_priority_list'] = PBI.objects.order_by('priority')
        context['normal_pbi'] = PBI.objects.all()

        return context

