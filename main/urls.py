from django.urls import path
from main.views import AboutView  # Make sure this line is present

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.layout, name='layout'),
    # path('team/', views.team_list, name='team_view'),
    path('history/', views.History, name='history'),
    path('services/', views.service_list, name='service_list'),
    path('gallery/', views.gallery_list, name='gallery_list'),
    path('news/', views.news_list, name='news_list'),
    path('contract-us/', views.contact_us_list, name='contact_us_list'),
    path('about/', AboutView.as_view(), name='about'),  # This line should work now
    
    #==============ERRORS==============================================
    path('400/', views.hendler400, name='400-error'),
    path('403/', views.hendler403, name='403-error'),
    path('404/', views.hendler404, name='404-error'),
    path('500/', views.hendler500, name='500-error'),
]
