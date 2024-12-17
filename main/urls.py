from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Main Pages
    path('', views.layout, name='layout'),
    path('gallery/', views.gallery_list, name='gallery_list'),
    path('team/', views.team_list, name='team_list'),
    path('combined/', views.combined_view, name='combined_view'),
    path('donate/', views.donate_list, name='donate_list'),
    path('news/', views.news_list, name='news_list'),
    path('history/', views.history, name='history'),

    # Error Pages
    path('400Error/', views.handler400, name='400error'),  # Corrected spelling here
    path('403Error/', views.handler403, name='403error'),  # Corrected spelling here
    path('404Error/', views.handler404, name='404error'),  # Corrected spelling here
    path('500Error/', views.handler500, name='500error'),  # Corrected spelling here
]
