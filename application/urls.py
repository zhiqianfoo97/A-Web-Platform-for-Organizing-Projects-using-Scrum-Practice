from django.urls import path
import application.views.product_backlog_views as pb_views
import application.views.sprint_backlog_views as sb_views
import application.views.project_views as project_views
import application.views.login_views as lg_views

app_name = 'application'
urlpatterns = [
    path('all_projects/', project_views.ProjectList.as_view(), name = 'all_project_list'),
    path('create_project/', project_views.ProjectList.createProject, name = 'create_project'),
    path('reject_invitation/', project_views.rejectInvitation, name='reject_invite'),
    path('accept_invitation/', project_views.acceptInvitation, name='accept_invite'),
    path('<int:project_id>/end_project/', project_views.ProjectList.endProject, name='end_project'),

    path('<int:project_id>/productbacklogs/', pb_views.BackLogList.as_view(), name = 'product_backlog'),
    path('<int:project_id>/productbacklogs/all/', pb_views.BackLogListFullView.as_view(), name='product_backlog_all'),
    path('productbacklogs/', pb_views.addData, name='addData'),
    path('productbacklogs/all/', pb_views.addDataAll, name='addData2'),
    path('productbacklogs/del/', pb_views.delData, name='delData'),
    path('productbacklogs/edit/', pb_views.editData, name='editData'),
    path('productbacklogs/all/del/', pb_views.delDataAll, name='delData2'),
    path('productbacklogs/all/edit/', pb_views.editDataAll, name='editData2'),
    path('productbacklogs/inc/<int:pbi_id>/<int:project_id>/', pb_views.increasePriority, name="increase_pri"),
    path('productbacklogs/decr/<int:pbi_id>/<int:project_id>/', pb_views.decreasePriority, name="decrease_pri"),

    path('<int:project_id>/sprintlist/', sb_views.SprintList.as_view(), name="sprint_list"),
    path('createSprint/', sb_views.SprintList.createSprint, name="create_sprint"),

    path('<int:project_id>/sprintbacklogs/current', sb_views.SprintBacklogList.as_view(), name="sprint_backlog_current"),
    path('<int:project_id>/sprintbacklogs/<int:sprint_id>', sb_views.PastSprintBacklogList.as_view(), name="past_sprint_backlog_current"),
    path('sprintbacklogs/current/add_to_sprint', sb_views.SprintBacklogList.add_to_sprint, name="add_pbi_to_sprint"),
    path('sprintbacklogs/current/remove_from_sprint', sb_views.SprintBacklogList.remove_from_sprint, name="remove_pbi_from_sprint"),
    path('sprintbacklogs/current/start_sprint/<int:project_id>/<int:sprint_id>/', sb_views.SprintBacklogList.start_sprint, name="start_sprint"),
    path('sprintbacklogs/current/end_sprint/<int:project_id>/<int:sprint_id>/', sb_views.SprintBacklogList.end_sprint, name="end_sprint"),

    path('insprint/<int:project_id>/<int:sprint_num>/<int:pbi_id>/',sb_views.InSprintView.as_view(), name='insprint'),
    path('insprint/createtask/', sb_views.createTask, name='createTask'),
    path('insprint/deletetask/', sb_views.deleteTask, name='deleteTask'),
    path('insprint/edittask/', sb_views.editTask, name='editTask'),
    path('insprint/pickdroptask/', sb_views.pickOrDropTask, name='pickOrDrop'),
    path('insprint/marktaskasdone/', sb_views.markTaskAsDone, name='markDone'),

    path('sprintpage/<int:project_id>/<int:sprint_num>', sb_views.SprintPageView.as_view(), name='sprint_page'),
    path('sprintpage/deletetask/', sb_views.deleteTask2, name='sprint_page_delete'),
    path('sprintpage/edittask/', sb_views.editTask2, name='sprint_page_edit'),
    path('sprintpage/pickdroptask/', sb_views.pickOrDropTask2, name='sprint_page_pickdrop'),
    path('sprintpage/marktaskasdone/', sb_views.markTaskAsDone2, name='sprint_page_done'),

    path('<int:project_id>/inviteteam/', project_views.inviteTeamPage.as_view(), name = 'invite_team'),
    path('inviteteam/send/', project_views.addToTeam, name='add_to_team'),

    path('', lg_views.loginPage.as_view(), name='login_page'),
    path('login', lg_views.loginPage.as_view(), name='login_page'),
    path('login/auth', lg_views.login_auth, name='login_auth'),
    path('logout/', lg_views.logout, name='logout'),
]