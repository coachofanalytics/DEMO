from datetime import datetime
import dateutil.relativedelta
from django.contrib.auth import get_user_model
from django.db.models import Sum, Max
from django.shortcuts import render

from .models import TrainingLoan, Transaction
from management.models import TaskHistory

from getdata.views import uploaddata
from main.utils import Finance,Data,Management
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

from django.contrib import messages
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

    # form = CsvImportForm()
    # data = {"form": form}
    # return render(request, "admin/csv_upload.html", data)

# def EOQ():
#     today = datetime.date.today()
#     lastMonth = today + dateutil.relativedelta.relativedelta(months=-3)
#     task_max_point = TaskHistory.objects.filter(
#         date__gte=lastMonth
#     ).aggregate(Max('point'))['point__max']
#     if(task_max_point > 0):
#         return TaskHistory.objects.filter(point=task_max_point)
#     return False
#
# def EOY():
#     today = datetime.date.today()
#     lastYear = today + dateutil.relativedelta.relativedelta(years=-1)
#     task_max_point = TaskHistory.objects.filter(
#         date__gte=lastYear
#     ).aggregate(Max('point'))['point__max']
#     if(task_max_point > 0):
#         return TaskHistory.objects.filter(point=task_max_point)
#     return False
