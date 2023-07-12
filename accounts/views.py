import math
from datetime import date, timedelta
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.db.models.aggregates import Avg, Sum
from .forms import UserForm, LoginForm, CredentialCategoryForm, CredentialForm
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
from .models import CustomerUser, Tracker, CredentialCategory, Credential, Department
from .utils import agreement_data,employees,compute_default_fee,get_clients_time
from main.filters import CredentialFilter,UserFilter
from management.models import Task
from application.models import UserProfile,Assets
from finance.models import Default_Payment_Fees,Payment_History,Payment_Information
from finance.utils import DYCDefaultPayments
from mail.custom_email import send_email
import string, random
# Create your views here..

# @allowed_users(allowed_roles=['admin'])
def home(request):
    return render(request, "main/home_templates/layout.html")


# @allowed_users(allowed_roles=['admin'])
def thank(request):
    return render(request, "accounts/clients/thank.html")


# ---------------ACCOUNTS VIEWS----------------------

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
                if form.cleaned_data.get("category") == 2:
                    form.instance.is_staff = True
                elif form.cleaned_data.get("category") == 3 or form.cleaned_data.get("category") == 4:
                    form.instance.is_client = True
                else:
                    form.instance.is_applicant = True

                form.save()
                return redirect('accounts:account-login')
    else:
        msg = "error validating form"
        print(msg)
    
    return render(request, "accounts/registration/coda/join.html", {"form": form})


# def join(request):
#     if request.method == "POST":
#         previous_user = CustomerUser.objects.filter(email = request.POST.get("email"))
#         if len(previous_user) > 0:
#             messages.success(request, f'User already exist with this email')
#             form = UserForm()
#             return redirect("/password-reset")
#         else:
#             contract_data,contract_date=agreement_data(request)
#             dyc_total_amount,dyc_down_payment,early_registration_bonus=DYCDefaultPayments()
#             if request.POST.get("category") == "3":
#                 check_default_fee = Default_Payment_Fees.objects.all()
#                 if check_default_fee:
#                     # default_fee = Default_Payment_Fees.objects.get(id=1)
#                     default_fee = Default_Payment_Fees.objects.all().first()
#                 else:
#                     default_payment_fees = Default_Payment_Fees(
#                         job_down_payment_per_month=1000,
#                         job_plan_hours_per_month=40,
#                         student_down_payment_per_month=500,
#                         student_bonus_payment_per_month=100,
#                     )
#                     default_payment_fees.save()
#                     # default_fee = Default_Payment_Fees.objects.get(id=1)
#                     default_fee = Default_Payment_Fees.objects.all().first()
#                 if (
#                     request.POST.get("category") == "3"
#                     and request.POST.get("sub_category") == "1"
#                 ):
#                     return render(
#                         request,
#                         "management/contracts/supportcontract_form.html",
#                         {
#                             "job_support_data": contract_data,
#                             "contract_date": contract_date,
#                             "payment_data": default_fee,
#                         },
#                     )
#                 if (
#                     request.POST.get("category") == "3"
#                     and request.POST.get("sub_category") == "2"
#                 ):
#                     return render(
#                         request,
#                         "management/contracts/trainingcontract_form.html",
#                         {
#                             "contract_data": contract_data,
#                             "contract_date": contract_date,
#                             "payment_data": default_fee,
#                         },
#                     )
#                 if (request.POST.get("category") == "4"):
#                     context={
#                                     'job_support_data': contract_data,
#                                     'student_data': contract_data,
#                                     'contract_date':contract_date,
#                                     'payments':default_fee
#                                 }
#                     return render(request, 'management/contracts/dyc_contracts/student_contract.html',context)
#                     # return render(
#                     #     request,
#                     #     "management/contracts/dyc_contracts/student_contract.html",
#                     #     {
#                     #         "contract_data": contract_data,
#                     #         "contract_date": contract_date,
#                     #         "dyc_total_amount": dyc_total_amount,
#                     #         "contract_date": dyc_down_payment,
#                     #         "early_registration_bonus": early_registration_bonus,
#                     #         "default_fee": default_fee,
#                     #     },
#                     # )
#             else:
#                 form = UserForm(request.POST, request.FILES)
#                 if form.is_valid():
#                     print("category", form.cleaned_data.get("category"))

#             if form.is_valid():
#                 if form.cleaned_data.get("category") == 2:
#                     form.instance.is_staff = True
#                 elif form.cleaned_data.get("category") == 3:
#                     form.instance.is_client = True
#                 else:
#                     form.instance.is_applicant = True

#                 form.save()
#                 # messages.success(request, f'Account created for {username}!')
#                 return redirect('accounts:account-login')
#     else:
#         msg = "error validating form"
#         form = UserForm()
#         print(msg)
#     return render(request, "accounts/registration/coda/join.html", {"form": form})


# ---------------ACCOUNTS VIEWS----------------------
def create_profile():
    users = CustomerUser.objects.filter(profile=None)
    assets = Assets.objects.all()
    # print(assets)
    if not assets:
        Assets.objects.create(
            name='default',
            category='default',
            description='default',
            image_url='default',
        )
    for user in users:
        UserProfile.objects.create(user=user)



def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            request.session["siteurl"] = settings.SITEURL
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            account = authenticate(username=username, password=password)
            create_profile()
            
            # If Category is Staff/employee
            if account is not None and account.category == 2:
                if account.is_staff and not account.is_employee_contract_signed:
                    login(request, account)
                    return redirect("management:employee_contract")
                
                if account.is_staff and account.is_employee_contract_signed:
                    login(request, account)
                    return redirect("management:companyagenda")

                # if account.sub_category == 2 or account.sub_category == 3:  # contractual
                #     login(request, account)
                #     return redirect("management:requirements-active")
                
                else:  # parttime (agents) & Fulltime
                    login(request, account)
                    return redirect("management:requirements-active")

            # If Category is client/customer:# Student # Job Support
            elif account is not None and (account.category == 3 or account.category == 4) :
                login(request, account)
                return redirect('management:companyagenda')
           
            # If Category is applicant
            # elif account is not None and account.profile.section is not None:
            #     if account.profile.section == "A":
            #         login(request, account)
            #         return redirect("application:section_a")
            #     elif account.profile.section == "B":
            #         login(request, account)
            #         return redirect("application:section_b")
            #     elif account.profile.section == "C":
            #         login(request, account)
            #         return redirect("application:policies")
            #     else:
            #         login(request, account)
            #         return redirect("application:interview")
            elif account is not None and account.profile.section is not None and account.category == 1:
                # if account.country in ("KE", "UG", "RW", "TZ"):  # Male
                # if account.gender == 1:
                #     login(request, account)
                #     return redirect("application:interview")
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

            elif account is not None and account.is_admin:
                login(request, account)
                # return redirect("main:layout")
                return redirect("management:companyagenda")
            else:
                # messages.success(request, f"Invalid credentials.Kindly Try again!!")
                msg=f"Invalid credentials.Kindly Try again!!"
                return render(
                        request, "accounts/registration/login_page.html", {"form": form, "msg": msg}
                    )
    return render(
        request, "accounts/registration/login_page.html", {"form": form, "msg": msg}
    )


# ================================USERS SECTION================================
def users(request):
    users = CustomerUser.objects.filter(is_active=True).order_by("-date_joined")
    queryset = CustomerUser.objects.filter(is_active=True).order_by("-date_joined")
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
    model = CustomerUser
    success_url = "/accounts/users"
    # fields=['category','address','city','state','country']
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
    model = CustomerUser
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
    #model=CustomerUser
    from_class=PasswordChangeForm
    template_name='accounts/registration/password_change_form.html'
    success_url=reverse_lazy('accounts:account-login')

class PasswordsSetView(PasswordChangeView):
    #model=CustomerUser
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


def newcredentialCategory(request):
    if request.method == "POST":
        form = CredentialCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("accounts:account-crendentials")
    else:
        form = CredentialCategoryForm()
    return render(
        request, "accounts/admin/forms/credentialCategory_form.html", {"form": form}
    )


def newcredential(request):
    if request.method == "POST":
        form = CredentialForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            instance=form.save(commit=False)
            instance.added_by=request.user
            instance.save()
            return redirect("accounts:account-crendentials")
    else:
        form = CredentialForm()
    return render(request, "accounts/admin/forms/credential_form.html", {"form": form})


# def credential_view(request):
#     categories = CredentialCategory.objects.all().order_by("-entry_date")
#     credentials = Credential.objects.all().order_by("-entry_date")
#     departments = Department(request)
#     credential_filters=CredentialFilter(request.GET,queryset=credentials)
#     context = {
#         "departments": departments,
#         "categories": categories,
#         "credentials": credentials,
#         "show_password": False,
#         "credential_filters": credential_filters,
#     }
#     try:
#         request.session["siteurl"] = settings.SITEURL
#         otp = request.POST["otp"]
#         if otp == request.session["security_otp"]:
#             del request.session["security_otp"]
#             context["show_password"] = True
#             return render(request, "accounts/admin/credentials.html", context)
#         else:
#             error_context = {"message": "Invalid OTP"}
#             return render(
#                 request, "accounts/admin/email_verification.html", error_context
#             )

#     except:
#         return render(request, "accounts/admin/credentials.html", context)


def credential_view(request):
    categories = CredentialCategory.objects.all().order_by("-entry_date")
    credentials = Credential.objects.all().order_by("-entry_date")
    departments = Department(request)
    credential_filters = CredentialFilter(request.GET, queryset=credentials)

    # Step 1: Create a list of credentials
    credentials_list = list(credentials)
    # for record in credentials_list:
        # print("credentials_list====>",record)

    # Step 2: Determine specific records to be moved to the center
    specific_records = ['boa','experian','betterment','robin','citi']  # Replace with the actual specific records you want to move
    # specific_records = ['68','75','85','89','91', '93']  # Replace with the actual specific records you want to move

    # Step 3: Remove specific records from the credentials list
    for record in specific_records:
        if record in credentials_list:
            print("specific_records====>",record)
            credentials_list.remove(record)

    # Step 4: Sort the credentials list
    credentials_list.sort(key=lambda cred: cred.entry_date, reverse=True)

    # Step 5: Calculate the index for inserting the specific records
    center_index = math.ceil(len(credentials_list) / 2)

    # Step 6: Insert the specific records at the center index
    for record in specific_records:
        credentials_list.insert(center_index, record)

    context = {
        "departments": departments,
        "categories": categories,
        "credentials": credentials_list,
        "show_password": False,
        "credential_filters": credential_filters,
    }

    try:
        request.session["siteurl"] = settings.SITEURL
        otp = request.POST["otp"]
        if otp == request.session["security_otp"]:
            del request.session["security_otp"]
            context["show_password"] = True
            return render(request, "accounts/admin/credentials.html", context)
        else:
            error_context = {"message": "Invalid OTP"}
            return render(
                request, "accounts/admin/email_verification.html", error_context
            )

    except:
        return render(request, "accounts/admin/credentials.html", context)



def security_verification(request):
    subject = "One time verification code to view passwords"
    # to = request.user.email
    otp = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    request.session["security_otp"] = otp
    request.session["siteurl"] = settings.SITEURL
    # html_content = "Your One time verification code is " + otp
    # print(to, otp)
    # email_template(subject, to, html_content)
    print(request.user.category)
    send_email( category=request.user.category,
                to_email=[request.user.email,],
                subject=subject, 
                html_template='email/security_verification.html',
                context={'otp': otp})
    return render(request, "accounts/admin/email_verification.html")


@method_decorator(login_required, name="dispatch")
class CredentialUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Credential
    success_url = "/accounts/credentials"
    fields = ['category','name', 'added_by','slug',
                'user_types','description','password',
                'link_name','link','is_active','is_featured']

    def form_valid(self, form):
        # if form.instance.added_by==self.request.user:
        if (
            self.request.user.is_superuser
            or self.request.user.is_admin
        ):
            return super().form_valid(form)
        else:
            return False

    def test_func(self):
        credential = self.get_object()
        # if self.request.user ==credential.added_by:
        if (
            self.request.user.is_superuser
            or self.request.user.is_admin
        ):
            return True
        else:
            return False


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
    clients = {
        'students': CustomerUser.objects.filter(Q(category=4), Q(is_client=True), Q(is_active=True)).order_by('-date_joined'),
        'jobsupport': CustomerUser.objects.filter(Q(category=3), Q(is_client=True), Q(is_active=True)).order_by('-date_joined'),
        'interview': CustomerUser.objects.filter(Q(category=4),  Q(is_client=True), Q(is_active=True)).order_by('-date_joined'),
        # 'dck_users': CustomerUser.objects.filter(Q(category=4), Q(sub_category=6), Q(is_applicant=True), Q(is_active=True)).order_by('-date_joined'),
        # 'dyc_users': CustomerUser.objects.filter(Q(category=4), Q(sub_category=7), Q(is_applicant=True), Q(is_active=True)).order_by('-date_joined'),
        'past': CustomerUser.objects.filter(Q(is_client=True), Q(is_active=False)).order_by('-date_joined'),
    }
    template_name = "accounts/clients/clientlist.html"
    
    # if request.user.is_superuser or request.user.is_staff or request.user.sub_category == 6:
    #     template_name = "accounts/clients/dcklist.html"

    # # if  request.user.is_superuser or request.user.is_staff or request.user.sub_category == 7:
    # if  request.user.is_superuser or request.user.is_staff:
    #     template_name = "accounts/clients/dyclist.html"

    return render(request, template_name, clients)


@method_decorator(login_required, name="dispatch")
class ClientDetailView(DetailView):
    template_name = "accounts/clients/client_detail.html"
    model = CustomerUser
    ordering = ["-date_joined "]

@method_decorator(login_required, name="dispatch")
class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomerUser
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
    model = CustomerUser
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


# ----------------------TIME TRACKING CLASS-BASED VIEWS--------------------------------
@method_decorator(login_required, name="dispatch")
class TrackDetailView(DetailView):
    model = Tracker
    ordering = ["-login_date"]


@method_decorator(login_required, name="dispatch")
class TrackListView(ListView):
    model = Tracker
    template_name = "accounts/tracker.html"
    context_object_name = "trackers"
    ordering = ["-login_date"]

def usertracker(request, user=None, *args, **kwargs):
        user = get_object_or_404(CustomerUser, username=kwargs.get("username"))
        trackers = Tracker.objects.all().filter(author=user).order_by("-login_date")
        try:
            em = Tracker.objects.all().values().order_by("-pk")[0]
        except:
            return redirect("accounts:tracker-create")
        customer_get = CustomerUser.objects.values_list("username", "email").get(id=em.get("author_id"))
        try:
            history_info = Payment_History.objects.filter(customer_id=user.id).order_by('-contract_submitted_date')[1]
        except IndexError:
            # Handle the case when there is no previous payment record
            history_info = None  # Or assign a default value
        current_info = Payment_Information.objects.filter(customer_id=user.id).first()
        plantime,history_time,added_time,Usedtime,delta,num=get_clients_time(current_info,history_info,trackers)
        if delta < 30:
            subject = "New Contract Alert!"
            send_email( category=request.user.category,
            to_email=customer_get[1], #[request.user.email,],
            subject=subject, 
            html_template='email/usertracker.html',
            context={'user': request.user})
            # to = customer_get[1]
            # html_content = f"""
            #     <span><h3>Hi {customer_get[0]},</h3>Your Total Time at CODA is less than 30 hours kindly click here to sign a new contract <br>
            #     <a href='https://www.codanalytics.net/finance/new_contract/{request.user}/'>click here to sign new contract</a><br>
                
            #     </span>"""
            # email_template(subject, to, html_content)

        context = {
            "trackers": trackers,
            "num": num,
            "plantime": plantime,
            "Usedtime": Usedtime,
            "delta": delta,
        }
        return render(request, "accounts/usertracker.html", context)
    # except:
    #     # return render(request, "accounts/usertracker.html", context)
    #     return redirect("accounts:tracker-create")


# def usertracker(request, user=None, *args, **kwargs):
#     # try:
#         user = get_object_or_404(CustomerUser, username=kwargs.get("username"))
#         trackers = Tracker.objects.all().filter(author=user).order_by("-login_date")
#         try:
#             em = Tracker.objects.all().values().order_by("-pk")[0]
#         except:
#             return redirect("accounts:tracker-create")
#         num = trackers.count()
#         # Check on my_time=avg("time")
#         my_time = trackers.aggregate(Assigned_Time=Avg("time"))
#         Used = trackers.aggregate(Used_Time=Sum("duration"))
#         Usedtime = Used.get("Used_Time")
#         # plantime = my_time.get("Assigned_Time")
#         payment_details = Payment_History.objects.filter(customer=user)
#         contract_plan_hours = payment_details.aggregate(Sum("plan"))
#         assigned_hours = 0
#         if contract_plan_hours.get("plan__sum"):
#             assigned_hours = contract_plan_hours.get("plan__sum") * 40
#         if my_time.get("Assigned_Time"):
#             plantime = my_time.get("Assigned_Time") + assigned_hours
#         plantime = assigned_hours
#         try:
#             delta = round(plantime - Usedtime)
#         except (TypeError, AttributeError):
#             delta = 0
#         customer_get = CustomerUser.objects.values_list("username", "email").get(
#             id=em.get("author_id")
#         )
#         if delta < 30:
#             subject = "New Contract Alert!"
#             send_email( category=request.user.category,
#             to_email=customer_get[1], #[request.user.email,],
#             subject=subject, 
#             html_template='email/usertracker.html',
#             context={'user': request.user})
#             # to = customer_get[1]
#             # html_content = f"""
#             #     <span><h3>Hi {customer_get[0]},</h3>Your Total Time at CODA is less than 30 hours kindly click here to sign a new contract <br>
#             #     <a href='https://www.codanalytics.net/finance/new_contract/{request.user}/'>click here to sign new contract</a><br>
                
#             #     </span>"""
#             # email_template(subject, to, html_content)

#         context = {
#             "trackers": trackers,
#             "num": num,
#             "plantime": plantime,
#             "Usedtime": Usedtime,
#             "delta": delta,
#         }
#         return render(request, "accounts/usertracker.html", context)
#     # except:
#     #     # return render(request, "accounts/usertracker.html", context)
#     #     return redirect("accounts:tracker-create")

class TrackCreateView(LoginRequiredMixin, CreateView):
    model = Tracker
    success_url = "/accounts/tracker"
    # success_url="usertime"
    # fields=['category','task','duration']
    fields = [
        "empname",
        "employee",
        "author",
        "category",
        "sub_category",
        "task",
        "duration",
        "plan",
    ]

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = self.request.user
        try:

            if form.instance.category == "Job_Support":
                print(form.instance.empname)
                idval, points, targetpoints = Task.objects.values_list(
                    "id", "point", "mxpoint"
                ).filter(
                    Q(activity_name=form.instance.category)
                    | Q(activity_name="job_support")
                    | Q(activity_name="jobsupport")
                    | Q(activity_name="Jobsupport")
                    | Q(activity_name="JobSupport")
                    | Q(activity_name="Job Support")
                    | Q(activity_name="Job support")
                    | Q(activity_name="job support"),
                    employee__username=form.instance.empname,
                )[
                    0
                ]
                # if Development, Testing : 
                # upto maximum 8 hours
                # 0------8 max 
                #
                self.idval = idval
                if (
                    form.instance.sub_category == "Development"  
                    or form.instance.sub_category == "Testing"
                ):
                    points = float(points) + (0.5 * form.instance.duration)
                else:
                    points = float(points) + form.instance.duration

                if points >= targetpoints:
                    targetpoints += 10

                Task.objects.filter(
                    Q(activity_name=form.instance.category)
                    | Q(activity_name="job_support")
                    | Q(activity_name="jobsupport")
                    | Q(activity_name="Jobsupport")
                    | Q(activity_name="JobSupport")
                    | Q(activity_name="Job Support")
                    | Q(activity_name="Job support")
                    | Q(activity_name="job support"),
                    employee__username=form.instance.empname,
                ).update(point=points, mxpoint=targetpoints)
        except:
            pass

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse(
                        "management:new_evidence", 
                        kwargs={
                            'taskid':  self.idval
                        }
                    )


@method_decorator(login_required, name="dispatch")
class TrackUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tracker
    success_url = "/accounts/tracker"

    fields = [
        "employee",
        "empname",
        "author",
        "plan",
        "category",
        "task",
        "duration",
        "time",
    ]

    def form_valid(self, form):
        # form.instance.author=self.request.user
        if (
            self.request.user.is_superuser
            or self.request.user.is_admin
            or self.request.user.is_staff
        ):
            return super().form_valid(form)
        else:
            return False

    def test_func(self):
        track = self.get_object()
        if (
            self.request.user.is_superuser
            or self.request.user.is_admin
            or self.request.user.is_staff
        ):
            return True
        # elif self.request.user ==track.author:
        #     return True
        else:
            return False


@method_decorator(login_required, name="dispatch")
class TrackDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tracker
    success_url = "/accounts/tracker"

    def test_func(self):
        # timer = self.get_object()
        # if self.request.user == timer.author:
        # if self.request.user.is_superuser:
        if self.request.user.is_superuser:
            return True
        return False