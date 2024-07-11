import secrets
import string, random
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  login #authenticate,
from django.utils.decorators import method_decorator
from accounts.choices import CategoryChoices
from coda_project import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest
from django.contrib.auth.views import LoginView
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from requests import request
from django.views.generic.edit import FormView
from .models import CustomerUser, User
from .forms import CustomAuthenticationForm, CustomUserCreationForm, UserForm,LoginForm
from .utils import agreement_data,employees,compute_default_fee
from finance.models import Default_Payment_Fees,Payment_History
from finance.utils import DYCDefaultPayments
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.forms import modelform_factory
from finance.models import Transaction
from django.core.exceptions import ValidationError
from main.utils import path_values
# Create your views here..


# path_values
# path_val,sub_title=path_values(request)

# @allowed_users(allowed_roles=['admin'])
def home(request):
    return render(request, "main/home_templates/layout.html")


# @allowed_users(allowed_roles=['admin'])
def thank(request):
    return render(request, "accounts/clients/thank.html")


# ---------------ACCOUNTS VIEWS----------------------
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/registration/DC48K/registers.html', {'form': form})

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'accounts/registration/DC48K/logins.html'
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%&"
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password
def join(request):
    form = UserForm()  # Define form variable with initial value
    if request.method == "POST":
        previous_user = CustomerUser.objects.filter(email=request.POST.get("email"))
        if len(previous_user) > 0:
            messages.success(request, f'User already exists with this email')
            return redirect("/password-reset")
        else:
            contract_data, contract_date = agreement_data(request)
            form = UserForm(request.POST)  # Assign form with request.POST data
            if form.is_valid():
                if form.cleaned_data.get('category') in [CategoryChoices.Jobsupport,CategoryChoices.Student,CategoryChoices.investor,CategoryChoices.General_User]:

                    random_password = generate_random_password(8)
                    form.instance.username = form.cleaned_data.get('email')
                    form.instance.password1 = random_password
                    form.instance.password2 = random_password
                    form.instance.gender = None
                    # form.instance.phone = "0000000000"

                if form.cleaned_data.get("category") == CategoryChoices.Coda_Staff_Member:
                    form.instance.is_staff = True
                elif form.cleaned_data.get("category") == CategoryChoices.Jobsupport or form.cleaned_data.get("category") == CategoryChoices.Student or form.cleaned_data.get("category") == CategoryChoices.investor:
                    form.instance.is_client = True
                else:
                    form.instance.is_applicant = True

                form.save()

    else:
        msg = "error validating form"
        print(msg)
    
    return render(request, "accounts/registration/DC48K/joins.html", {"form": form})    

def authenticate(email=None, password=None, **kwargs):
    try:
        users = User.objects.filter(email=email)
        if users.exists():
            user = users.first()
            if user.check_password(password):
                return user
    except User.DoesNotExist:
        return None

    return None


@login_required
def userlist(request):
    users = User.objects.filter(transaction_sender__amount__gte=5000).distinct()
    template_name = "accounts/admin/processing_users.html"

    context={
        "users": users,
    }
    if request.user.is_superuser:
        return render(request, template_name, context)
    else:
        return redirect("main:layout")
    

@login_required
def users(request):
    users = User.objects.filter(is_active=True).order_by("-date_joined")
    template_name="accounts/admin/adminpage.html"
    context={
        "users": users,
    }

    if request.user.is_superuser:
        return render(request, template_name, context)
    else:
        return redirect("main:layout")
    

class SuperuserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    success_url = "/accounts/users"
    fields = [
        "category",
        "sub_category",
        "first_name",
        "last_name",
        "username",
        "date_joined",
        "email",
        "gender",
        "phone",
        "address",
        "city",
        "state",
        "country",
        "is_superuser",
        "is_admin",
        "is_staff",
        "is_client",
        "is_applicant",
        "is_active",
        "is_staff",
    ]

    def form_valid(self, form):
        # form.instance.username=self.request.user
        # if request.user.is_authenticated:
        if self.request.user.is_superuser:  # or self.request.user.is_authenticated :
            return super().form_valid(form)
        #  elif self.request.user.is_authenticated:
        #      return super().form_valid(form)
        return False

    def test_func(self):
        user = self.get_object()
        # if self.request.user == client.username:
        #     return True
        if self.request.user.is_superuser:  # or self.request.user == user.username:
            return True
        return False


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    success_url = "/accounts/users"
    # fields=['category','address','city','state','country']
    fields = [
        # "category",
        # "sub_category",
        "first_name",
        "last_name",
        "date_joined",
        "email",
        "gender",
        "phone",
        # "address",
        # "city",
        # "state",
        # "country",
        "is_admin",
        "is_staff",
        "is_client",
        "is_applicant",
    ]

    def form_valid(self, form):
        # form.instance.username=self.request.user
        # if request.user.is_authenticated:
        if self.request.user.is_superuser or self.request.user.is_admin:
            return super().form_valid(form)
        #  elif self.request.user.is_admin:
        #       return super().form_valid(form)
        return False

    def test_func(self):
        user = self.get_object()
        # if self.request.user == client.username:
        #     return True
        if self.request.user.is_superuser or self.request.user.is_admin:
            return True
        return False



# def membership_registration_view(request):
#     if request.method == 'POST':
#         form = MemberRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success_page')  # Redirect to a success page after registration
#     else:
#         form = MemberRegistrationForm()
    
#     membership_plans = MembershipPlan.objects.all()
    
#     context = {
#         'form': form,
#         'membership_plans': membership_plans,
#     }
    
#     return render(request, 'main/membership_registration.html', context)
