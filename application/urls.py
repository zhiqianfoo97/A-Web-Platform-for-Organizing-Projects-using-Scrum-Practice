from django.urls import path
import application.views.product_backlog_views as pb_views
import application.views.sprint_backlog_views as sb_views


app_name = 'application'
urlpatterns = [
    path('productbacklogs/', pb_views.BackLogList.as_view(), name = 'product_backlog'),
    path('productbacklogs/all/', pb_views.BackLogListFullView.as_view(), name='product_backlog_all'),
    path('productbacklogs/action_page.php/', pb_views.addData, name='addData'),
    path('productbacklogs/all/action_page.php/', pb_views.addDataAll, name='addData2'),
    path('productbacklogs/del/', pb_views.delData, name='delData'),
    path('productbacklogs/edit/', pb_views.editData, name='editData'),
    path('productbacklogs/all/del/', pb_views.delDataAll, name='delData2'),
    path('productbacklogs/all/edit/', pb_views.editDataAll, name='editData2'),
    path('productbacklogs/inc/<int:pbi_id>/', pb_views.increasePriority, name="increase_pri"),
    path('productbacklogs/decr/<int:pbi_id>/', pb_views.decreasePriority, name="decrease_pri"),
    path('productbacklogs/all/inc/<int:pbi_id>/', pb_views.increasePriorityAll, name="increase_pri2"),
    path('productbacklogs/all/decr/<int:pbi_id>/', pb_views.decreasePriorityAll, name="decrease_pri2"),

    path('insprint/<int:pbi_id>/',sb_views.InSprintView.as_view(), name='insprint'),
    path('insprint/createtask/', sb_views.createTask, name='createTask'),
    path('insprint/deletetask/', sb_views.deleteTask, name='deleteTask'),
    path('insprint/edittask/', sb_views.editTask, name='editTask'),


]


