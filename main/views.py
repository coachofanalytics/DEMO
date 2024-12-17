from django.shortcuts import redirect, render, get_object_or_404
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.apps import AppConfig
from django.contrib.auth import get_user_model

from .models import (
    Assets, Description, News, Page, Service,
    SubService, Team, MembershipPlan, Memberregistration, GallerysImagess,
    Volunteerdata, Donation  # Added missing imports
)
from .forms import ContactForm
from .utils import image_view, path_values

User = get_user_model()

# ==================== ERROR HANDLERS =====================

def handler400(request, exception):
    return render(request, "main/errors/400.html", {"title": "400 Error"})

def handler403(request, exception):
    return render(request, "main/errors/403.html", {"title": "403 Error"})

def handler404(request, exception):
    return render(request, "main/errors/404.html", {"title": "404 Error"})

def handler500(request):
    return render(request, "main/errors/500.html", {"title": "500 Error"})

def general_errors(request):
    context = {'message': 'Something went wrong.'}
    return render(request, 'main/errors/generalerrors.html', context)

# ==================== CONFIGURATION =====================

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from .models import Page
        # Initialize the 'Home' page if it doesn't exist
        if not Page.objects.filter(page_name='Home').exists():
            Page.objects.create(page_name='Home', content='Default home page content')

# ==================== VIEWS =====================

@login_required
def layout(request):
    page_instance = get_object_or_404(Page, page_name='Home')
    description = Description.objects.filter(page=page_instance)
    service = Service.objects.all()
    subservice = SubService.objects.all()
    news = News.objects.all().order_by('-published_date')[:3]

    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.task = 'NA'
            instance.plan = 'NA'
            instance.trained_by = request.user
            instance.save()
            context = {"message": "Thank you, we will get back to you within 48 hours."}
            return render(request, "main/errors/generalerrors.html", context)
    else:
        form = ContactForm()

    context = {
        "form": form,
        'description': description,
        'service': service,
        'news': news,
        'subservice': subservice
    }
    return render(request, "main/home_templates/home.html", context)

@login_required
def history(request):
    page_instance = get_object_or_404(Page, page_name='About')
    description = Description.objects.filter(page=page_instance)
    context = {'description': description}
    return render(request, "main/about_templates/history.html", context)

class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Assets
    fields = ["name", "category", "description", "image_url"]
    success_url = "/images/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def images(request):
    all_images = Assets.objects.all()
    return render(request, "main/snippets_templates/static/images.html", {
        "title": "Images",
        "images": all_images
    })

class ImageUpdateView(LoginRequiredMixin, UpdateView):
    model = Assets
    fields = ['category', 'name', 'image_url', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:images')

@login_required
def team_list(request):
    teams = Team.objects.all()
    return render(request, 'main/snippets_templates/table/team2.html', {'teams': teams})

@login_required
def combined_view(request):
    memberregistrations = Memberregistration.objects.all()
    membership_plans = MembershipPlan.objects.all()
    return render(request, 'main/snippets_templates/table/combined.html', {
        'memberregistrations': memberregistrations,
        'membership_plans': membership_plans
    })

@login_required
def gallery_list(request):
    gallery_images = GallerysImagess.objects.all()
    return render(request, 'main/snippets_templates/table/gallery.html', {'gallery_images': gallery_images})

@login_required
def donate_list(request):
    volunteers = Volunteerdata.objects.all()  # Fix: correct import
    donations = Donation.objects.all()  # Fix: correct import
    return render(request, 'main/snippets_templates/table/donate.html', {
        'volunteers': volunteers,
        'donations': donations
    })

@login_required
def news_list(request):
    news = News.objects.all()
    return render(request, 'main/snippets_templates/table/news.html', {'news': news})

def test(request):
    return render(request, "main/test.html", {"title": "Test Page"})

def checkout(request):
    return render(request, "main/checkout.html", {"title": "Checkout"})
