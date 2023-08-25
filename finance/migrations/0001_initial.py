# Generated by Django 3.2.6 on 2023-04-06 07:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
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
        # migrations.CreateModel(
        #     name='LaptopSaving',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('period', models.CharField(max_length=10)),
        #         ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
        #         ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
        #     ],
        # ),
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
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Mpesa', 'Mpesa'), ('Check', 'Check'), ('Other', 'Other')], default='Other', max_length=25)),
                ('category', models.CharField(choices=[('Salary', 'Salary'), ('Health', 'Health'), ('Transport', 'Transport'), ('Food_Accomodation', 'Food & Accomodation'), ('Internet_Airtime', 'Internet & Airtime'), ('Recruitment', 'Recruitment'), ('Labour', 'Labour'), ('Management', 'Management'), ('Electricity', 'Electricity'), ('Construction', 'Construction'), ('Other', 'Other')], default='Other', max_length=100)),
                ('department', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='accounts.department')),
                ('sender', models.ForeignKey(blank=True, limit_choices_to={'is_active': True, 'is_employee': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to=settings.AUTH_USER_MODEL, verbose_name='sender')),
            ],
            options={
                'verbose_name_plural': 'Transactions',
                'ordering': ['-activity_date'],
            },
        ),
        migrations.CreateModel(
            name='TrainingLoan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Debit', 'Debit'), ('Credit', 'Credit')], max_length=25)),
                ('amount', models.BigIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is complete')),
                ('training_loan_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('total_earnings_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('deduction_date', models.DateField(auto_now_add=True)),
                ('deduction_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('balance_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('phone', models.CharField(default='90001', help_text='Start with Country Code ie 254******', max_length=100)),
                ('location', models.CharField(default='Makutano', max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('featured', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('added_by', models.ForeignKey(blank=True, limit_choices_to={'is_active': True, 'is_employee': True}, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='staff', to=settings.AUTH_USER_MODEL, verbose_name='staff')),
            ],
        ),
        # migrations.CreateModel(
        #     name='RetirementPackage',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('period', models.CharField(max_length=10)),
        #         ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
        #         ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
        #     ],
        # ),
        migrations.CreateModel(
            name='PayslipConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_status', models.BooleanField(default=True)),
                ('loan_amount', models.DecimalField(decimal_places=2, default=20000.0, max_digits=10)),
                ('loan_repayment_percentage', models.DecimalField(decimal_places=2, default=0.2, max_digits=5)),
                ('laptop_status', models.BooleanField(default=True)),
                ('lb_amount', models.DecimalField(decimal_places=2, default=1000.0, max_digits=10)),
                ('ls_amount', models.DecimalField(decimal_places=2, default=1000.0, max_digits=10)),
                ('ls_max_limit', models.DecimalField(decimal_places=2, default=20000.0, max_digits=10)),
                ('rp_starting_period', models.CharField(max_length=10)),
                ('rp_starting_amount', models.DecimalField(decimal_places=2, default=10000.0, max_digits=10)),
                ('rp_increment_percentage', models.DecimalField(decimal_places=2, default=0.01, max_digits=5)),
                ('rp_increment_max_percentage', models.DecimalField(decimal_places=2, default=0.05, max_digits=5)),
                ('rp_increment_percentage_increment', models.DecimalField(decimal_places=2, default=0.01, max_digits=5)),
                ('rp_increment_percentage_increment_cycle', models.IntegerField(default=12)),
                ('holiday_pay', models.DecimalField(decimal_places=2, default=3000.0, max_digits=10)),
                ('night_bonus', models.DecimalField(decimal_places=2, default=500.0, max_digits=10)),
                ('computer_maintenance', models.DecimalField(decimal_places=2, default=500.0, max_digits=10)),
                ('food_accommodation', models.DecimalField(decimal_places=2, default=1000.0, max_digits=10)),
                ('health', models.DecimalField(decimal_places=2, default=500.0, max_digits=10)),
                ('kra', models.DecimalField(decimal_places=2, default=300.0, max_digits=10)),
                ('eom_bonus', models.DecimalField(decimal_places=2, default=1500.0, max_digits=10)),
                ('eoq_bonus', models.DecimalField(decimal_places=2, default=1500.0, max_digits=10)),
                ('eoy_bonus', models.DecimalField(decimal_places=2, default=1500.0, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        # migrations.CreateModel(
        #     name='Payslip',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('period', models.CharField(max_length=10)),
        #         ('points', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
        #         ('earned_pay', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
        #         ('EOM', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
        #         ('EOQ', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
        #         ('EOY', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
        #         ('laptop_bonus', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
        #         ('holiday_wages', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
        #         ('night_allowance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
        #         ('FA', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
        #         ('computer_maintenance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
        #         ('health_care', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
        #         ('laptop_saving', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='finance.laptopsaving')),
        #         ('loan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='finance.trainingloan')),
        #         ('retirement_package', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='finance.retirementpackage')),
        #         ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
        #     ],
        # ),
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
            name='LoanUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_loan', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        # migrations.CreateModel(
        #     name='LBandLS',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('laptop_bonus', models.FloatField(null=True)),
        #         ('laptop_savings', models.FloatField(null=True)),
        #         ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
        #     ],
        # ),
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
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=255, unique=True)),
                ('unit_amt', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('qty', models.PositiveIntegerField()),
                ('bal_qty', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('featured', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('supplier', models.ForeignKey(limit_choices_to=models.Q(('active', True)), on_delete=django.db.models.deletion.RESTRICT, to='finance.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='DC48_Inflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clients_category', models.CharField(choices=[('DYC', 'Diaspora Youth Caucus'), ('DC48KENYA', 'DC48KENYA'), ('Other', 'Other')], default='Other', max_length=25)),
                ('category', models.CharField(choices=[('Registration Fee', 'Registration Fee'), ('Contributions', 'Contributions'), ('Donations', 'Donations'), ('GC Application', 'GC Application'), ('Business', 'Business'), ('Tourism', 'Tourism'), ('Stocks', 'Stocks'), ('Other', 'Other')], default='Other', max_length=25)),
                ('method', models.CharField(choices=[('Cash', 'Cash'), ('Mpesa', 'Mpesa'), ('Check', 'Check'), ('Cashapp', 'Cashapp'), ('Zelle', 'Zelle'), ('Venmo', 'Venmo'), ('Paypal', 'Paypal'), ('Other', 'Other')], default='Other', max_length=25)),
                ('period', models.CharField(choices=[('Weekly', 'Weekly'), ('Bi_Weekly', 'Bi_Weekly'), ('Monthly', 'Monthly'), ('Yearly', 'Yearly')], default='Other', max_length=25)),
                ('receiver', models.CharField(default=None, max_length=100, null=True)),
                ('phone', models.CharField(default=None, max_length=50, null=True)),
                ('transaction_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('receipt_link', models.CharField(blank=True, max_length=100, null=True)),
                ('qty', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('transaction_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('description', models.TextField(default=None, max_length=1000)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('has_paid', models.BooleanField(blank=True, default=False, null=True)),
                ('sender', models.ForeignKey(limit_choices_to=models.Q(('sub_category', 6), ('sub_category', 7), ('is_superuser', True), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, related_name='dc_inflows', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['transaction_date'],
            },
        ),
    ]
