from django.urls import path, include
from . import views
from .views import company_propertiesList,company_propertiesCreate,company_properties_update,company_properties_delete
app_name = 'application'
urlpatterns = [
    # path('application/', include('application.urls')),
    #=============================USERS VIEWS=====================================
    #path('', views.home, name='home'),

    path('propertylist/', views.company_propertiesList, name='propertylist'),
    path('propertycreate/', views.company_propertiesCreate, name='propertycreate'),
    path('propertyupdate/<int:pk>/',views.company_properties_update,name='propertyupdate'),
    path('propertydelete/<int:pk>/',views.company_properties_delete,name='propertydelete'),




]
    