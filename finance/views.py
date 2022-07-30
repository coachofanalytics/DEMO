import datetime
import json
import ast
import re
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from requests import request
from accounts.forms import UserForm
from accounts.models import CustomerUser
from .models import Payment_Information, Payment_History, Default_Payment_Fees
from django.db.models import Q
from django.http import QueryDict
from django.shortcuts import render
from django.db.models import Count
from datetime import date, datetime, timedelta
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from management.utils import email_template

# from .forms import (
#     # TransactionForm,
#     OutflowForm,
#     InflowForm,
#     PolicyForm,
#     ManagementForm,
#     RequirementForm,
#     EvidenceForm,
# )
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from data.models import DSU

from django.conf import settings
from django.contrib.auth import get_user_model
from accounts.models import Tracker

# User=settings.AUTH_USER_MODEL
User = get_user_model()


# Create your views here.


# ================================STUDENT AND JOB SUPPORT CONTRACT FORM SUBMISSION================================


def contract_form_submission(request):
    try:
        if request.method == "POST":
            user_student_data = request.POST.get("usr_data")
            student_dict_data = QueryDict(user_student_data)
            username = student_dict_data.get("username")
            try:
                customer = CustomerUser.objects.get(username=username)
                ss = customer.id
                payment = Payment_Information.objects.get(customer_id_id=customer.id)
            except:
                customer = None
                payment = None
            if not payment:
                form = UserForm(student_dict_data)
                print("form --->", form)
                if form.cleaned_data.get("category") == 1:
                    form.instance.is_applicant = True
                elif form.cleaned_data.get("category") == 2:
                    form.instance.is_employee = True
                elif form.cleaned_data.get("category") == 3:
                    form.instance.is_client = True
                else:
                    form.instance.is_admin = True
                form.save()
            customer = CustomerUser.objects.get(username=username)
            payment_fees = int(request.POST.get("duration")) * 1000
            down_payment = int(request.POST.get("down_payment"))
            student_bonus_amount = request.POST.get("bonus")
            fee_balance = payment_fees - down_payment
            if request.POST.get("student_contract"):
                fee_balance = payment_fees - (down_payment + int(student_bonus_amount))
            plan = request.POST.get("duration")
            payment_method = request.POST.get("payment_type")
            client_signature = request.POST.get("client_sign")
            company_rep = request.POST.get("rep_name")
            client_date = request.POST.get("client_date")
            rep_date = request.POST.get("rep_date")
            if payment:
                payment_data = Payment_Information.objects.filter(
                    customer_id_id=int(customer.id)
                ).update(
                    payment_fees=int(payment_fees),
                    down_payment=down_payment,
                    student_bonus=student_bonus_amount,
                    fee_balance=int(fee_balance),
                    plan=plan,
                    payment_method=payment_method,
                    client_signature=client_signature,
                    company_rep=company_rep,
                    client_date=client_date,
                    rep_date=rep_date,
                )
            else:
                payment_data = Payment_Information(
                    payment_fees=int(payment_fees),
                    down_payment=down_payment,
                    student_bonus=student_bonus_amount,
                    fee_balance=int(fee_balance),
                    plan=plan,
                    payment_method=payment_method,
                    client_signature=client_signature,
                    company_rep=company_rep,
                    client_date=client_date,
                    rep_date=rep_date,
                    customer_id_id=int(customer.id),
                )
                payment_data.save()
            payment_history_data = Payment_History(
                payment_fees=int(payment_fees),
                down_payment=down_payment,
                student_bonus=student_bonus_amount,
                fee_balance=int(fee_balance),
                plan=plan,
                payment_method=payment_method,
                client_signature=client_signature,
                company_rep=company_rep,
                client_date=client_date,
                rep_date=rep_date,
                customer_id=int(customer.id),
            )
            payment_history_data.save()
            if payment:
                messages.success(request, f"Added New Contract For the {username}!")
                return redirect("accounts:user-list", username=request.user)
            else:
                messages.success(request, f"Account created for {username}!")
                return redirect("data:bitraining")
    except Exception as e:
        print("Student Form Creation Error ==>", print(e))
        return render(request, "my_supportcontract_form.html", {"error": e})


def mycontract(request, *args, **kwargs):
    username = kwargs.get("username")
    client_data = CustomerUser.objects.get(username=username)
    check_default_fee = Default_Payment_Fees.objects.all()
    if check_default_fee:
        default_fee = Default_Payment_Fees.objects.get(id=1)
    else:
        default_payment_fees = Default_Payment_Fees(
            job_down_payment_per_month=500,
            job_plan_hours_per_month=40,
            student_down_payment_per_month=500,
            student_bonus_payment_per_month=100,
        )
        default_payment_fees.save()
        default_fee = Default_Payment_Fees.objects.get(id=1)
    payemnt_details = Payment_Information.objects.get(customer_id_id=client_data.id)
    contract_date = payemnt_details.contract_submitted_date.strftime("%d %B, %Y")
    if client_data.category == 3 and client_data.sub_category == 1:
        return render(
            request,
            "my_supportcontract_form.html",
            {
                "job_support_data": client_data,
                "contract_date": contract_date,
                "payment_data": payemnt_details,
            },
        )
    if client_data.category == 3 and client_data.sub_category == 2:
        return render(
            request,
            "my_trainingcontract_form.html",
            {
                "student_data": client_data,
                "contract_date": contract_date,
                "payment_data": payemnt_details,
            },
        )

    return render(
        request, "my_supportcontract_form.html", {"job_support_data": client_data}
    )


@login_required
def newcontract(request, *args, **kwargs):
    username = kwargs.get("username")
    client_data = CustomerUser.objects.get(username=username)
    check_default_fee = Default_Payment_Fees.objects.all()
    if check_default_fee:
        default_fee = Default_Payment_Fees.objects.get(id=1)
    else:
        default_payment_fees = Default_Payment_Fees(
            job_down_payment_per_month=500,
            job_plan_hours_per_month=40,
            student_down_payment_per_month=500,
            student_bonus_payment_per_month=100,
        )
        default_payment_fees.save()
        default_fee = Default_Payment_Fees.objects.get(id=1)
    today = date.today()
    contract_date = today.strftime("%d %B, %Y")

    if client_data.category == 3 and client_data.sub_category == 1:
        return render(
            request,
            "management/doc_templates/supportcontract_form.html",
            {
                "job_support_data": client_data,
                "contract_date": contract_date,
                "default_fee": default_fee,
            },
        )
    if client_data.category == 3 and client_data.sub_category == 2:
        return render(
            request,
            "management/doc_templates/trainingcontract_form.html",
            {
                "student_data": client_data,
                "contract_date": contract_date,
                "default_fee": default_fee,
            },
        )


# @login_required
# def newcontract(request, *args, **kwargs):
# 	username = kwargs.get('username')
# 	client_data=CustomerUser.objects.get(username=username)
# 	check_default_fee = Default_Payment_Fees.objects.all()
# 	if check_default_fee:
# 		default_fee = Default_Payment_Fees.objects.get(id=1)
# 	else:
# 		default_payment_fees = Default_Payment_Fees(job_down_payment_per_month=500,
# 				job_plan_hours_per_month=40,
# 				student_down_payment_per_month=500,
# 				student_bonus_payment_per_month=100)
# 		default_payment_fees.save()
# 		default_fee = Default_Payment_Fees.objects.get(id=1)
# 	today = date.today()
# 	contract_date = today.strftime("%d %B, %Y")

# 	if client_data.category == 3 and client_data.sub_category == 1:
# 		return render(request, 'management/doc_templates/supportcontract_form.html',{'job_support_data': client_data,'contract_date':contract_date,'default_fee':default_fee})
# 	if client_data.category == 3 and client_data.sub_category == 2:
# 		return render(request, 'management/doc_templates/trainingcontract_form.html',{'student_data': client_data,'contract_date':contract_date,'default_fee':default_fee})


class PaymentCreateView(LoginRequiredMixin, CreateView):
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


class PaymentListView(ListView):
    model = Payment_History
    template_name = "finance/payments/payments.html"
    context_object_name = "payments"


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
    ]
    # fields=['user','activity_name','description','point']
    def form_valid(self, form):
        # form.instance.author=self.request.user
        if self.request.user.is_superuser:
            return super().form_valid(form)
        else:
            # return redirect("management:tasks")
            return render(request, "management/doc_templates/supportcontract_form.html")

    def test_func(self):
        task = self.get_object()
        if self.request.user.is_superuser:
            return True
        # elif self.request.user == task.employee:
        #     return True
        return False
