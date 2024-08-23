from django.urls import path

from . import views


app_name = 'main'
urlpatterns = [
    path('', views.layout, name='layout'),
    # path('about/', views.about, name='about'),
    path('teammember_list',views.teammember_list, name ='teammember_list'),
    path('teammember_create', views.teammember_create , name = 'teammember_create'),
    path('team/<int:pk>/edit/', views.teammember_update, name='teammember_update'),
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
