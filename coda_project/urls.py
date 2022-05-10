"""
coda_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls import handler400
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.auth import views as auth_views

from accounts import views as account_views
#from accounts.views import account_views PasswordsChangeView ,PasswordsSetView,
from coda_project import settings
from testing import AdminViews, views

#===========ERROR HANDLING SECTION================
handler400='main.views.hendler400'
handler403='main.views.hendler403'
handler300='main.views.hendler300'
handler500='main.views.hendler500'


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    #path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    #path('join/', account_views.join, name='accounts-join'),
    #path('profile/', account_views.profile, name='account-profile'),
    #path('login/', account_views.login_view, name='accounts-login_view'),
    #path('login/', auth_views.LoginView.as_view(template_name='accounts/registration/login.html'), name='account-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/registration/logout.html'), name='account-logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/registration/password_reset.html'), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='accounts/registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    #path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/registration/password_reset_complete.html'), name='password_reset_complete'),
    path('password-reset-complete/', account_views.PasswordResetCompleteView, name='password_reset_complete'),
   
    #path('password-change/', PasswordsChangeView.as_view(),{'post_change_redirect': 'accounts:password_change_done'}, name='password_change'),
    #path('password-set/', PasswordsSetView.as_view(template_name='accounts/registration/password_set_form.html'), name='password_set'),
    #path('reset-password/', account_views.reset_password, name='reset-password'),
    
    #path(r'^password_change/$',auth_views.password_change, {'post_change_redirect': 'league:password_change_done'},
    #name='password_change'),
    
    #path('users/', include('users.urls')),
    path('', include('main.urls', namespace='main')),
    #path('accounts/', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('accounts.urls')),
    path('data/', include('data.urls', namespace='data')),
    path('getdata/', include('getdata.urls', namespace='getdata')),
    path('application/', include('application.urls', namespace='application')),
    path('projectmanagement/', include('projectmanagement.urls', namespace='projectmanagement')),
    path('blog/', include('codablog.urls', namespace='blog')),
    path('investing/', include('investing.urls', namespace='investing')),
    #path('store/', include('store.urls'),name='store'),
    path('management/', include('management.urls',namespace='management')),
    path('globalsearch/', include('globalsearch.urls'),name='search'),
    
    path('testing/', include('testing.urls', namespace='testing')),
    path('admindashboard/',include("testing.adminurls"))


]


if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
