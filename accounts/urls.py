from django.urls import path
from . import views
from .views import (UserUpdateView,SuperuserUpdateView,register,CustomLoginView
                   
                    )
app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('', views.home, name='home'),
    path('join/',views.join, name ='joins'),
     path('login_view/', views.login_view, name='account-login'),
  
    path('register/', register, name='register'),
    path('profile/', views.profile_view, name='profile_view'),


    path('verify-email/<uuid:token>/', views.verify_email, name='verify-email'),
    path('email-verification-notice/<int:user_id>/', views.email_verification_notice, name='email-verification-notice'),
    path('select-category/', views.select_category, name='select_category'),
    #path('login/', CustomLoginView.as_view(), name='login'),
    path('users/', views.users, name='accounts-users'),
    # path('users/', views.userslistview.as_view(), name='accounts-users'),
    path('processing/', views.userlist, name='processing-users'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(template_name='accounts/admin/user_update_form.html'), name='user-update'),
    path('superuser/<int:pk>/update/', SuperuserUpdateView.as_view(template_name='accounts/admin/user_update_form.html'), name='superuser-update'),
   
    path('thank/',views.thank, name='thank-you'),
    

]