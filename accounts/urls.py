from django.urls import path
from . import views
from .views import (UserUpdateView,UserDeleteView,SuperuserUpdateView,
                    ClientUpdateView,ClientDeleteView,ClientDetailView,
                    Employeelist
                    )
app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('', views.home, name='home'),
    path('join/', views.join, name='join'),
    # path('select_category/', views.user_category_create, name='select_category'),
    path('select_category/', views.UserCategoryCreateView.as_view(), name='select_category'),
    path('login/', views.login_view, name='account-login'),
    path('profile/', views.profile, name='account-profile'),
    path('userdashboard/', views.userdashboard, name='userdashboard'),
    path('users/', views.users, name='accounts-users'),
    # path('users/', views.userslistview.as_view(), name='accounts-users'),
    path('processing/', views.userlist, name='processing-users'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(template_name='accounts/admin/user_update_form.html'), name='user-update'),
    path('superuser/<int:pk>/update/', SuperuserUpdateView.as_view(template_name='accounts/admin/user_update_form.html'), name='superuser-update'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(template_name='accounts/admin/user_delete.html'), name='user-delete'),

    #=============================CLIENTS VIEWS=====================================
    path('clients/', views.clientlist, name='clients'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client-update'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),

     #=============================EMPLOYEES VIEWS=====================================
    path('employees/', views.Employeelist, name='employees'),
    path('thank/',views.thank, name='thank-you'),

]