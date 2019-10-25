from django.urls import path
from application import views


app_name = 'application'
urlpatterns = [
    path('', views.BackLogList.as_view(), name = 'product-backlog-item'),
    path('all/', views.BackLogListFullView.as_view(), name='pbi_all'),
    path('action_page.php/', views.addData, name='addData'),
    path('all/action_page.php/', views.addDataAll, name='addData2'),
    path('del/', views.delData, name='delData'),
    path('edit/', views.editData, name='editData'),
    path('all/del/', views.delDataAll, name='delData2'),
    path('all/edit/', views.editDataAll, name='editData2'),

]