from django.db import models
from datetime import datetime, date
from decimal import *
from enum import unique
from django.db.models import Q
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.contrib.auth import get_user_model
from accounts.models import Department
User = get_user_model()


# Create your models here.


class Payment_Information(models.Model):
    # id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(
        "accounts.CustomerUser",
        verbose_name=("Client Name"),
        on_delete=models.CASCADE,
        related_name="customer")
    payment_fees=models.IntegerField()
    down_payment=models.IntegerField(default=500)
    student_bonus=models.IntegerField(null=True,blank=True)
    fee_balance=models.IntegerField(default=None)
    plan = models.IntegerField()
    payment_method = models.CharField(max_length=100)
    contract_submitted_date = models.DateTimeField(default=timezone.now)
    client_signature = models.CharField(max_length=1000)
    company_rep = models.CharField(max_length=1000)
    client_date = models.CharField(max_length=100, null=True, blank=True)
    rep_date = models.CharField(max_length=100, null=True, blank=True)

    @property
    def student_balance(self):
        stu_bal = self.payment_fees - (int(self.down_payment) + int(self.student_bonus))
        return stu_bal
    @property
    def jobsupport_balance(self):
        support_bal = self.payment_fees - int(self.down_payment) 
        return support_bal

    @property
    def student_balance(self):
        stu_bal = self.payment_fees - (int(self.down_payment) + int(self.student_bonus))
        return stu_bal
    @property
    def jobsupport_balance(self):
        support_bal = self.payment_fees - int(self.down_payment) 
        return support_bal

class Payment_History(models.Model):
    # id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        User,
        verbose_name=("Client Name"),
        on_delete=models.CASCADE,
        related_name="customer_payment_history")
    payment_fees=models.IntegerField()
    down_payment=models.IntegerField(default=500)
    student_bonus=models.IntegerField(null=True,blank=True)
    fee_balance=models.IntegerField(default=None)
    down_payment = models.IntegerField(default=500)
    student_bonus = models.IntegerField(null=True, blank=True)
    fee_balance = models.IntegerField(default=None)
    plan = models.IntegerField()
    payment_method = models.CharField(max_length=100)
    contract_submitted_date = models.DateTimeField(default=timezone.now)
    client_signature = models.CharField(max_length=1000)
    company_rep = models.CharField(max_length=1000)
    client_date = models.CharField(max_length=100, null=True, blank=True)
    rep_date = models.CharField(max_length=100, null=True, blank=True)

class Default_Payment_Fees(models.Model):
    # id = models.AutoField(primary_key=True)
    job_down_payment_per_month = models.IntegerField(default=500)
    job_plan_hours_per_month = models.IntegerField(default=40)
    student_down_payment_per_month = models.IntegerField(default=500)
    student_bonus_payment_per_month = models.IntegerField(default=250)

    loan_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)

    def __str__(self):
        return str(self.loan_amount)


class PayslipConfig(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    # configs for loan
    loan_status = models.BooleanField(default=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, default=20000.00)
    loan_repayment_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.20)

    # configs for laptop service
    laptop_status = models.BooleanField(default=True)
    lb_amount = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    ls_amount = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    ls_max_limit = models.DecimalField(max_digits=10, decimal_places=2, default=20000.00)

    # configs for retirement package
    rp_starting_period = models.CharField(max_length=10)
    rp_starting_amount = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)
    rp_increment_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.01)
    rp_increment_max_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.05)
    rp_increment_percentage_increment = models.DecimalField(max_digits=5, decimal_places=2, default=0.01)
    rp_increment_percentage_increment_cycle = models.IntegerField(default=12)

    # configs for bonus
    holiday_pay = models.DecimalField(max_digits=10, decimal_places=2, default=3000.00)
    night_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)

    # configs for deductions
    computer_maintenance = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    food_accommodation = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    health = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    kra = models.DecimalField(max_digits=10, decimal_places=2, default=300.00)

    # employee of the month, quarter and year
    eom_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=1500.00)
    eoq_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=1500.00)
    eoy_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=1500.00)

    def __str__(self):
        return str(self.loan_amount)

class Transaction(models.Model):
    # Method of Category
    CAT_CHOICES = [
        ("Salary", "Salary"),
        ("Health", "Health"),
        ("Transport", "Transport"),
        ("Food_Accomodation", "Food & Accomodation"),
        ("Internet_Airtime", "Internet & Airtime"),
        ("Recruitment", "Recruitment"),
        ("Labour", "Labour"),
        ("Management", "Management"),
        ("Electricity", "Electricity"),
        ("Construction", "Construction"),
        ("Other", "Other"),
    ]
    # Method of Payment
    PAY_CHOICES = [
        ("Cash", "Cash"),
        ("Mpesa", "Mpesa"),
        ("Check", "Check"),
        ("Other", "Other"),
    ]
    sender = models.ForeignKey(
         User,
         verbose_name=_("sender"),
         related_name="sender", 
         null=True, blank=True,
         on_delete=models.SET_NULL,
         limit_choices_to={"is_employee": True, "is_active": True},
         )
    department = models.ForeignKey(
        to=Department, on_delete=models.CASCADE, default=None
        )
    # sender = models.CharField(max_length=100, null=True, default=None)
    receiver = models.CharField(max_length=100, null=True, default=None)
    phone = models.CharField(max_length=50, null=True, default=None)
    # department = models.CharField(max_length=100, default=None)
    type = models.CharField(max_length=100, default=None, null=True)
    activity_date = models.DateTimeField(default=timezone.now)
    receipt_link = models.CharField(max_length=100, blank=True, null=True)
    qty = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=None
    )
    transaction_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=0
    )
    description = models.TextField(max_length=1000, default=None)

    payment_method = models.CharField(
        max_length=25,
        choices=PAY_CHOICES,
        default="Other",
    )

    category = models.CharField(
        max_length=100,
        choices=CAT_CHOICES,
        default="Other",
    )

    def get_absolute_url(self):
        return reverse("management:transaction-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.id} Transactions"


# -------------------------------------CASH FLOW MODEL---------------------------------------

class Inflow(models.Model):
    # Period of Payment
    Weekly = "Weekly"
    Bi_Weekly = "Bi_Weekly"
    Monthly = "Monthly"
    Yearly = "Yearly"

    # Method of Payment
    Cash = "Cash"
    Mpesa = "Mpesa"
    Check = "Check"
    Cashapp = "Cashapp"
    Zelle = "Zelle"
    Venmo = "Venmo"
    Paypal = "Paypal"

    # Category.
    Job_Support = "Job_Support"
    Interview = "Interview"
    Training = "Training"
    Stocks = "Stocks"
    Blockchain = "Blockchain"
    Mentorship = "Mentorship"
    Other = "Other"
    # Task/Activities
    Reporting = "reporting"
    Database = "database"
    Business_Analysis = "Business Analysis"
    ETL = "Data Cleaning"
    Options = "Options"
    Other = "Any Other"

    PERIOD_CHOICES = [
        (Weekly, "Weekly"),
        (Bi_Weekly, "Bi_Weekly"),
        (Monthly, "Monthly"),
        (Yearly, "Yearly"),
    ]

    CAT_CHOICES = [
        (Job_Support, "Job_Support"),
        (Interview, "Interview"),
        (Training, "Training"),
        (Stocks, "Stocks"),
        (Blockchain, "Blockchain"),
        (Mentorship, "Mentorship"),
        (Other, "Other"),
    ]
    TASK_CHOICES = [
        (Reporting, "reporting"),
        (Database, "database"),
        (Business_Analysis, "Business Analysis"),
        (ETL, "Data Cleaning"),
        (Options, "Options"),
        (Other, "Other"),
    ]

    PAY_CHOICES = [
        (Cash, "Cash"),
        (Mpesa, "Mpesa"),
        (Check, "Check"),
        (Cashapp, "Cashapp"),
        (Zelle, "Zelle"),
        (Venmo, "Venmo"),
        (Paypal, "Paypal"),
        (Other, "Other"),
    ]

    category = models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
    )
    task = models.CharField(
        max_length=25,
        choices=TASK_CHOICES,
    )
    method = models.CharField(
        max_length=25,
        choices=PAY_CHOICES,
        default=Other,
    )

    period = models.CharField(
        max_length=25,
        choices=PERIOD_CHOICES,
        default=Other,
    )

    sender = models.ForeignKey("accounts.CustomerUser", on_delete=models.CASCADE, related_name="inflows")
    receiver = models.CharField(max_length=100, null=True, default=None)
    phone = models.CharField(max_length=50, null=True, default=None)
    transaction_date = models.DateTimeField(default=timezone.now)
    receipt_link = models.CharField(max_length=100, blank=True, null=True)
    qty = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=None
    )
    transaction_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=0
    )
    description = models.TextField(max_length=1000, default=None)

    class Meta:
        ordering = ["transaction_date"]

    def get_absolute_url(self):
        return reverse("management:inflow-detail", kwargs={"pk": self.pk})

    @property
    def end(self):
        # date_time = datetime.datetime.now() + datetime.timedelta(hours=2)
        date_time = self.login_date + datetime.timedelta(hours=0)
        endtime = date_time.strftime("%H:%M")
        return endtime
    # Computing total payment
    @property
    def total_payment(self):
        total = self.amount.objects.aggregate(TOTAL=Sum("amount"))["TOTAL"]
        return total


class TrainingLoan(models.Model):
    LOAN_CHOICES = [
        ("Debit", "Debit"),
        ("Credit", "Credit"),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.CharField(max_length=25, choices=LOAN_CHOICES,)
    amount = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField('Is complete', default=True)
    # training_loan_amount = models.ForeignKey('PayslipConfig',on_delete=models.CASCADE,null=True)
    training_loan_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_earnings_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    deduction_date = models.DateField(auto_now_add=True)
    deduction_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class LoanUsers(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_loan = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# ========================Food Models============================

class Supplier(models.Model):
    added_by= models.ForeignKey(
        User,
        verbose_name=_("staff"),
        related_name="staff",
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        limit_choices_to={"is_employee": True, "is_active": True},
    )
    supplier = models.CharField(
        max_length=255,
    )
    slug = models.SlugField(blank=True, null=True)
    phone = models.CharField(default="90001",
            max_length=100,
            help_text=_("Start with Country Code ie 254******"),
    )
    location = models.CharField(max_length=255,default='Makutano')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    featured=models.BooleanField(default=True)
    active=models.BooleanField(default=True)

    def get_absolute_url(self):
        return "/services/{slug}/".format(slug=self.slug)

    def __str__(self):
        return self.supplier

class Food(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.RESTRICT,
        limit_choices_to=Q(active=True)
    )
    item = models.CharField(
        max_length=255,
        unique=True,
    )
    unit_amt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    slug = models.SlugField(blank=True, null=True)
    qty=models.PositiveIntegerField()
    bal_qty=models.PositiveIntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    featured=models.BooleanField(default=False)
    active=models.BooleanField(default=True)

    def get_absolute_url(self):
        return "/services/{slug}/".format(slug=self.slug)

    def __str__(self):
        return self.item
    
    @property
    def budgeted_items(self):
        budgeted_qty=self.qty-self.bal_qty
        return budgeted_qty

    @property
    def total_amt(self):
        total_amt=Decimal(self.qty-self.bal_qty)*self.unit_amt
        return total_amt

