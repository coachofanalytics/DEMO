import requests
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.db.models import Sum, Max
from django.shortcuts import get_object_or_404,render
from django.contrib import messages
from .models import  Transaction


def check_default_fee(Default_Payment_Fees,username):
    try:
        default_fee = get_object_or_404(Default_Payment_Fees, user=username)
        # default_fee = Default_Payment_Fees.objects.get(id=1)
    except:
        default_payment_fees = Default_Payment_Fees(job_down_payment_per_month=500,
				job_plan_hours_per_month=40,
				student_down_payment_per_month=500,
				student_bonus_payment_per_month=100)
        default_payment_fees.save()
        default_fee = Default_Payment_Fees.objects.get(id=1)
    return default_fee

#This function obtains exchange rate information
def get_exchange_rate(base, target):
    # api_key = 'YOUR_APP_ID'
    exchange_api_key = '07c439585ffa45e0a254d01fef4b0c33'
    # api_key = exchange_api_key
    url = f'https://openexchangerates.org/api/latest.json?app_id={exchange_api_key}&base={base}'
    response = requests.get(url)
    if response.status_code != 200:
        rate=135.50
    else:
        data = response.json()
        rate=data['rates'][target]
    print(rate)
    return rate

def compute_amt(transactions, rate):
    total_amt = 0
    total_paid = 0
    pledged = 0
    amount_ksh = 0
    receipt_url = None

    for transact in transactions:
        total_amt += transact.total_payment
        if transact.has_paid:
            total_paid += transact.total_paid
        if transact.receipturl:
            receipt_url = transact.receipturl
        else:
            return redirect('main:404error')

    pledged = total_amt - total_paid
    amount_ksh = total_amt * rate

    return pledged, total_amt, amount_ksh, receipt_url

# ==================================================
def DYCDefaultPayments():
    context_dict = {
        "student": {'total_amount': 5000, 'down_payment': 500,'early_registration_bonus':100,},
        "business": {'total_amount': 10000, 'down_payment': 500,'early_registration_bonus':100,},
        "greencard": {'total_amount': 20000, 'down_payment': 500,'early_registration_bonus':100,},
    }
    for usertype, values in context_dict.items():
        if usertype=='student':
            total_amount= values["total_amount"]
            down_payment= values["down_payment"]
            early_registration_bonus= values["early_registration_bonus"]
            print(total_amount,down_payment,early_registration_bonus)
    return total_amount,down_payment,early_registration_bonus