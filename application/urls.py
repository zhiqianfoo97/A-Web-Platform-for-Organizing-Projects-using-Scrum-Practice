from django.urls import path
import application.views.product_backlog_views as pb_views
import application.views.sprint_backlog_views as sb_views
import application.views.project_views as project_views

app_name = 'application'
urlpatterns = [
    path('all_projects/', project_views.ProjectList.as_view(), name = 'all_project_list'),
    path('create_project/', project_views.ProjectList.createProject, name = 'create_project'),

    path('<int:project_id>/productbacklogs/', pb_views.BackLogList.as_view(), name = 'product_backlog'),
    path('<int:project_id>/productbacklogs/all/', pb_views.BackLogListFullView.as_view(), name='product_backlog_all'),
    path('productbacklogs/action_page.php/', pb_views.addData, name='addData'),
    path('productbacklogs/all/action_page.php/', pb_views.addDataAll, name='addData2'),
    path('productbacklogs/del/', pb_views.delData, name='delData'),
    path('productbacklogs/edit/', pb_views.editData, name='editData'),
    path('productbacklogs/all/del/', pb_views.delDataAll, name='delData2'),
    path('productbacklogs/all/edit/', pb_views.editDataAll, name='editData2'),
    path('productbacklogs/inc/<int:pbi_id>/<int:project_id>/', pb_views.increasePriority, name="increase_pri"),
    path('productbacklogs/decr/<int:pbi_id>/<int:project_id>/', pb_views.decreasePriority, name="decrease_pri"),

    path('<int:project_id>/sprintlist/', sb_views.SprintList.as_view(), name="sprint_list"),

    path('<int:project_id>/sprintbacklogs/current', sb_views.SprintBacklogList.as_view(), name="sprint_backlog_current"),
    path('sprintbacklogs/current/add_to_sprint', sb_views.SprintBacklogList.add_to_sprint, name="add_pbi_to_sprint"),
    path('sprintbacklogs/current/remove_from_sprint', sb_views.SprintBacklogList.remove_from_sprint, name="remove_pbi_from_sprint"),

    path('<int:project_id>/insprint/<int:pbi_id>/',sb_views.InSprintView.as_view(), name='insprint'),
    path('insprint/createtask/', sb_views.createTask, name='createTask'),
    path('insprint/deletetask/', sb_views.deleteTask, name='deleteTask'),
    path('insprint/edittask/', sb_views.editTask, name='editTask'),
    path('insprint/pickdroptask/', sb_views.pickOrDropTask, name='pickOrDrop'),
    path('insprint/marktaskasdone/', sb_views.markTaskAsDone, name='markDone'),

    path('sprintpage/<int:project_id>/<int:sprint_num>', sb_views.SprintPageView.as_view(), name='sprint_page'),
]