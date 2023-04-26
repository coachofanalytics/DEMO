from django.urls import path

from . import views
# from .utils import convert_html_to_pdf

app_name = 'main'
urlpatterns = [
    path('', views.layout, name='layout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
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

    path('400/', views.hendler400, name='400-error'),
    path('403/', views.hendler403, name='403-error'),
    path('404/', views.hendler404, name='404-error'),
    path('500/', views.hendler500, name='500-error'),

]
