import requests
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models import Sum, Max
from django.shortcuts import get_object_or_404,render
from django.contrib import messages
from .models import TrainingLoan, Transaction
from accounts.models import Department


CustomUser = get_user_model()
def calculate_loan(user):
    debit = TrainingLoan.objects.filter(
        user=user,
        category=TrainingLoan.DEBIT
    ).aggregate(Sum('value'))
    if debit['value__sum'] == None:
        debit['value__sum'] = 0
    credit = TrainingLoan.objects.filter(
        user=user,
        category=TrainingLoan.CREDIT
    ).aggregate(Sum('value'))
    if credit['value__sum'] == None:
        credit['value__sum'] = 0
    loan = debit['value__sum'] - credit['value__sum']
    return loan

def balance_loan(user):
    debit = TrainingLoan.objects.filter(
        user=user,
        category=TrainingLoan.DEBIT
    ).aggregate(Sum('value'))
    if debit['value__sum'] == None:
        debit['value__sum'] = 0
    credit = TrainingLoan.objects.filter(
        user=user,
        category=TrainingLoan.CREDIT
    ).aggregate(Sum('value'))
    if credit['value__sum'] == None:
        credit['value__sum'] = 0
    balloan = debit['value__sum'] - credit['value__sum']
    return balloan


def upload_csv(request):
    context = {
        "Finance": Finance,
        "Data": Data,
        "Management": Management,
    }
    if request.method == "POST":
        csv_file = request.FILES.get("csv_upload")
        if not csv_file.name.endswith(".csv"):
            # return HttpResponseRedirect(request.path_info)
            messages.warning(request, "Not a CSV file")
            return render(request, "getdata/uploaddata.html", context)
        # file= csv_file.read().decode("utf-8")
        try:
            file = csv_file.read().decode("ISO-8859-1")
            file_data = file.split("\n")
            csv_data = [line for line in file_data if line.strip() != ""]
            for x in csv_data:
                fields = x.split(",")
                date = datetime.strptime(str(fields[0]), '%m/%d/%Y').date()
                created = Transaction.objects.update_or_create(
                    activity_date=date,
                    sender=CustomUser.objects.filter(first_name=fields[0]).first(),
                    receiver=fields[2],
                    phone=fields[3],
                    qty=fields[4],
                    amount=fields[5],
                    payment_method=fields[6],
                    department=Department.objects.filter(id=fields[7]).first(),
                    category=fields[8],
                    type=fields[9],
                    description=fields[10],
                    receipt_link=fields[11],
                )
            # url = reverse("admin:index")
            messages.info(request, "data populated successsfully")
            return render(request, "getdata/uploaddata.html", context)
        except Exception as e:
            messages.warning(request, e)
            return render(request, "getdata/uploaddata.html", context)
    if request.method == 'GET':
        return render(request, "getdata/uploaddata.html", context)

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
    data = response.json()
    # print(data)
    return data['rates'][target]

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