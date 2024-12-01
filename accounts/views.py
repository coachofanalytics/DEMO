import secrets
import string, random
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
from .models import CustomerUser
from .forms import CustomAuthenticationForm, CustomUserCreationForm, UserForm,LoginForm
from finance.utils import DYCDefaultPayments
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
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
        if previous_user:
            messages.success(request, f'User already exists with this email')
            return redirect("/password-reset")
        else:
            
            form = UserForm(request.POST)  # Assign form with request.POST data
            if form.is_valid():
                if form.cleaned_data.get('category') in [CategoryChoices.CLIENT]:
                    form.instance.is_client = True
                    random_password = generate_random_password(8)
                    form.instance.username = form.cleaned_data.get('email')
                    form.instance.password1 = random_password
                    form.instance.password2 = random_password
                    form.instance.gender = None
                    # form.instance.phone = "0000000000"

                if form.cleaned_data.get("category") == CategoryChoices.STAFF_MEMBER:
                    form.instance.is_staff = True
               
                form.save()
                return redirect('accounts:account-login')

    else:
        msg = "error validating form"
        print(msg)
    
    return render(request, "accounts/registration/DC48K/joins.html", {"form": form})  
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == 'GET':
        sociallogin = request.session.pop("socialaccount_sociallogin", None)
        if sociallogin is not None:
            msg = 'Error with social login. Check your credentials or try to sign up manually.'

    if request.method == "POST":
        if form.is_valid():
            print('Form is valid')
            request.session["siteurl"] = settings.SITEURL
            username_or_email = form.cleaned_data.get("enter_your_username_or_email")
            enter_your_password = form.cleaned_data.get("enter_your_password")
            print(f'Username or Email: {username_or_email}')

            # Try to get the user by username
            user = authenticate(request, username=username_or_email, password=enter_your_password)
            if user is None:
                # If authentication with username failed, try email
                UserModel = get_user_model()
                try:
                    user_obj = UserModel.objects.get(email__iexact=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=enter_your_password)
                except UserModel.DoesNotExist:
                    pass

            if user:
                print('User authenticated')
                login(request, user)
                return redirect('https://dc48k.org/')
            else:
                print('Authentication failed')
                msg = 'Invalid credentials'
        else:
            print('Form is invalid')
            msg = 'Error validating the form'

            
    return render(request, "accounts/registration/DC48K/login_page.html", {"form": form, "msg": msg}  )



@login_required
def userlist(request):
    users = CustomerUser.objects.filter(transaction_sender__amount__gte=5000).distinct()
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
    users = CustomerUser.objects.filter(is_active=True).order_by("-date_joined")
    template_name="accounts/admin/adminpage.html"
    context={
        "users": users,
    }

    if request.user.is_superuser:
        return render(request, template_name, context)
    else:
        return redirect("main:layout")
    

class SuperuserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomerUser
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
    model = CustomerUser
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
