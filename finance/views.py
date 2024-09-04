import base64
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.db.models import Sum
from django.http import QueryDict, Http404,JsonResponse
from .utils import *
from requests import request
from datetime import datetime,date

import requests

from django.conf import settings
from decimal import *
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView,
)
import json
from accounts.forms import UserForm
from accounts.models import *
from .models import (
        Budget, CodaBudget, Payment_Information,Payment_History,
        Default_Payment_Fees,
    Transaction
        )
from .forms import BudgetForm, DepartmentFilterForm, InflowForm
from coda_project.settings import SITEURL,payment_details
from main.utils import image_view,download_image,path_values
from .utils import check_default_fee,get_exchange_rate,compute_amt,category_subcategory
from main.utils import countdown_in_month



User = get_user_model()

# payment details
phone_number,email_info,cashapp,venmo,account_no=payment_details(request)


#Time details
(remaining_days, remaining_seconds, remaining_minutes, remaining_hours,now) = countdown_in_month()
#Exchange Rate details
usd_to_kes = get_exchange_rate('USD', 'KES')
rate = round(Decimal(usd_to_kes), 2)

def finance_report(request):
    return render(request, "finance/reports/finance.html", {"title": "Finance"})


def contract_form_submission(request):
    try:
        if request.method == "POST":
            user_student_data = request.POST.get('usr_data')
            student_dict_data = QueryDict(user_student_data)
            username = student_dict_data.get('username')
            
            try:
                customer=User.objects.get(username=username)
                # ss= customer.id
                # print("id",ss)
                payment = Payment_Information.objects.filter(
                        customer_id=request.user.id
                    ).first()
                # print("payment=====>",payment)
                # payment = Payment_Information.objects.get(customer_id_id=customer.id)
            except:
                customer = None
                payment = None
            if not payment:
                form=UserForm(student_dict_data)
                if form.cleaned_data.get('category') == 1:
                    form.instance.is_applicant = True
                elif form.cleaned_data.get('category') == 2:
                    form.instance.is_staff = True 
                elif form.cleaned_data.get('category') == 3:
                    form.instance.is_client = True 
                else:
                    form.instance.is_admin = True 
                if form.is_valid():
                    form.save()
            customer=User.objects.get(username=username)
            payment_fees = int(request.POST.get('duration'))*1000
            down_payment = int(request.POST.get('down_payment'))
            student_bonus_amount = request.POST.get('bonus')
            fee_balance = payment_fees - down_payment
            if request.POST.get('student_contract'):
                fee_balance = payment_fees - (down_payment+int(student_bonus_amount))
            plan = request.POST.get('duration')
            payment_method = request.POST.get('payment_type')
            client_signature = request.POST.get('client_sign')
            company_rep = request.POST.get('rep_name')
            client_date = request.POST.get('client_date')
            rep_date = request.POST.get('rep_date')
            if payment:
                payment_data=Payment_Information.objects.filter(customer_id_id=int(customer.id)).update(payment_fees=int(payment_fees),
                    down_payment=down_payment,
                    student_bonus = student_bonus_amount,
                    fee_balance=int(fee_balance),
                    plan=plan,
                    payment_method=payment_method,
                    client_signature=client_signature,
                    company_rep=company_rep,
                    client_date=client_date,
                    rep_date=rep_date)
            else:

                payment_data=Payment_Information(payment_fees=int(payment_fees),
                    down_payment=down_payment,
                    student_bonus = student_bonus_amount,
                    fee_balance=int(fee_balance),
                    plan=plan,
                    payment_method=payment_method,
                    client_signature=client_signature,
                    company_rep=company_rep,
                    client_date=client_date,
                    rep_date=rep_date,
                    customer_id_id=int(customer.id)
                    )
                payment_data.save()
            payment_history_data=Payment_History(payment_fees=int(payment_fees),
                down_payment=down_payment,
                student_bonus = student_bonus_amount,
                fee_balance=int(fee_balance),
                plan=plan,
                payment_method=payment_method,
                client_signature=client_signature,
                company_rep=company_rep,
                client_date=client_date,
                rep_date=rep_date,
                customer_id=int(customer.id)
                )
            payment_history_data.save()
            if payment:
                messages.success(request, f'Added New Contract For the {username}!')
                return redirect('finance:pay')
    except:
        message=f'Hi,{request.user}, there is an issue on our end kindly contact us directly at info@codanalytics.net'
        context={
                  "title": "CONTRACT", 
                  "message": message,
                }
        return render(request, "main/errors/generalerrors.html", context)


def mycontract(request, *args, **kwargs):
    username = kwargs.get('username')
    print(username)
    client_data=User.objects.get(username=username)
    check_default_fee = Default_Payment_Fees.objects.all()
    if check_default_fee:
        default_fee = Default_Payment_Fees.objects.filter().first()
        print(default_fee)
    else:
        default_payment_fees = Default_Payment_Fees(job_down_payment_per_month=500,
                job_plan_hours_per_month=40,
                student_down_payment_per_month=500,
                student_bonus_payment_per_month=100)
        default_payment_fees.save()
        default_fee = Default_Payment_Fees.objects.all().first()
        print(default_fee)
        
    if Payment_Information.objects.filter(customer_id_id=client_data.id).exists():
        # payemnt_details = Payment_Information.objects.get(customer_id_id=client_data.id).first()
        payemnt_details = Payment_Information.objects.get(customer_id_id=client_data.id)
        print("payemnt_details",payemnt_details)
        contract_date = payemnt_details.contract_submitted_date.strftime("%d %B, %Y")
        if client_data.category == 3 and client_data.sub_category == 1:
            plan_dict = {"1":40,"2":80,"3":120}
            selected_plan = plan_dict[str(payemnt_details.plan)]
            job_support_hours = selected_plan - 30
            context={
                    'job_support_data': client_data,
                    'contract_date':contract_date,
                    'payment_data':payemnt_details,
                    "selected_plan":selected_plan,
                    "job_support_hours":job_support_hours
                }
            return render(request, 'management/contracts/my_supportcontract_form.html',context)
        if client_data.category == 3 and client_data.sub_category == 2:
            context={
                'student_data': client_data,
                'contract_date':contract_date,
                'payment_data':payemnt_details
            }
            return render(request, 'management/contracts/my_trainingcontract_form.html',context)
        else:
            raise Http404("Login/Wrong Page: Are You a Client?")
    else:
        context={"title": "CONTRACT", 
                'username':username}
        return render(request, 'management/contracts/contract_error.html',context)





# ==================PAYMENT CONFIGURATIONS VIEWS=======================
# ==================PAYMENTVIEWS=======================
class DefaultPaymentCreateView(LoginRequiredMixin, CreateView):
    model = Default_Payment_Fees
    success_url = "/finance/contract_form"
    fields = [
                "job_down_payment_per_month",
                "job_plan_hours_per_month",
                "student_down_payment_per_month",
                "student_bonus_payment_per_month",
    ]
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
#Adding payments to payment history
class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment_History
    success_url = "/finance/contract_form"
    # fields = "__all__"
    fields = [
                "customer",
                "payment_fees",
                "down_payment",
                # "student_bonus",
                "plan",
                "payment_method",
    ]
    def form_valid(self, form):
        # form.instance.user = self.request.user
        form.instance.client_signature = form.instance.customer
        today=str(now)
        form.instance.client_date = today
        form.instance.rep_date = today
        form.instance.student_bonus = 0
        form.instance.company_rep = 'coda'
        payment_fees = form.instance.payment_fees
        down_payment = form.instance.down_payment
        form.instance.fee_balance=payment_fees-down_payment-form.instance.student_bonus
        return super().form_valid(form)

def payments(request):
    payment_history=Payment_History.objects.all()
    Payment_Info=Payment_Information.objects.all()
    context={
        "title":"Payments",
        "payment_history":payment_history,
        "Payment_Info":Payment_Info
    }
    return render(request,"finance/payments/payments.html",context)


def payment(request,method):
    path_value,sub_title=path_values(request)
    subject='PAYMENT'
    url='finance/payments/payment_method.html'
    
    message=f'Hi,{request.user.first_name}, an email has been sent \
            with {sub_title} details for your payment.In the unlikely event\
            that you have not received it, kindly \
            check your spam folder.'
    error_message=f'Hi,{request.user.first_name}, there seems to be an issue on our end.kindly contact us directly for payment details.'
    context={
                'subtitle': sub_title,
                'user': request.user.first_name,
                'mpesa_number':phone_number,
                'cashapp':cashapp,
                'venmo':venmo,
                'account_no':account_no,
                'email':email_info,
                'message':message,
                'error_message':error_message,
                'contact_message':'info@codanalytics.net',
            }
    try:
        send_email( category=request.user.category,
                    to_email=[request.user.email,],
                    subject=subject, html_template=url,
                    context=context
                    )
        return render(request, "finance/payments/payment_method.html",context)
    except:
        return render(request, "finance/payments/payment_method.html",context)
    

def pay(request, service=None):
    if not request.user.is_authenticated:
        return redirect(reverse('accounts:account-login'))
    payment_info = Payment_Information.objects.filter(customer_id=request.user).last()

 
    context = {
            "title": "PAYMENT",
            "payments": payment_info,
            "rate": rate,
            'user': request.user,
            
            "message": f"Hi {request.user}, you are yet to sign the contract with us. Kindly contact us at info@codanalytics.net.",
            
            # "service": True,
        }
    return render(request, "finance/payments/pay.html", context)

def paymentComplete(request):
    payments = Payment_Information.objects.filter(customer_id=request.user.id).first()
    customer = request.user
    body = json.loads(request.body)
    payment_fees = body["payment_fees"]
    down_payment = payments.down_payment
    studend_bonus = payments.student_bonus
    plan = payments.plan
    fee_balance = payments.fee_balance
    payment_mothod = payments.payment_method
    contract_submitted_date = payments.contract_submitted_date
    client_signature = payments.client_signature
    company_rep = payments.company_rep
    client_date = payments.client_date
    rep_date = payments.rep_date
    Payment_History.objects.create(
        customer=customer,
        payment_fees=payment_fees,
        down_payment=down_payment,
        student_bonus=studend_bonus,
        plan=plan,
        fee_balance=fee_balance,
        payment_method=payment_mothod,
        contract_submitted_date=contract_submitted_date,
        client_signature=client_signature,
        company_rep=company_rep,
        client_date=client_date,
        rep_date=rep_date,
    )
    return JsonResponse("Payment completed!", safe=False)

class DefaultPaymentListView(ListView):
    model = Default_Payment_Fees
    template_name = "finance/payments/defaultpayments.html"
    context_object_name = "defaultpayments"

class DefaultPaymentUpdateView(UpdateView):
    model = Default_Payment_Fees
    success_url = "/finance/payments"
    
    fields = [
                "job_down_payment_per_month",
                "job_plan_hours_per_month",
                "student_down_payment_per_month",
                "student_bonus_payment_per_month",
                "loan_amount",
    ]
    # fields=['user','activity_name','description','point']
    def form_valid(self, form):
        # form.instance.author=self.request.user
        if self.request.user.is_superuser:
            return super().form_valid(form)
        else:
            # return redirect("management:tasks")
            return render(request,"management/contracts/supportcontract_form.html")

    def test_func(self):
        task = self.get_object()
        if self.request.user.is_superuser:
            return True
        # elif self.request.user == task.employee:
        #     return True
        return False



# For payment purposes
class PaymentInformationUpdateView(UpdateView):
    model = Payment_Information
    success_url = "/finance/pay/"
    template_name="main/snippets_templates/generalform.html"
    
    # fields ="__all__"
    fields=['customer_id','down_payment']
    def form_valid(self, form):
        # form.instance.author=self.request.user
        # if self.request.user.is_superuser or self.request.user:
        if self.request.user is not None:
            return super().form_valid(form)
        else:
            # return redirect("management:tasks")
            return render(request,"main/snippets_templates/generalform.html")

    def test_func(self):
        task = self.get_object()
        # if self.request.user.is_superuser:
        #     return True
        # elif self.request.user == task.employee:
        if self.request.user:
            return True


# ----------------------CASH OUTFLOW CLASS-BASED VIEWS--------------------------------
@login_required
def transact(request):
    if request.method == "POST":
        form = InflowForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            instance=form.save(commit=False)
            instance.sender=request.user
            instance.save()
            return redirect("/finance/transaction/")
    else:
        form = InflowForm()
    return render(request, "finance/payments/transact.html", {"form": form})


class TransactionListView(ListView):
    model = Transaction
    template_name = "finance/payments/transactions.html"
    context_object_name = "transactions"
    # ordering=['-transaction_date']


@method_decorator(login_required, name="dispatch")
class TransanctionDetailView(DetailView):
    template_name = "finance/payments/transaction_detail.html"
    model = Transaction
    ordering = ["-transaction_date"]


class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    # success_url="/finance/transaction"
    fields = [
        "sender",
        "receiver",
        "phone",
        "sender_phone",
        "department",
        "category",
        "type",
        "payment_method",
        "qty",
        "amount",
        "transaction_cost",
        "description",
        "receipt_link",
    ]

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("finance:transaction-list")

    def test_func(self):
        inflow = self.get_object()
        if self.request.user == inflow.sender:
            return True
        elif self.request.user.is_admin or self.request.user.is_superuser:
            return True
        return False
@login_required
def add_budget_item(request):
    if request.method == "POST":
        form = BudgetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            instance=form.save(commit=False)
            print(request.user)
            instance.budget_lead=request.user
            instance.save()
            return redirect("finance:budget", company_slug="coda")
    else:
        form = BudgetForm()
    return render(request, "finance/budgets/newbudget.html", {"form": form})

def budget(request, company_slug='coda'):
   
    # Fetch budgets for the company
    company_budgets = Budget.objects.all()
  
    # Calculate total budgets
    total_budget = sum(site.amount for site in company_budgets)
   
    # Construct link URL
    #link_url = reverse('finance:site_budget_with_subcategory', kwargs={'company_slug': company_slug, 'category': 'Web', 'subcategory': 'all'})

    # Prepare summary data
    summary = [
        {"title": "Total Budget", "value": total_budget, "link": ''},
    ]


    context = {
        "budget_obj": company_budgets,
        "data": summary,
       
    }
    return render(request, "finance/budgets/budget.html", context)
def filter_transactions_by_duration_and_department(duration, department_name=None):
    """
    Filters transactions based on the given duration and optionally by department name.
    """
    if duration > 12:
        year = duration - 1
        if department_name:
            return CodaBudget.objects.filter(department__name=department_name, created_at__year=str(year)).order_by('category')
        else:
            return CodaBudget.objects.filter(created_at__year=str(year)).order_by('category')
    else:
        month = duration-1
        year=2024
        if department_name:
            # return CodaBudget.objects.filter(department__name=department_name, created_at__month=str(month)).order_by('category')
            return CodaBudget.objects.filter(department__name=department_name, created_at__year=str(year), created_at__month=str(month)).order_by('category')
        else:
            return CodaBudget.objects.filter( created_at__year=str(year),created_at__month=str(month)).order_by('category')

def budget_projection(request,subtitle='summary',duration=2024):
    path_list, sub_title, pre_sub_title = path_values(request)
    subtitle=path_list[2]
    # departments = Department.objects.all()
    # categories = BudgetCategory.objects.all()

    # Validate and convert duration to an integer
    try:
        duration = int(duration)
    except ValueError:
        raise Http404("Invalid duration value")

    total = 0
    budget_items = []
    
    if request.method == "POST":
        form = DepartmentFilterForm(request.POST)
        if form.is_valid():
            department_name = form.cleaned_data.get('name')
            if department_name:
                budget_items = filter_transactions_by_duration_and_department(duration, department_name)
            else:
                budget_items = filter_transactions_by_duration_and_department(duration)
            total = sum(item.amount * item.qty for item in budget_items)
    else:
        form = DepartmentFilterForm()
        budget_items = filter_transactions_by_duration_and_department(duration)
        total = sum(item.amount * item.qty for item in budget_items)




    # Aggregate data by month and category
    budget_summary = budget_items.values('category__name','subcategory__name').annotate(
        total_qty=Sum('qty'),
        total_amount=Sum('unit_price')

    )
    # Create a list of unique categories
    available_categories = budget_summary.values_list('category__name', flat=True).distinct()

    context = {
        # "departments": departments,
        "categories": available_categories,
        "summary": budget_summary,
        "budget_items": budget_items,
        "budget_months": budget_months,
        "budget_years": budget_years,
        "total_amt_ksh": total,
        "total_amt": total / rate if total else 0,
        
    }
    if subtitle=='detailed':
        return render(request, "finance/budgets/detailed_budget.html", context)
    else:
        return render(request, "finance/budgets/summary_budget.html", context)