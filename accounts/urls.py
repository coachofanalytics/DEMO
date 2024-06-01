from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('', views.home, name='home'),
    path('sCredentialCategorys_list/', views.sCredentialCategorys_list, name='sCredentialCategorys_list'),
    path('sCredentialCategorys_create/', views.sCredentialCategorys_create, name='sCredentialCategorys_create'),
    path('sCredentialCategorys_update/<int:pk>/', views.sCredentialCategorys_update, name='sCredentialCategorys_update'),
    path('sCredentialCategorys_delete/<int:pk>/', views.sCredentialCategorys_delete, name='sCredentialCategorys_delete'),
    
]

