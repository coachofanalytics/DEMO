import string, random
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  login #authenticate,
from django.utils.decorators import method_decorator
from coda_project import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from requests import request
from django.views.generic.edit import FormView
from .models import User,UserProfile,UserCategory
from .forms import UserForm,LoginForm,UserCategoryForm
from .utils import agreement_data,employees,compute_default_fee
from finance.models import Default_Payment_Fees,Payment_History
from finance.utils import DYCDefaultPayments
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.forms import modelform_factory
from .models import UserCategory
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

class UserCategoryCreateView(CreateView):
    model = UserCategory
    template_name = 'accounts/registration/DYC/select_category.html'
    fields = '__all__'
    success_url = '/accounts/join'
    queryset = UserCategory.objects.none()  # add this line

    def form_valid(self, form):
        # do not save to database
        self.object = form.save(commit=False)
        category = form.cleaned_data.get('category')
        subcategory = form.cleaned_data.get('sub_category')
        self.request.session['category'] = category
        self.request.session['subcategory'] = subcategory
        # self.object.save()
        # print('Instance saved:', self.object.pk)
        return super().form_valid(form)
    

def join(request):
    form = UserForm()
    if request.method == "POST":
        previous_user = User.objects.filter(email=request.POST.get("email"))
        if len(previous_user) > 0:
            messages.success(request, f'User already exists with this email')
            return redirect("/password-reset")
        else:
            contract_data, contract_date = agreement_data(request)
            default_amounts = Default_Payment_Fees.objects.all()
            category = request.session.get('category')
            subcategory = request.session.get('subcategory')
            default_fee = compute_default_fee(category, default_amounts, Default_Payment_Fees)
            context = {"job_support_data": contract_data,
                       "contract_date": contract_date,
                       "payment_data": default_fee
                       }
            form = UserForm(request.POST, request.FILES)
            if form.is_valid():
                if category == 4:
                    form.instance.is_staff = True
                else:
                    form.instance.is_client = True
                first_name = form.instance.first_name
                last_name = form.instance.last_name
                username = (first_name[0] + last_name).lower()
                form.instance.username = username
                form.save()
                user = User.objects.get(username=username)
                user_category = UserCategory(category=category, sub_category=subcategory, user=user, entry_date=timezone.now())
                user_category.save()
                return redirect('accounts:account-login')
            else:
                msg = "error validating form"
    return render(request, "accounts/registration/DYC/register.html", {"form": form})


def CreateProfile():
    users = User.objects.filter(profile=None)
    for user in users:
        UserProfile.objects.create(user=user)


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            request.session["siteurl"] = settings.SITEURL
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            account = authenticate(email=email, password=password)
            if account is not None:
                try:
                    user_category = UserCategory.objects.filter(user=account.id).latest("entry_date")
                    category = user_category.category
                    subcategory = user_category.sub_category
                except UserCategory.DoesNotExist:
                    category = 5
                    subcategory = 6
            # try:
            #     user_category = UserCategory.objects.filter(user=account.id).latest("entry_date")
            #     category = user_category.category
            #     subcategory = user_category.sub_category
            # except UserCategory.DoesNotExist:
            #     # use the default user_category value if there are no UserCategory objects
            #     # user_category = default_user_category_value
            #     category = 5
            #     subcategory = 6
            # CreateProfile()
            # If Category is Staff/employee
            if account is not None and category == 4 and account.is_staff:
                login(request, account)
                return redirect("accounts:userdashboard")

            # If Category is Business #2 
            elif account is not None and category == 2:
                if subcategory == 2:  # B1 Visa
                    login(request, account)
                    return redirect('accounts:userdashboard')
                else:  # B1 Visa
                    login(request, account)
                    return redirect('accounts:userdashboard')
                
            # If Category is Student
            elif account is not None and category == 1:
                if subcategory == 1:  # F1 Visa
                    login(request, account)
                    return redirect('accounts:userdashboard')
                
            # If Category is Staff & Admin
            # elif account is not None and account.is_admin:
            elif account is not None:
                login(request, account)
                return redirect("main:layout")
            
            else:
                # messages.success(request, f"Invalid credentials.Kindly Try again!!")
                msg=f"Invalid credentials.Kindly Try again!!"
                return render(
                        request, "accounts/registration/DYC/login_page.html", {"form": form, "msg": msg}
                    )
    return render(
        request, "accounts/registration/DYC/login_page.html", {"form": form, "msg": msg}
    )



# ================================USERS SECTION================================
@login_required
def userdashboard(request):
    # departments = Department.objects.filter(is_active=True)
    # return render(request, "management/departments/agenda/dck_dashboard.html", {'title': "DCK DASHBOARD"})
    return render(request, "accounts/dashboard/userdashboard.html", {'title': "DCK DASHBOARD"})

# class userslistview(ListView):
#     model=User
#     fields="__all__"
#     template_name="accounts/admin/adminpage.html"

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


@method_decorator(login_required, name="dispatch")
class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = "/accounts/users"

    def test_func(self):
        user = self.get_object()
        # if self.request.user == user.username:
        if self.request.user.is_superuser:
            return True
        return False


def PasswordResetCompleteView(request):
    return render(request, "accounts/registration/password_reset_complete.html")


''' 
class PasswordsChangeView(PasswordChangeView):
    #model=User
    from_class=PasswordChangeForm
    template_name='accounts/registration/password_change_form.html'
    success_url=reverse_lazy('accounts:account-login')

class PasswordsSetView(PasswordChangeView):
    #model=User
    from_class=SetPasswordForm
    success_url=reverse_lazy('accounts:account-login')

def reset_password(email, from_email, template='registration/password_reset_email.html'):
    """
    Reset the password for all (active) users with given E-Mail adress
    """
    form = PasswordResetForm({'email': email})
    #form = PasswordResetForm({'email':'sample@sample.com'})
    return form.save(from_email=from_email, email_template_name=template)
''' 

# ================================EMPLOYEE SECTION================================
def Employeelist(request):
    employee_subcategories,active_employees=employees()
    context={
        "employee_subcategories":employee_subcategories,
        "active_employees":active_employees,
    }
    return render(request, 'accounts/employees/employeelist.html', context)
# ================================CLIENT SECTION================================

def clientlist(request):
    students = User.objects.filter(
                                             Q(category=3), Q(sub_category=2),
                                             Q(is_client=True),Q(is_active=True)
                                          ).order_by("-date_joined")
    jobsupport = User.objects.filter(
                                             Q(category=3), Q(sub_category=1),
                                             Q(is_client=True),Q(is_active=True)
                                          ).order_by("-date_joined")
    interview = User.objects.filter(
                                             Q(category=3), Q(sub_category=2),
                                             Q(is_client=True),Q(is_active=True)
                                          ).order_by("-date_joined")
    dck_users = User.objects.filter(
                                             Q(category=4), Q(sub_category=6),
                                             Q(is_applicant=True),Q(is_active=True)
                                          ).order_by("-date_joined")
    past = User.objects.filter(
                                             Q(category=3)|Q(is_client=True),
                                             Q(is_active=False)
                                          ).order_by("-date_joined")
    context={
        "students": students,
        "jobsupport": jobsupport,
        "interview": interview,
        "dck_users": dck_users,
        "past": past
    }
    if request.user.category == 4 and request.user.sub_category == 6:
        return render(request, "accounts/clients/dcklist.html", context)
    else:
        return render(request, "accounts/clients/clientlist.html", context)

def clientlist(request):
    clients = {
        'students': User.objects.filter(Q(category=3), Q(sub_category=2), Q(is_client=True), Q(is_active=True)).order_by('-date_joined'),
        'jobsupport': User.objects.filter(Q(category=3), Q(sub_category=1), Q(is_client=True), Q(is_active=True)).order_by('-date_joined'),
        'interview': User.objects.filter(Q(category=3), Q(sub_category=2), Q(is_client=True), Q(is_active=True)).order_by('-date_joined'),
        'dck_users': User.objects.filter(Q(category=4), Q(sub_category=6), Q(is_applicant=True), Q(is_active=True)).order_by('-date_joined'),
        'past': User.objects.filter(Q(category=3) | Q(is_client=True), Q(is_active=False)).order_by('-date_joined'),
    }

    template_name = "accounts/clients/clientlist.html"
    if request.user.category == 4 and request.user.sub_category == 6:
        template_name = "accounts/clients/dcklist.html"

    if request.user.category == 4 and request.user.sub_category == 7:
        print ('request.user')
        template_name = "accounts/clients/dyclist.html"

    return render(request, template_name, clients)


@method_decorator(login_required, name="dispatch")
class ClientDetailView(DetailView):
    template_name = "accounts/clients/client_detail.html"
    model = User
    ordering = ["-date_joined "]

@method_decorator(login_required, name="dispatch")
class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    success_url = "/accounts/clients"
    fields = ["category", "address", "city", "state", "country"]
    form = UserForm

    def form_valid(self, form):
        # form.instance.username=self.request.user
        if (
            self.request.user.is_superuser
            or self.request.user.is_admin
            # or self.request.user.is_staff
        ):
            return super().form_valid(form)
        else:
            return False

    def test_func(self):
        # client = self.get_object()
        if (
            self.request.user.is_superuser
            or self.request.user.is_admin
            # or self.request.user.is_staff
        ):
            return True
        else:
            return False

@method_decorator(login_required, name="dispatch")
class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = "/accounts/clients"

    def test_func(self):
        client = self.get_object()
        # if self.request.user == client.username:
        if self.request.user.is_superuser:
            return True
        return False


@login_required(login_url="accounts:account-login")
def profile(request):
    return render(request, "accounts/profile.html")
