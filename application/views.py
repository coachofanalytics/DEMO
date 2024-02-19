from django.db.models import Q
from django.utils.text import capfirst
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import (
        CreateView,
        DeleteView,
        ListView,
        DetailView,
        UpdateView,
    )
from.models import company_properties
from .forms import propertiesForm

# User=settings.AUTH_USER_MODEL
import json
from coda_project import settings
User = get_user_model

def company_propertiesList(request):
    properties = company_properties.objects.all()
    print("properties====>",properties)  
    return render(request,"application/propertylist.html",{'properties':properties})

def company_propertiesCreate(request):
    if request.method == 'POST':
        form =propertiesForm(request.POST)
        if form.is_valid():
            form.save            
            return redirect("application:propertylist")
    else:
        form = propertiesForm()
        print("form ====>",form) 
    return render(request,"application/propertycreate.html", {'form': form})

def company_properties_update(request,pk):
    properties = get_object_or_404(company_properties,pk=pk)
    if request.method =='POST':
        form =propertiesForm(request.POST,instance = properties)
        if form.is_valid():
            form.save()
            return redirect("application:propertylist")
    else:
        form = propertiesForm(instance= properties)
        return render(request,"application/propertyupdate.html",{'form':form,'properties':properties})
