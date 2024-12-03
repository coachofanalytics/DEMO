from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import UserUpdateView, SuperuserUpdateView, register, CustomLoginView

app_name = "accounts"
urlpatterns = [
    # User authentication views
    path('login/', views.login_view, name='login'),  # Login page
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),  # Logout functionality
    path('register/', register, name='register'),  # Register page

    # User management views
    path('profile/', views.profile, name='profile'),  # Profile page
    path('users/', views.users, name='accounts-users'),  # Users list
    path('processing/', views.userlist, name='processing-users'),  # Processing users
    path('user/<int:pk>/update/', UserUpdateView.as_view(
        template_name='accounts/admin/user_update_form.html'
    ), name='user-update'),  # User update
    path('superuser/<int:pk>/update/', SuperuserUpdateView.as_view(
        template_name='accounts/admin/user_update_form.html'
    ), name='superuser-update'),  # Superuser update

    # Additional views
    path('', views.home, name='home'),  # Home page
    path('join/', views.join, name='join'),  # Join functionality
    path('thank/', views.thank, name='thank-you'),  # Thank you page
]
