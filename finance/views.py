from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.db.models import Sum
from django.http import QueryDict, Http404,JsonResponse
from requests import request
from datetime import datetime,date
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
        Payment_Information,Payment_History,
        Default_Payment_Fees,
        Inflow,Transaction,Outflow
        )
from .forms import InflowForm,OutflowForm
from coda_project.settings import SITEURL,payment_details
from main.utils import image_view,download_image,Meetings,path_values
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


@login_required
def newcontract(request, *args, **kwargs):
    username = kwargs.get('username')
    # get the current logged in user
    user = request.user
    user_categories = UserCategory.objects.filter(user=user)
    category, sub_category = [(cat.category, cat.sub_category) for cat in user_categories][0] if user_categories else (None, None)

    #Gets client/user information from the custom user table
    client_data=User.objects.get(username=username)

    reg_fee = 19.99
    try:
        service = VisaService.objects.get(sub_category=sub_category)
        total_price = service.price + reg_fee
    except VisaService.DoesNotExist:
        service = None
        total_price = reg_fee
    # print(service)

    request.session['total_price'] = total_price
    today = date.today()
    contract_date = today.strftime("%d %B, %Y")
    context={
            'client_data': client_data,
            'contract_date': contract_date,
            'payments': service,
            'reg_fee': reg_fee,
            'total_price': total_price,
            }
    try:
        payment_info = Payment_Information()
        payment_info.payment_fees = total_price
        payment_info.down_payment = total_price
        payment_info.customer_id = request.user
        payment_info.fee_balance = total_price
        payment_info.plan = sub_category
        payment_info.payment_method = ''
        payment_info.client_signature = ''
        payment_info.company_rep = ''
        payment_info.save()
        print(payment_info)
    except:
        print('Problem Found')

    if category == 1 and sub_category == 2 or request.user.is_superuser:
        return render(request, 'main/contracts/client_contract.html',context)
    else:
        return render(request, 'main/contracts/client_contract.html',context)


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
    contract_url = reverse('finance:newcontract', args=[request.user.username])
    payment_info = Payment_Information.objects.filter(customer_id=request.user).last()

    if not payment_info:
        return redirect('finance:newcontract', request.user)
    
    context = {
            "title": "PAYMENT",
            "payments": payment_info,
            "rate": rate,
            "Fee_USD": payment_info.down_payment,
            "Fee_KSH": payment_info.down_payment * rate,
            "message": f"Hi {request.user}, you are yet to sign the contract with us. Kindly contact us at info@codanalytics.net.",
            "link": contract_url,
            "service": True,
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

@method_decorator(login_required, name="dispatch")
class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Transaction
    success_url = "/finance/transaction"

    def test_func(self):
        transaction = self.get_object()
        if self.request.user == transaction.sender:
            return True
        elif self.request.user.is_superuser or self.request.user.is_admin:
            return True
        return False
        
# ----------------------CASH INFLOW CLASS-BASED VIEWS--------------------------------
@login_required
def cashflows(request):
    path_value,sub_title=path_values(request)
    user_categories = UserCategory.objects.filter(user= request.user)
    #categories and subcategories
    (category,sub_category)=category_subcategory(user_categories)
    transactions = Transaction.objects.filter(clients_category="DYC")
    outflows=Outflow.objects.all()
    total_outflows = sum(transact.total_payment for transact in outflows)
   
    (total_price,total_amt,balance,receipt_url)=compute_amt(VisaService,transactions,rate,user_categories)
    total_members = transactions.filter(clients_category="DYC").count()
    paid_members = transactions.filter(clients_category="DYC", has_paid=True).count()
    # print(total_price,total_amt,balance)
    balance_amount=total_amt-total_outflows

    inflow_context = {
        "transactions": transactions,
        "total_count": total_members,
        "paid_count": paid_members,
        "total_price": total_price,
        "expenditure": total_outflows,
        "balance_amount": balance_amount,
        "total_amt": total_amt,
        "balance": balance,
        "rate": rate,
        "remaining_days": remaining_days,
        "remaining_seconds ": int(remaining_seconds % 60),
        "remaining_minutes ": int(remaining_minutes % 60),
        "remaining_hours": int(remaining_hours % 24),
        "receipt_url": receipt_url,
    }
    outflow_context = {
        "transactions": outflows,
        "total_price": total_price,
        "expenditure": total_outflows,
        "balance_amount": balance_amount,
        "total_amt": total_amt,
        "balance": balance,
        "rate": rate,
        "remaining_days": remaining_days,
        "remaining_seconds ": int(remaining_seconds % 60),
        "remaining_minutes ": int(remaining_minutes % 60),
        "remaining_hours": int(remaining_hours % 24),
        "receipt_url": receipt_url,
    }
    if sub_title == 'outflows':
        return render(request, "finance/payments/outflows.html", outflow_context)
    elif sub_title == 'inflows':
        return render(request, "finance/payments/inflows.html", inflow_context)
    else:
        return render(request, 'finance/cashflows/user_inflow.html', inflow_context)


def inflow(request):
    if request.method == "POST":
        form = InflowForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.sender = request.user
            form.save()
            return redirect("/finance/inflows/")
    else:
        form = InflowForm()
    return render(
        request, "finance/payments/payment_form.html", {"form": form}
    )

def outflow(request):
    if request.method == "POST":
        form = OutflowForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.sender = request.user
            form.save()
            return redirect("/finance/outflows/")
    else:
        form = OutflowForm()
    return render(
        request, "finance/payments/payment_form.html", {"form": form}
    )

@method_decorator(login_required, name="dispatch")
class InflowDetailView(DetailView):
    template_name = "finance/cashflows/inflow_detail.html"
    model = Inflow
    context_object_name = 'inflow'
    ordering = ["-transaction_date"]


def userlist(request, username):
    user_categories = UserCategory.objects.filter(user= request.user)
    #categories and subcategories
    (category,sub_category)=category_subcategory(user_categories)
    user = get_object_or_404(User, username=username)
    transactions = Transaction.objects.filter(sender=user)
    (total_price,total_amt,balance,receipt_url)=compute_amt(VisaService,transactions,rate,user_categories)
    # bal=float(total_price)- float(total_amt)
    bal=float(total_amt)
    reg_fee = 19.99
    # try:
    #     service = VisaService.objects.get(sub_category=sub_category)
    #     total_price = service.price + reg_fee
    # except VisaService.DoesNotExist:
    #     service = None
    #     total_price = reg_fee

    # total_price=float(total_price)*float(rate)
    # request.session['total_price'] = total_price
    today = date.today()
    contract_date = today.strftime("%d %B, %Y")

#     context = {
#     "items": [
#         {
#             "title": "Total Amount",
#             "amount": total_price,
#             "description": "Total amount",
#         },
#         {
#             "title": "Amount Paid",
#             "amount": total_amt,
#             "description": "Amount Paid",
#         },
#         {
#             "title": "Balance",
#             "amount": bal,
#             "description": "Unpaid Amount",
#         }
#     ],
#     "rate": rate,
#     "receipt_url": receipt_url,
#     "category": category,
#     "sub_category": sub_category,
# }

    context={
                "total_price": total_price,
                "total_amt": total_amt,
                "balance": balance,
                'inflow': transactions,
                "rate":rate,
                'receipt_url': receipt_url,
                'category': category,
                'sub_category': sub_category,
             }
    return render(request, 'finance/cashflows/user_inflow.html', context)

@method_decorator(login_required, name="dispatch")
class UserInflowListView(ListView):
    model = Inflow
    template_name = "finance/cashflows/user_inflow.html"
    context_object_name = "inflows"
    ordering = ["-transaction_date"]

@method_decorator(login_required, name="dispatch")
class OutflowListView(ListView):
    model = Outflow
    template_name = "finance/payments/outflows.html"
    context_object_name = "outflows"
    ordering = ["-transaction_date"]

@method_decorator(login_required, name="dispatch")
class InflowUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    success_url = "/finance/inflows/"
    template_name='finance/payments/payment_form.html'
    fields = [
        "sender",
        "receiver",
        "phone",
        "sender_phone",
        "category",
        # "task",
        "method",
        "period",
        "qty",
        "amount",
        "transaction_cost",
        "receipt_link",
        "description",
    ]

    def form_valid(self, form):
        # form.instance.sender = self.request.user
        return super().form_valid(form)

    def test_func(self):
        inflow = self.get_object()
        if self.request.user.is_superuser or self.request.user == inflow.sender:
            return True
        return False

@method_decorator(login_required, name="dispatch")
class InflowDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Transaction
    success_url = "/finance/inflows"
    template_name='finance/cashflows/transaction_confirm_delete.html'
    def test_func(self):
        inflow = self.get_object()
        # if self.request.user == inflow.sender:
        if self.request.user.is_superuser:
            return True
        return False
    
@method_decorator(login_required, name="dispatch")
class OutflowUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Outflow
    success_url = "/finance/outflows/"
    template_name='finance/payments/payment_form.html'
    fields = [
        "sender",
        "receiver",
        "phone",
        "category",
        # "task",
        # "method",
        # "period",
        "qty",
        "amount",
        "transaction_cost",
        "receipt_link",
        "description",
    ]

    def form_valid(self, form):
        # form.instance.sender = self.request.user
        return super().form_valid(form)

    def test_func(self):
        outflow = self.get_object()
        if self.request.user.is_superuser or self.request.user == outflow.sender:
            return True
        return False

@method_decorator(login_required, name="dispatch")
class OutflowDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Outflow
    success_url = "/finance/outflows"
    template_name='finance/cashflows/outflow_confirm_delete.html'
    def test_func(self):
        outflow = self.get_object()
        # if self.request.user == outflow.sender:
        if self.request.user.is_superuser:
            return True
        return False

