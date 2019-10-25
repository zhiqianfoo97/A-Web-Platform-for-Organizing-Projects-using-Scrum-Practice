from django.urls import path
from application import views


app_name = 'application'
urlpatterns = [
    path('', views.BackLogList.as_view(), name = 'product-backlog-item'),
    path('action_page.php/', views.addData, name='addData'),
    path('del/', views.delData, name='delData'),
    path('edit/', views.editData, name='editData'),
    # path('all/', views.BackLogList.as_view(), name = 'pbi_all'),

]