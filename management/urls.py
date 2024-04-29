from django.urls import path
from management import views
from management.views import (
                        # TaskListView,
                        TaskDetailView,
                        TaskUpdateView,TaskDeleteView,UsertaskUpdateView,
                        # AssessListView,
                        TaskCategoryCreateView,TaskGroupCreateView,
                        DepartmentUpdateView, add_requirement_justification,
                        RequirementUpdateView,RequirementDetailView,RequirementDeleteView
                     )

app_name = 'management'
urlpatterns = [
    path('', views.home, name='management-home'),
    #-----------COMPANY REPORTS---------------------------------------
    path('companyagenda/', views.companyagenda, name='companyagenda'),
    path('userdashboard/', views.dckdashboard, name='dckdashboard'),
    # path('companyagenda/updatelinks', views.updatelinks_companyagenda, name='companyagenda-updatelinks'),
    path('update-agenda/<str:title>/<int:pk>/', views.updatelinks_companyagenda, name='update_agenda'),

    #-----------COMPANY POLICIES---------------------------------------
    path('policy/', views.policy, name='policy'),
    path('policies/', views.policies, name='policies'),
    path("policy/<int:pk>/update/", views.PolicyUpdateView.as_view(template_name="management/departments/hr/policy_form.html"), name="policy-update"),

    path('benefits/', views.benefits, name='benefits'),

    #========================Employee Assessment=====================================================
    path("employee_contract/", views.employee_contract, name="employee_contract"),
    path("read_employee_contract/", views.read_employee_contract, name="read_employee_contract"),
    path("confirm_employee_contract/", views.confirm_employee_contract, name="confirm_employee_contract"),
    path('tasks/', views.tasklist, name='tasks'),
    path("reset_tasks/",views.reset_task,name="reset_tasks"),
    path('score_report/', views.score_report, name='score_report'),
    # path('filterbycategorytag', views.filterbycategorytag, name='filterbycategorytag'),
    # path('newlink/', TaskCreateView.as_view(), name='newlink'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='taskdetail'),
    path('newevidence/<int:taskid>', views.newevidence, name='new_evidence'),
    path('evidence/',views.evidence, name='evidence'),
    path('userevidence/<str:username>/',views.userevidence, name='user_evidence'),
    path('<id>/update', views.evidence_update_view ,name='evidence_update'),
    # path('<int:pk>/update', views.EvidenceUpdateView.as_view(template_name='management/daf/evidence_form.html') ,name='evidence_update'),
    path('taskhistory/', views.historytasks, name='taskhistory'),
    path('getaveragetargets/', views.getaveragetargets, name='getaveragetargets'),
    path('employee/<str:username>/',views.usertask, name='user_task'),
    path('task_employee/<str:username>/',views.usertaskhistory, name='user_task_history'),
    # path('task_employee/<int:pk>/',views.usertaskhistory, name='user_task_history'),
    path('payslip/<str:username>/',views.usertask, name='user_payslip'),
    path('task_payslip/<str:username>/',views.task_payslip, name='task_payslip'),
    path('newtask/', views.newtaskcreation, name='newtask'),
    path('gettasksuggestions/', views.gettasksuggestions, name='gettasksuggestions'),
    path('verifytaskgroupexists/', views.verifytaskgroupexists, name='verifytaskgroupexists'),

    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='updatetask'),
    path('usertask/<int:pk>/update/', UsertaskUpdateView.as_view(), name='userupdatetask'),
    path('gettotalduration/', views.gettotalduration, name='gettotalduration'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='deletetask'),
    path('newcategory/', TaskCategoryCreateView.as_view(), name='newcategory'),
    path('newtaskgroup/', TaskGroupCreateView.as_view(template_name="main/snippets_templates/generalform.html"), name='newtaskgroup'),
    path('contract/',views.contract, name='contract'),

    path('newclient/', views.clientassessment, name='newclient'),
    path('clientassessment/', views.ClientAssessmentListView.as_view(), name='clientassessment'),
    path('new_grievance/', views.grievance_form, name='new_grievance'),
    path('grievance_file/<str:slug>', views.grievance_file, name='grievance_file'),
    path('update_grievance/<int:pk>/', views.GrievanceUpdateView.as_view(template_name="main/snippets_templates/generalform.html"), name='update_grievance'),
    path('update_resolution/<int:pk>/', views.ResolutionUpdateView.as_view(template_name="main/snippets_templates/generalform.html"), name='update_resolution'),
    path('update_assessment/<int:pk>/', views.AssessmentUpdateView.as_view(template_name="main/snippets_templates/generalform.html"), name='update_assessment'),
    path('assess/', views.assess, name='assess'),
    # path('assessment/', AssessListView.as_view(), name='assessment'),
    path('assessment/<str:user_type>', views.dsulist, name='assessment'),
    path('update_dsu/<int:pk>/', views.AssessUpdateView.as_view(template_name="main/snippets_templates/generalform.html"), name='update_dsu'),
    path('session/', views.SessionCreateView.as_view(template_name="main/snippets_templates/generalform.html"), name='session'),
    path('session/<int:pk>/', views.SessionUpdateView.as_view(template_name="main/snippets_templates/generalform.html"), name='updatesession'),
    path('sessions/', views.sessions, name='sessions'),
    path('usersession/<str:username>/',views.usersession, name='user_session'),

    path('newdepartment/', views.newdepartment, name='newdepartment'),
    path('departments/', views.department, name='departments'),
    path('department/<int:pk>/', DepartmentUpdateView.as_view(template_name='management/tag_form.html'), name='department-update'),
    path('newmeeting/', views.newmeeting, name='newmeeting'),
    # path('meetings/', views.meetings, name='meetings'),
    path('meetings/<str:status>', views.meetings, name='meetings'),
    path('meeting/<int:pk>/', views.MeetingUpdateView.as_view(template_name='main/snippets_templates/generalform.html'), name='meeting-update'),

    #========================REQUIREMENTS SECTION=====================================================
    path('requirement/new', views.newrequirement, name='new_requirement'),
    path('form_submission_view/', views.form_submission_view, name='form_submission_view'),
    path('requirements/', views.requirements, name='requirements'),
    path('activerequirements/', views.active_requirements, name='requirements-active'),
    path('client_requirements/', views.requirements, name='client_requirements'),
    path('coda_requirements/', views.requirements, name='coda_requirements'),
    path('dyc_requirements/', views.requirements, name='dyc_requirements'),
    path('reviewed/', views.requirements, name='reviewed'),
    path('tested/', views.requirements, name='tested'),
    path('requirement/<int:pk>/update/', RequirementUpdateView.as_view(template_name='management/doc_templates/requirement_form.html'), name='requirement-update'),
    path('requirement/<int:pk>/delete/', RequirementDeleteView.as_view(), name='requirement-delete'),
    path('requirement/<int:pk>/', RequirementDetailView.as_view(), name='RequirementDetail'),
    path('requirementvideo/<int:detail_id>/', views.videolink, name='video_req_code'),
    # path('addjustification/<int:detail_id>/', views.add_requirement_justification, name='addjustification'),
    path('justification/<int:pk>/', views.justification, name='justification'),
    path('add_justification/', views.add_requirement_justification, name='addjustification'),


    path("create_advertisement/", views.AdsCreateView.as_view(), name="create_advertisement"),
    path("advertisement/", views.AdsContent.as_view(), name="advertisement"),
    path("update_advertisement/<int:pk>/", views.AdsUpdateView.as_view(), name="update_advertisement"),
    path('FilterUsersByLoan/', views.FilterUsersByLoan, name='FilterUsersByLoan'),

]
