from django.urls import path
from main.views import AboutView
from main.views import volunteer_update,volunteer_delete,volunteer_detail ,registration_update


from . import views

 
app_name = 'main'
urlpatterns = [
    path('', views.layout, name='layout'),
    path('history',views.History, name ='history'),
    path('gallary',views.gallery_image_list, name ='gallery_image_list'),
    path('Volunteer',views.Volunteers_list, name ='Volunteers_list'),
    path('volunteer_create',views.volunteer_create, name ='volunteer_create'),
    path('volunteers/<int:pk>/update/', volunteer_update, name='volunteer_update'),
    path('volunteers/<int:pk>/delete/', volunteer_delete, name='volunteer_delete'),
    path('volunteers/<int:pk>/', volunteer_detail, name='volunteer_detail'),
    path('registration',views.registration_list, name ='registration_list'),
    path('registration_create',views.registration_create, name ='registration_create'),
    path('registration/<int:pk>/update/', registration_update, name='registration_update'),  
    
  
    
    
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
