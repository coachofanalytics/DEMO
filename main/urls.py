from django.urls import path

from . import views
# from .utils import convert_html_to_pdf

app_name = 'main'
urlpatterns = [
    path('', views.layout, name='layout'),
    path('team/', views.team_list, name='team_view'),
     path('members/', views.combined_view, name='combined_view'),
     path('galley/', views.galley_list, name='galley_list'),
    path('donate/', views.donate_list, name='donate_list'),
    path('history',views.History, name ='history'),
    
  
    
    
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
