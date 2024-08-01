from django.urls import path
from . import views
from .views import (
                    UserUpdateView,UserDeleteView,SuperuserUpdateView,
                    ClientUpdateView,ClientDeleteView,ClientDetailView,
                   CredentialUpdateView,
                     TrackDeleteView, TrackDetailView,
                    TrackListView, TrackUpdateView,
                    )
app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('', views.home, name='home'),
    path('join/', views.join, name='join'),
    path('login/', views.login_view, name='account-login'),
    path('login_history/<str:username>', views.user_login_history, name='login_history'),
    path('time/<int:pk>/update/', views.edit_login_logout_time, name='time-update'),
    path('users/', views.users, name='accounts-users'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(template_name='accounts/admin/user_update_form.html'), name='user-update'),
    path('superuser/<int:pk>/update/', SuperuserUpdateView.as_view(template_name='accounts/admin/user_update_form.html'), name='superuser-update'),
    #path('user/<int:pk>/update/', UserUpdateView.as_view(template_name='accounts/registration/join.html'), name='user-update'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(template_name='accounts/admin/user_delete.html'), name='user-delete'),

#=============================CREDENTIALS VIEWS=====================================
    path('credentials/', views.credential_view, name='account-crendentials'),
    path('newcredentialcategory/', views.newcredentialCategory, name='account-newcredentialcategory'),
    path('newcredential/', views.newcredential, name='account-newcredentials'),
    path('credential/update/<int:pk>/', CredentialUpdateView.as_view(template_name="accounts/admin/forms/credential_form.html"), name='credential-update'),
    
    path('security_verification/', views.security_verification, name='security_verification'),
    #=============================CLIENTS VIEWS=====================================
    path('clients/', views.clientlist, name='clients'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client-update'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),

     #=============================EMPLOYEES VIEWS=====================================
    path('employees/', views.Employeelist, name='employees'),
    #=============================CLIENTS WORK=====================================
    path('tracker/', TrackListView.as_view(), name='tracker-list'),
    path('client/<str:username>/', views.usertracker, name='user-list'),
    path('track/<int:pk>/', TrackDetailView.as_view(), name='tracker-detail'),
    path('track/<int:pk>/update/', TrackUpdateView.as_view(), name='tracker-update'),
    path('track/<int:pk>/delete/', TrackDeleteView.as_view(), name='tracker-delete'),
    path('thank/',views.thank, name='thank-you'),

]