from django.urls import path
from . import views
from .views import (UserUpdateView,SuperuserUpdateView,
                   
                    )
app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('', views.home, name='home'),
  
    path('users/', views.users, name='accounts-users'),
    # path('users/', views.userslistview.as_view(), name='accounts-users'),
    path('processing/', views.userlist, name='processing-users'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(template_name='accounts/admin/user_update_form.html'), name='user-update'),
    path('superuser/<int:pk>/update/', SuperuserUpdateView.as_view(template_name='accounts/admin/user_update_form.html'), name='superuser-update'),
   
    path('thank/',views.thank, name='thank-you'),

]