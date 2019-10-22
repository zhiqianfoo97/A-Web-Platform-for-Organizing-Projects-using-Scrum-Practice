from django.urls import path
from application import views

urlpatterns = [
    path('all',views.BackLogList.as_view(), name = 'product-backlog-item'),

]