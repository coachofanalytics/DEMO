from django.db.models import Min,Max
from django.db.models import Q
from celery import shared_task
from django.shortcuts import redirect, render
from django.contrib import messages
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
from coda_project import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView,
    UpdateView,
)
from .models import Service,Plan,Assets
from accounts.models import CustomerUser,UserProfile
from .utils import Meetings,image_view,path_values
from accounts.utils import employees
from accounts.forms import LoginForm
from accounts.forms import LoginForm
from .forms import RegistrationForm,ContactForm
from accounts.views import CreateProfile
from PIL import Image
from django.contrib.auth import get_user_model

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
    return render(request, "main/home_templates/layout.html")


# =====================DC_KENYA VIEWS=======================================
def dclayout(request):
    # advertisement()
    
    posts=posts.objects.all()
    services=Service.objects.all()

    context={
            "services":services,
            "posts":posts,
            "title": "DCKENYA"
        }
    return render(request, "main/dc48kenya/dc_layout.html",context)

def register(request):
    if request.method == "POST":
        previous_user = User.objects.filter(email = request.POST.get("email"))
        if len(previous_user) > 0:
            messages.success(request, f'User already exist with this email')
            form = RegistrationForm()
            return redirect("/password-reset")
        else:
            if form.is_valid():
                if form.cleaned_data.get("category") == 4:
                    form.instance.is_applicant = True
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!')
                return redirect('main:dc_login')
    else:
        msg = "error validating form"
        form = RegistrationForm()
    return render(request, "main/dc48kenya/dc_register.html", {"form": form,"msg":msg})


def dc48login(request):
    form = LoginForm(request.POST or None)
    msg = f'account with that username and password does not exist!'
    if request.method == "POST":
        if form.is_valid():
            request.session["siteurl"] = settings.SITEURL
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            account = authenticate(username=username, password=password)
            CreateProfile()
            # If Category is DC48KENYA User
            if account is not None and account.category == 4:
                if account.sub_category == 6:  # contractual
                    login(request, account)
                    return redirect("finance:list-inflow")
                else:  # parttime (agents) & Fulltime
                    login(request, account)
                    # return redirect("management:user_task", username=request.user)
                    return redirect("main:dc_home")
    return render(
       request, "main/dc48kenya/dc_login.html", {"form": form, "msg": msg})
    

# =====================SERVICE VIEWS=======================================
class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    success_url = "/services/"
    fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def services(request):
    services = Service.objects.filter(is_active=True).order_by('serial')
    context = {
        "SITEURL" :settings.SITEURL,
        "services": services
    }
    return render(request, "main/services.html", context)


class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    fields ="__all__"

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("main:services")

    def test_func(self):
        service = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user == service.staff:
            return True
        return False

def delete_service(request,id):
    service = service.objects.get(pk=id)
    if request.user.is_superuser:
        service.delete()
    return redirect('main:services')

    
def about(request):
    # Get active employee team members
    team_members = UserProfile.objects.filter(user__is_employee=True, user__is_active=True, user__is_staff=True)
    
    # Set start and end dates
    start_date_str = "01/20/2023"
    start_date = datetime.strptime(start_date_str, '%m/%d/%Y')
    end_date = start_date + relativedelta(months=3)
    
    # Filter active employees and get their image URLs
    active_employees = [member for member in team_members if member.img_category == 'employee']
    img_urls = [member.img_url for member in active_employees]
    
    # Set context variables
    context = {
        "start_date": start_date,
        "end_date": end_date,
        "title_team": "team",
        "active_employees": active_employees,
        "title_about": "about",
        "img_urls": img_urls,
        "title_letter": "letter",
    }
    
    # Map page names to templates
    templates = {
        'team': 'main/team.html',
        'letter': 'main/doc_templates/letter.html',
        'appointment_letter': 'main/doc_templates/appointment_letter.html',
        'about': 'main/about.html',
    }
    
    # Render the appropriate template based on the page name
    page_name = path_values(request)[-1]
    template = templates.get(page_name, 'main/about.html')
    return render(request, template, context)


class UserCreateView(LoginRequiredMixin, CreateView):
    model = UserProfile
    success_url = "/team/"
    fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    # fields ="__all__"
    fields=['position','description','image','image2','is_active','laptop_status']
    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse("management:companyagenda")

    def test_func(self):
        # profile = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user:
            return True
        return False

def contact(request):
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
    return render(request, "main/contact/contact_message.html", {"form": form})


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