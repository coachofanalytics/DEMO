import math
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from .forms import UserForm, LoginForm,LoginHistoryForm,CredentialCategoryForm, CredentialForm
from coda_project import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, F, ExpressionWrapper, fields,Q
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth import get_user_model
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.urls import reverse
from .models import CustomerUser, LoginHistory,Tracker, CredentialCategory, Credential, Department
from .utils import (agreement_data,employees,compute_default_fee,
                    get_clients_time,generate_random_password,JOB_SUPPORT_CATEGORIES)
from main.filters import UserFilter

from finance.models import Payment_History,Payment_Information
from mail.custom_email import send_email
import string, random

from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import CustomerUser
from .forms import UserForm
from accounts.choices import CategoryChoices
from django.utils.http import urlsafe_base64_decode
import datetime
from django.contrib.auth import get_user_model
                             
# from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
# from allauth.core.exceptions import ImmediateHttpResponse
from django.http import HttpResponseRedirect
from django.utils import timezone
from accounts.choices import CategoryChoices
from django.contrib.auth import login
from django.utils.encoding import force_text


# Create your views here..

# @allowed_users(allowed_roles=['admin'])
def home(request):
    return render(request, "main/home_templates/newlayout.html")

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

# @allowed_users(allowed_roles=['admin'])
def thank(request):
    return render(request, "accounts/clients/thank.html")


# ---------------ACCOUNTS VIEWS----------------------


def join(request):
    form = UserForm()  # Initialize form
    if request.method == "POST":
        previous_user = CustomerUser.objects.filter(email=request.POST.get("email"))
        if previous_user.exists():
            messages.success(request, 'User already exists with this email')
            return redirect("/password-reset")
        else:
            form = UserForm(request.POST)
            if form.is_valid():
                if form.cleaned_data.get('category') in [CategoryChoices.Jobsupport, CategoryChoices.Bussines_Training, CategoryChoices.investor, CategoryChoices.General_User]:
                    random_password = generate_random_password(8)
                    form.instance.username = form.cleaned_data.get('email')
                    form.instance.set_password(random_password)  # Set password securely
                    form.instance.is_active = False  # User is inactive until email verification
                    form.save()

                    # Send verification email
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your account.'
                    
                    # Encode user ID and token
                    uid = urlsafe_base64_encode(force_bytes(form.instance.pk))
                    token = default_token_generator.make_token(form.instance)
                    # Reverse URL to activation view
                    activation_link = reverse('accounts:activate', kwargs={'uidb64': uid, 'token': token})

                    # Construct full URL
                    activation_url = f"http://{current_site.domain}{activation_link}"

                    # Render email template with context
                    message = render_to_string('email/activation_email.html', {
                        'user': form.instance,
                        'domain': current_site.domain,
                        'uid': uid,
                        'token': token,
                        'activation_url': activation_url,
                    })

                    # Send email
                    send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [form.instance.email])

                    messages.success(request, 'Please confirm your email address to complete the registration.')
                    return redirect('accounts:account-login')
            else:
                messages.error(request, 'Error validating form')
    
    return render(request, "accounts/registration/Biashara/join.html", {"form": form})
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    
    #when error occur while login/signup with social account, we are redirecting it to login page of website
    if request.method == 'GET':
        sociallogin = request.session.pop("socialaccount_sociallogin", None)
        
        if sociallogin is not None:
            msg = 'Error with social login. check your credential or try to sing up manually.'
    
    if request.method == "POST":
        if form.is_valid():
            request.session["siteurl"] = settings.SITEURL
            username_or_email = form.cleaned_data.get("enter_your_username_or_email")
            enter_your_password = form.cleaned_data.get("enter_your_password")
            account = authenticate(username=username_or_email, password=enter_your_password)
            if account is None:
                account = authenticate(email=username_or_email, password=enter_your_password)
            
            
            # If Category is Staff/employee
            if account is not None and account.category == CategoryChoices.Bussines_Training:
               
                login(request, account)
                return redirect("main:import")

            # If Category is client/customer:# Student # Job Support
            elif account is not None and (account.category == CategoryChoices.Jobsupport or account.category == CategoryChoices.Student) :
                login(request, account)
                # if Payment_History.objects.filter(customer=account).exists():
                return redirect('/')
            
            elif account is not None and (account.category == CategoryChoices.investor) :
                login(request, account)
                print("category,subcat",account.category,account.sub_category)
                # url = reverse('management:meetings', kwargs={'status': 'company'})
                return redirect('management:companyagenda')
        
            elif account is not None and account.profile.section is not None and account.category == CategoryChoices.Job_Applicant:
              
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

            elif account is not None and account.profile.section is not None and account.category == CategoryChoices.Job_Applicant and account.sub_category==0:
                login(request, account)
                # print("account.category",account.sub_category)
                return redirect("application:policies")
            
            elif account is not None and account.category == CategoryChoices.General_User:
                login(request, account)
                return redirect("main:layout")

            elif account is not None and account.is_admin:
                login(request, account)
                # return redirect("main:layout")
                return redirect("management:companyagenda")
            else:
                # messages.success(request, f"Invalid credentials.Kindly Try again!!")
                msg=f"Invalid credentials.Kindly Try again!!"
                return render(
                        request, "accounts/registration/Biashara/login_page.html", {"form": form, "msg": msg}
                    )
    return render(
        request, "accounts/registration/Biashara/login_page.html", {"form": form, "msg": msg}
    )
def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('accounts:account-login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('accounts:account-login')
# ================================USERS SECTION================================
def users(request):
    # Filter active staff users and order by date joined
    active_users = CustomerUser.objects.filter(is_active=True).order_by("-date_joined")
    active_staff_users = CustomerUser.objects.filter(is_active=True, is_staff=True).order_by("-date_joined")

    total_users = CustomerUser.objects.all().order_by("-date_joined").count()
    total_active_users = CustomerUser.objects.filter(is_active=True).order_by("-date_joined").count()
    
    # Automatically set is_active to False for staff users who haven't logged in for more than 3 months
    three_months_ago = timezone.now() - timezone.timedelta(days=90)
    inactive_staff_users = active_staff_users.filter(last_login__lt=three_months_ago)
    inactive_staff_users.update(is_active=False)
    
    # Apply filters
    userfilters = UserFilter(request.GET, queryset=active_users)
    
    # Use the Paginator to paginate the queryset
    paginator = Paginator(userfilters.qs, 10)  # Show 10 objects per page
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    
    context = {
        "userfilters": userfilters,
        "objects": objects,
        "total_users": total_users,
        "total_active_users": total_active_users,
    }
    
    if request.user.is_superuser:
        return render(request, "accounts/admin/users.html", context)
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
        "zipcode",
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
        if self.request.user.is_superuser or self.request.user.is_admin :
            return super().form_valid(form)
        #  elif self.request.user.is_authenticated:
        #      return super().form_valid(form)
        return False

    def test_func(self):
        user = self.get_object()
        # if self.request.user == client.username:
        #     return True
        if self.request.user.is_superuser or self.request.user.is_admin :  # or self.request.user == user.username:
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

@login_required
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

@login_required
def credential_view(request):
    if not request.user.is_superuser and not request.user.is_admin and not request.user.is_staff:
        message = 'You are not allowed to access this page. Contact admin: info@codanalytics.net'
        return render(request, "main/errors/generalerrors.html", {"message": message})
    else:
        message = 'Please Contact Admin, if you fail to find access'
        categories = CredentialCategory.objects.all().order_by("-entry_date")
        departments = Department.objects.all()  # Fixed: get all departments
        
        if request.user.is_superuser:
            credentials = Credential.objects.all().order_by("-entry_date")
        elif request.user.is_admin:
            credentials = Credential.objects.filter(Q(user_types='Admin') | Q(user_types='Employee')).order_by("-entry_date")
        elif request.user.is_staff:
            credentials = Credential.objects.filter(user_types='Employee').order_by("-entry_date")
        else:
            credentials = Credential.objects.none()
        
        credential_filters = CredentialFilter(request.GET, queryset=credentials)

        # Step 1: Create a list of credentials
        credentials_list = list(credentials)

        # Step 2: Determine specific records to be moved to the center
        specific_records = ['boa', 'experian', 'betterment', 'robin', 'citi']  # Replace with the actual specific records you want to move

        # Step 3: Remove specific records from the credentials list
        for record in specific_records:
            if record in credentials_list:
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
            "message": message,
        }

        try:
            request.session["siteurl"] = settings.SITEURL
            otp = request.POST.get("otp")
            if otp == request.session.get("security_otp"):
                del request.session["security_otp"]
                context["show_password"] = True
                return render(request, "accounts/admin/credentials.html", context)
            else:
                error_context = {"message": "Invalid OTP"}
                return render(request, "accounts/admin/email_verification.html", error_context)

        except Exception as e:
            print(f"Error: {e}")
            return render(request, "accounts/admin/credentials.html", context)
@login_required
def security_verification(request):
    subject = "One time verification code to view passwords"
    otp = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    request.session["security_otp"] = otp
    request.session["siteurl"] = settings.SITEURL
    
    # Pass the OTP directly to the template
    context = {'otp': otp, 'subject': subject}
    return render(request, "accounts/admin/email_verification.html", context)

# @login_required
# def security_verification(request):
#     subject = "One time verification code to view passwords"
#     # to = request.user.email
#     otp = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
#     request.session["security_otp"] = otp
#     request.session["siteurl"] = settings.SITEURL
#     try:
#         send_email( 
#                 category=request.user.category,
#                 to_email=[request.user.email,],
#                 subject=subject, 
#                 html_template='email/security_verification.html',
#                 context={'otp': otp})
#     except Exception as e:
#         # Handle any other exceptions
#         print(f"An unexpected error occurred: {e}") 

#     return render(request, "accounts/admin/email_verification.html")


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
        "active_employees":active_employees
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


# @login_required(login_url="accounts:account-login")
# def profile(request):
#     return render(request, "accounts/profile.html")

@login_required
def user_login_history(request,username="eunice"):
    login_history = LoginHistory.objects.filter(user__username=username).order_by('-login_time')
    for entry in login_history:
        print(entry.id)
    # user = request.user
    # login_dates = user.get_login_days()
    # login_count = user.get_login_count()
    # has_logged_in_last_7_days = user.has_logged_in_last_days(7)

    context = {
        # 'login_dates': login_dates,
        # 'login_count': login_count,
        # 'has_logged_in_last_7_days': has_logged_in_last_7_days,
        'login_history': login_history
    }

    return render(request, 'accounts/login_history.html', context)
@login_required
def edit_login_logout_time(request, pk):
    login_history = get_object_or_404(LoginHistory, pk=pk)
    username=login_history.user.username
    print(username)
    if request.method == 'POST':
        form = LoginHistoryForm(request.POST, instance=login_history)
        if form.is_valid():
            form.save()
            return redirect('accounts:account-profile', username=username)
    else:
        form = LoginHistoryForm(instance=login_history)
    return render(request, 'main/snippets_templates/generalform.html', {'form': form})

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
            try:
                send_email( category=request.user.category,
                to_email=customer_get[1], #[request.user.email,],
                subject=subject, 
                html_template='email/usertracker.html',
                context={'user': request.user})
            except Exception as e:
                # Handle any other exceptions
                print(f"An unexpected error occurred: {e}") 

        context = {
            "trackers": trackers,
            "num": num,
            "plantime": plantime,
            "Usedtime": Usedtime,
            "delta": delta,
        }
        
        return render(request, "accounts/usertracker.html", context)

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


def custom_social_login(request):   

    try:
        category = request.GET.get('category')
        subcategory = request.GET.get('subcategory')

        if category is not None and subcategory is not None:
            request.session['category'] = request.GET.get('category')
            request.session['subcategory'] = request.GET.get('subcategory')

        # Redirect to the built-in Google login view with the state parameter
        social_login_url = reverse('google_login')  # Use the name of the built-in Google login view
        
        if request.GET.get('socialPlatform'):
       
            social_login_url = reverse(request.GET.get('socialPlatform'))  # Use the name of the built-in Google login view

        return redirect(social_login_url)
    
    except:
    
        return render(request, "accounts/registration/join.html", {"form": UserForm()})