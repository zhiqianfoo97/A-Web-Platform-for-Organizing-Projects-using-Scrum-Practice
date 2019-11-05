from django.urls import path
import application.views.product_backlog_views as pb_views


app_name = 'application'
urlpatterns = [
    path('', pb_views.BackLogList.as_view(), name = 'product_backlog'),
    path('all/', pb_views.BackLogListFullView.as_view(), name='product_backlog_all'),
    path('action_page.php/', pb_views.addData, name='addData'),
    path('all/action_page.php/', pb_views.addDataAll, name='addData2'),
    path('del/', pb_views.delData, name='delData'),
    path('edit/', pb_views.editData, name='editData'),
    path('all/del/', pb_views.delDataAll, name='delData2'),
    path('all/edit/', pb_views.editDataAll, name='editData2'),
    path('inc/<int:pbi_id>/', pb_views.increasePriority, name="increase_pri"),
    path('decr/<int:pbi_id>/', pb_views.decreasePriority, name="decrease_pri"),
    path('all/inc/<int:pbi_id>/', pb_views.increasePriorityAll, name="increase_pri2"),
    path('all/decr/<int:pbi_id>/', pb_views.decreasePriorityAll, name="decrease_pri2"),
]