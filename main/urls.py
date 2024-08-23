from django.urls import path

from . import views


app_name = 'main'
urlpatterns = [
    path('', views.layout, name='layout'),
    # path('about/', views.about, name='about'),
    path('history',views.History, name ='history'),
    path('teammember_list', views.teammember_list , name = 'teammember_list'),
    path('export_training', views.Export_training , name = 'export'),
    path('G2B_training', views.G2B_training , name = 'G2B'),
    path('plan/<int:course_id>/', views.Plan_training, name='plan'),
    
    
   #==============ERRORS==============================================
    path('400Error/', views.error400, name='400error'),
    path('403Error/', views.error403, name='403error'),
    path('404Error/', views.error404, name='404error'),
    path('500Error/', views.error500, name='500error'),
    path('errors/', views.template_errors, name='template_errors'),

    path('400/', views.hendler400, name='400-error'),
    path('403/', views.hendler403, name='403-error'),
    path('404/', views.hendler404, name='404-error'),
    path('500/', views.hendler500, name='500-error'),

]
