from django.shortcuts import redirect, render
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView,
    UpdateView,
)
from .models import Assets,Description, News, Page, Pricing, Service, SubService,Training,business

from django.shortcuts import render
from .utils import image_view,path_values
from main.forms import ContactForm
from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import Investment
# views.py



User=get_user_model()


def error400(request):
    return render(request, "main/errors/400.html", {"title": "400Error"})

def error403(request):
    return render(request, "main/errors/403.html", {"title": "403Error"})

def error404(request):
    return render(request, "main/errors/404.html", {"title": "404Error"})
    
def error500(request):
    return render(request, "main/errors/500.html", {"title": "500Error"})

#Other Error pages or no results error

def template_errors(request):
    url = request.path
    contact = 'Please contact admin at info@codanalytics.net'
    title = ['Bad Request', 'Permission Denied', 'Page Not Found', 'System Issue']

    # Map each error code to its corresponding context
    context_dict = {
        400: {'title': title[0], 'error_message': 'Kindly check your URL/link provided', 'contact_message': contact},
        403: {'title': title[1], 'error_message': 'You are not allowed to visit this page', 'contact_message': contact},
        404: {'title': title[2], 'error_message': 'Page not found', 'contact_message': contact},
        500: {'title': title[3], 'error_message': 'There is an issue on our end. Please try again later.', 'contact_message': contact},
    }

    # Get the context based on the error code, or use a default context
    error_code = getattr(url, 'response', None)
    context = context_dict.get(error_code, {'title': 'Error', 'error_message': 'An error has occurred', 'contact_message': contact})

    print(error_code)
    return render(request, 'main/errors/template_error.html', context)


def general_errors(request):
    # return render(request, "main/errors/noresult.html")
    context={'message':'message'}
    return render(request,'main/errors/generalerrors.html',context)

#  ===================================================================================   
def hendler400(request,exception):
    return render(request, "errors/400.html")

def hendler403(request,exception):
    return render(request, "main/errors/403.html")

def hendler404(request,exception):
    return render(request, "main/errors/404.html")

def hendler404(request,exception):
    return render(request, "main/errors/404.html")

def hendler500(request):
    return render(request, "main/errors/500.html")
    
def test(request):
    return render(request, "main/test.html", {"title": "test"})

def checkout(request):
    return render(request, "main/checkout.html", {"title": "checkout"})

from django.shortcuts import get_object_or_404


def layout(request):
    page_instance = Page.objects.get(page_name='Home')
    description = Description.objects.filter(page = page_instance)
    
    news = News.objects.all().order_by('-published_date')[:5] 
    # print(news)
   
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        message=f'Thank You, we will get back to you within 48 hours.'
        context={
            "message":message,
            # "link":SITEURL+'/management/companyagenda'
        }
        if form.is_valid():
            # form.save()
            instance=form.save(commit=False)
            # instance.client_name='admin',
            instance.task='NA',
            instance.plan='NA',
            instance.trained_by=request.user
            instance.save()
            # return redirect("management:assessment")
            return render(request, "main/errors/generalerrors.html",context)
    else:
        form = ContactForm()
    context={
            # "posts":posts,
            "form": form,
            'description': description,
           
            'news':news,
            
        }
    return render(request, "main/home_templates/home.html",context)


def History(request):
    page_instance = Page.objects.get(page_name='About')
    description = Description.objects.filter(page = page_instance)
    context={
            
            'description': description,
            
        }
    return render(request, "main/about_templates/history.html",context)

class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Assets
    success_url = "/images/"
    # fields = ["title", "description"]
    fields = ["name",'category', "description","image_url"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
        
def images(request):
    # images = Assets.objects.all().first()
    images = Assets.objects.all()
    # print(images)
    return render(request, "main/snippets_templates/static/images.html", {"title": "pay", "images": images})

class ImageUpdateView(LoginRequiredMixin,UpdateView):
    model=Assets
    fields = ['category','name','image_url','description']
     
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:images') 
def Import_training(request):
    course = Training.objects.all()
    page_instance = Page.objects.get(page_name='Import Training')
    description = Description.objects.filter(page = page_instance)  
    context = {
        'description': description,
        'course': course
    }
   
    return render(request , 'main/training/import.html', context)    
def Export_training(request):
    course = Training.objects.all()
    page_instance = Page.objects.get(page_name='Export Training')
    description = Description.objects.filter(page = page_instance)
    context = {
        'description': description,
        'course': course
    }
    return render(request , 'main/training/export.html',context)  
def G2B_training(request):
    return render(request , 'main/training/G2B.html') 
def Plan_training(request, course_id):
    # Retrieve the specific Training object by ID
    training = get_object_or_404(Training, id=course_id)
    
    # Pass the training object and its related Pricing objects to the template
    return render(request, 'main/training/plans.html', {'training': training})





def investment__page(request):
    page_instance = Page.objects.get(page_name='Investment')
    description = Description.objects.filter(page = page_instance)


    context ={
        'description':description
    }
    
    return render(request, 'main/services/investment.html',context)


def business_page(request):
    page_instance = Page.objects.get(page_name='business')
    description = Description.objects.filter(page=page_instance)
    businesses = business.objects.all()  # Ensure correct capitalization of the model name

    # Process features safely within the loop
    for item in businesses:
        # Check if `features` is a string, and only then split
        if isinstance(item.features, str):
            item.features = item.features.split(',')  # Split the features into a list

    context = {
        'description': description,
        'businesses': businesses,
    }
    return render(request, 'main/services/business.html', context)

def International_trade(request):
    return render(request, 'main/services/International_trade.html')
