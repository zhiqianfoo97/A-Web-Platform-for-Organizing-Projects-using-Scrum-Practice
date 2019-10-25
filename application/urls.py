from django.urls import path
from application import views


app_name = 'application'
urlpatterns = [
    path('all', views.BackLogList.as_view(), name = 'product-backlog-item'),
    path('all/action_page.php', views.addData, name='addData'),

]