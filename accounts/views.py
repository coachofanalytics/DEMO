import string, random
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from coda_project import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from .models import User,CustomUser, Department,UserProfile
from .forms import UserForm,LoginForm
from .utils import agreement_data,employees,compute_default_fee
from finance.models import Default_Payment_Fees,Payment_History
from finance.utils import DYCDefaultPayments

# Create your views here..

# @allowed_users(allowed_roles=['admin'])
def home(request):
    return render(request, "main/home_templates/layout.html")


# @allowed_users(allowed_roles=['admin'])
def thank(request):
    return render(request, "accounts/clients/thank.html")


# ---------------ACCOUNTS VIEWS----------------------
def join(request):
    if request.method == "POST":
        previous_user = User.objects.filter(email = request.POST.get("email"))
        if len(previous_user) > 0:
            messages.success(request, f'User already exist with this email')
            form = UserForm()
            return redirect("/password-reset")
        else:
            contract_data,contract_date=agreement_data(request)
            dyc_total_amount,dyc_down_payment,early_registration_bonus=DYCDefaultPayments()
            if request.POST.get("category") == "3":
                check_default_fee = Default_Payment_Fees.objects.all()
                if check_default_fee:
                    # default_fee = Default_Payment_Fees.objects.get(id=1)
                    default_fee = Default_Payment_Fees.objects.all().first()
                else:
                    default_payment_fees = Default_Payment_Fees(
                        job_down_payment_per_month=1000,
                        job_plan_hours_per_month=40,
                        student_down_payment_per_month=500,
                        student_bonus_payment_per_month=100,
                    )
                    default_payment_fees.save()
                    default_fee = Default_Payment_Fees.objects.all().first()
                if (
                    request.POST.get("category") == "3"
                    and request.POST.get("sub_category") == "1"
                ):
                    return render(
                        request,
                        "management/contracts/supportcontract_form.html",
                        {
                            "job_support_data": contract_data,
                            "contract_date": contract_date,
                            "payment_data": default_fee,
                        },
                    )
                if (
                    request.POST.get("category") == "3"
                    and request.POST.get("sub_category") == "2"
                ):
                    return render(
                        request,
                        "management/contracts/trainingcontract_form.html",
                        {
                            "contract_data": contract_data,
                            "contract_date": contract_date,
                            "payment_data": default_fee,
                        },
                    )
                if (request.POST.get("category") == "4"):
                    context={
                                    'job_support_data': contract_data,
                                    'student_data': contract_data,
                                    'contract_date':contract_date,
                                    'payments':default_fee
                                }
                    return render(request, 'management/contracts/dyc_contracts/student_contract.html',context)
            else:
                form = UserForm(request.POST, request.FILES)
                if form.is_valid():
                    print("category", form.cleaned_data.get("category"))

            if form.is_valid():
                # print("category", form.cleaned_data.get("category"))
                if form.cleaned_data.get("category") == 2:
                    form.instance.is_staff = True
                elif form.cleaned_data.get("category") == 3:
                    form.instance.is_client = True
                else:
                    form.instance.is_applicant = True

                form.save()
                # messages.success(request, f'Account created for {username}!')
                return redirect('accounts:account-login')
    else:
        msg = "error validating form"
        form = UserForm()
        print(msg)
    return render(request, "accounts/registration/coda/join.html", {"form": form})

# ---------------ACCOUNTS VIEWS----------------------
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
            # email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            account = authenticate(username=username, password=password)
            CreateProfile()
            # If Category is Staff/employee
            if account is not None and account.category == 2:
                if account.is_staff and not account.is_employee_contract_signed:
                    login(request, account)
                    return redirect("management:employee_contract")

                if account.sub_category == 2:  # contractual
                    login(request, account)
                    return redirect("management:requirements-active")
                else:  # parttime (agents) & Fulltime
                    login(request, account)
                    # return redirect("management:user_task", username=request.user)
                    return redirect("management:companyagenda")

            # If Category is client/customer
            elif account is not None and account.category == 3:
                if account.sub_category == 1:  # Job Support
                    login(request, account)
                    # return redirect("accounts:user-list", username=request.user)
                    return redirect('management:companyagenda')
                else:  # Student
                    login(request, account)
                    return redirect('management:companyagenda')

            elif account is not None and account.category == 4:
                    login(request, account)
                    return redirect("management:dckdashboard")
           
            # If Category is applicant
            elif account is not None and account.profile.section is not None:
                if account.profile.section == "A":
                    login(request, account)
                    return redirect("application:section_a")
                elif account.profile.section == "B":
                    login(request, account)
                    return redirect("application:section_b")
                elif account.profile.section == "C":
                    login(request, account)
                    return redirect("application:policies")
                else:
                    login(request, account)
                    return redirect("application:interview")
            elif account is not None and account.category == 1:
                if account.country in ("KE", "UG", "RW", "TZ"):  # Male
                    if account.gender == 1:
                        login(request, account)
                        return redirect("application:interview")
                    if account.account_profile.section == "A":
                        login(request, account)
                        return redirect("application:sectionA")
                    elif account.account_profile.section == "B":
                        login(request, account)
                        return redirect("application:sectionB")
                    elif account.account_profile.section == "C":
                        login(request, account)
                        return redirect("application:policies")
                    else:
                        login(request, account)
                        return redirect("application:interview")
                else:
                    login(request, account)
                    return redirect("application:interview")

            elif account is not None and account.is_admin:
                login(request, account)
                # return redirect("main:layout")
                return redirect("management:agenda")
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
def users(request):
    users = User.objects.filter(is_active=True).order_by("-date_joined")
    queryset = User.objects.filter(is_active=True).order_by("-date_joined")
    userfilters=UserFilter(request.GET,queryset=users)

    # Use the Paginator to paginate the queryset
    paginator = Paginator(userfilters.qs, 10) # Show 10 objects per page
    page = request.GET.get('page')
    objects = paginator.get_page(page)

    context={
        # "users": queryset,
        "userfilters": userfilters,
        "objects":objects
    }

    if request.user.is_superuser:
        return render(request, "accounts/admin/superpage.html", context)

    # if request.user.is_admin:
    #     return render(request, "accounts/admin/adminpage.html", {"users": users})
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
        "category",
        "sub_category",
        "first_name",
        "last_name",
        "date_joined",
        "email",
        "gender",
        "phone",
        "address",
        "city",
        "state",
        "country",
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
