# Generated by Django 3.2.6 on 2023-04-25 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Default_Payment_Fees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_down_payment_per_month', models.IntegerField(default=500)),
                ('job_plan_hours_per_month', models.IntegerField(default=40)),
                ('student_down_payment_per_month', models.IntegerField(default=500)),
                ('student_bonus_payment_per_month', models.IntegerField(default=250)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.CharField(default=None, max_length=100, null=True)),
                ('phone', models.CharField(default=None, max_length=50, null=True)),
                ('type', models.CharField(default=None, max_length=100, null=True)),
                ('activity_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('receipt_link', models.CharField(blank=True, max_length=100, null=True)),
                ('qty', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('transaction_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('description', models.TextField(default=None, max_length=1000)),
                ('department', models.CharField(choices=[('HR', 'HR'), ('IT', 'IT'), ('HEALTH', 'HEALTH'), ('Other', 'Other')], default='Other', max_length=25)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Mpesa', 'Mpesa'), ('Check', 'Check'), ('Other', 'Other')], default='Other', max_length=25)),
                ('category', models.CharField(choices=[('Salary', 'Salary'), ('Health', 'Health'), ('Transport', 'Transport'), ('Food_Accomodation', 'Food & Accomodation'), ('Internet_Airtime', 'Internet & Airtime'), ('Recruitment', 'Recruitment'), ('Labour', 'Labour'), ('Management', 'Management'), ('Electricity', 'Electricity'), ('Construction', 'Construction'), ('Other', 'Other')], default='Other', max_length=100)),
                ('sender', models.ForeignKey(blank=True, limit_choices_to={'is_active': True, 'is_staff': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to=settings.AUTH_USER_MODEL, verbose_name='sender')),
            ],
            options={
                'verbose_name_plural': 'Transactions',
                'ordering': ['-activity_date'],
            },
        ),
        migrations.CreateModel(
            name='Payment_Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_fees', models.IntegerField()),
                ('down_payment', models.IntegerField(default=500)),
                ('student_bonus', models.IntegerField(blank=True, null=True)),
                ('fee_balance', models.IntegerField(default=None)),
                ('plan', models.IntegerField()),
                ('payment_method', models.CharField(max_length=100)),
                ('contract_submitted_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('client_signature', models.CharField(max_length=1000)),
                ('company_rep', models.CharField(max_length=1000)),
                ('client_date', models.CharField(blank=True, max_length=100, null=True)),
                ('rep_date', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL, verbose_name='Client Name')),
            ],
        ),
        migrations.CreateModel(
            name='Payment_History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_fees', models.IntegerField()),
                ('down_payment', models.IntegerField(default=500)),
                ('student_bonus', models.IntegerField(blank=True, null=True)),
                ('fee_balance', models.IntegerField(default=None)),
                ('plan', models.IntegerField()),
                ('payment_method', models.CharField(max_length=100)),
                ('contract_submitted_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('client_signature', models.CharField(max_length=1000)),
                ('company_rep', models.CharField(max_length=1000)),
                ('client_date', models.CharField(blank=True, max_length=100, null=True)),
                ('rep_date', models.CharField(blank=True, max_length=100, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_payment_history', to=settings.AUTH_USER_MODEL, verbose_name='Client Name')),
            ],
        ),
        migrations.CreateModel(
            name='Inflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Job_Support', 'Job_Support'), ('Interview', 'Interview'), ('Training', 'Training'), ('Stocks', 'Stocks'), ('Blockchain', 'Blockchain'), ('Mentorship', 'Mentorship'), ('Any Other', 'Other')], max_length=25)),
                ('task', models.CharField(choices=[('reporting', 'reporting'), ('database', 'database'), ('Business Analysis', 'Business Analysis'), ('Data Cleaning', 'Data Cleaning'), ('Options', 'Options'), ('Any Other', 'Other')], max_length=25)),
                ('method', models.CharField(choices=[('Cash', 'Cash'), ('Mpesa', 'Mpesa'), ('Check', 'Check'), ('Cashapp', 'Cashapp'), ('Zelle', 'Zelle'), ('Venmo', 'Venmo'), ('Paypal', 'Paypal'), ('Any Other', 'Other')], default='Any Other', max_length=25)),
                ('period', models.CharField(choices=[('Weekly', 'Weekly'), ('Bi_Weekly', 'Bi_Weekly'), ('Monthly', 'Monthly'), ('Yearly', 'Yearly')], default='Any Other', max_length=25)),
                ('receiver', models.CharField(default=None, max_length=100, null=True)),
                ('phone', models.CharField(default=None, max_length=50, null=True)),
                ('transaction_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('receipt_link', models.CharField(blank=True, max_length=100, null=True)),
                ('qty', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('transaction_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('description', models.TextField(default=None, max_length=1000)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inflows', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['transaction_date'],
            },
        ),
    ]
