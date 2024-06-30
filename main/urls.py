from django.urls import path
from . import views
from .views import Donation_create, Donation_list,Donation_update,Donation_delete

app_name = 'main'
urlpatterns = [
    
    #==============ERRORS==============================================
    path('Donation_list/', views.Donation_list, name='Donation_list'),
    path('Donation_create/', views.Donation_create, name='Donation_create'),
    path('Donation_update/<int:pk>/', Donation_update, name='Donation_update'),
    path('Donation_delete/<int:pk>/', views.Donation_delete, name='Donation_delete'),
    path('gallery_detail/<int:pk>/', views.gallery_detail, name='gallery_detail'), 
    path('team/', views.about, name='team'),

    #=======================SERVICES=====================================
    # path('newservice/', views.ServiceCreateView.as_view(template_name='main/form.html'), name='newservice'),
    # path('services/', views.services, name='services'),
    # path('update/<int:pk>/', views.ServiceUpdateView.as_view(template_name='main/form.html'), name='update_service'),
    # path('delete/<int:id>/', views.delete_service, name='delete_service'),
    #==============DEPARTMENTS==============================================
    path('newprofile/', views.UserCreateView.as_view(template_name='main/form.html'), name='newprofile'),
    path('updateprofile/<int:pk>/', views.UserProfileUpdateView.as_view(template_name='main/form.html'), name='update_profile'),

    #==============ERRORS==============================================
    path('400Error/', views.error400, name='400error'),
    path('403Error/', views.error403, name='403error'),
    path('404Error/', views.error404, name='404error'),
    path('500Error/', views.error500, name='500error'),
    path('errors/', views.template_errors, name='template_errors'),

    # path('400/', views.hendler400, name='400-error'),
    # path('403/', views.handler403, name='403-error'),
    # path('404/', views.handler404, name='404-error'),
    # path('500/', views.handler500, name='500-error'),
]
