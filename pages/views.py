from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def  product_backlog_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/product_backlog.html", {})

def  sprint_backlog_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/sprint_backlog.html", {})