# Generated by Django 3.2.6 on 2024-10-29 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='Operations', max_length=100, null=True)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'verbose_name': 'Budget Category',
                'verbose_name_plural': 'Budget Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='BudgetSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='finance.budgetcategory')),
            ],
            options={
                'verbose_name': 'Budget Sub category',
                'verbose_name_plural': 'Budget Sub categories',
                'ordering': ['category', 'name'],
            },
        ),
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
                ('clients_category', models.CharField(choices=[('DYC', 'Diaspora Youth Caucus'), ('Other', 'Other')], default='Other', max_length=25)),
                ('category', models.CharField(choices=[('Registration Fee', 'Registration Fee'), ('Contributions', 'Contributions'), ('Donations', 'Donations'), ('GC Application', 'GC Application'), ('Business', 'Business'), ('Tourism', 'Tourism'), ('Stocks', 'Stocks'), ('Other', 'Other')], default='Other', max_length=25)),
                ('method', models.CharField(choices=[('Cash', 'Cash'), ('Mpesa', 'Mpesa'), ('Check', 'Check'), ('Cashapp', 'Cashapp'), ('Zelle', 'Zelle'), ('Venmo', 'Venmo'), ('Paypal', 'Paypal'), ('Other', 'Other')], default='Other', max_length=25)),
                ('period', models.CharField(choices=[('Weekly', 'Weekly'), ('Bi_Weekly', 'Bi_Weekly'), ('Monthly', 'Monthly'), ('Yearly', 'Yearly')], default='Other', max_length=25)),
                ('receiver', models.CharField(default=None, max_length=100, null=True)),
                ('phone', models.CharField(default=None, max_length=50, null=True)),
                ('sender_phone', models.CharField(default=None, max_length=50, null=True)),
                ('transaction_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('receipt_link', models.CharField(blank=True, max_length=100, null=True)),
                ('qty', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('transaction_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('description', models.TextField(default=None, max_length=1000)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('has_paid', models.BooleanField(blank=True, default=False, null=True)),
                ('sender', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['transaction_date'],
            },
        ),
        migrations.CreateModel(
            name='Payment_Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.IntegerField(blank=True, null=True)),
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
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_featured', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('sector', models.CharField(blank=True, max_length=100, null=True)),
                ('mission', models.CharField(blank=True, max_length=100, null=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='CodaBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_featured', models.BooleanField(default=False)),
                ('item', models.CharField(default=None, max_length=100, null=True)),
                ('cases', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('qty', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('unit_price', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('description', models.TextField(default=None, max_length=1000)),
                ('receipt_link', models.CharField(blank=True, max_length=255, null=True)),
                ('budget_leads', models.ManyToManyField(limit_choices_to=models.Q(models.Q(('category', 2), ('is_active', True), ('is_staff', True)), ('is_superuser', True), _connector='OR'), related_name='coda_budgets_as_leads', to='accounts.CustomerUser')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='budgetcategory', to='finance.budgetcategory')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_budgets', to='accounts.department')),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='budget_subcategory', to='finance.budgetsubcategory')),
            ],
            options={
                'verbose_name': 'Coda Budget',
                'verbose_name_plural': 'Coda Budget',
                'ordering': ['department', 'created_at', 'category', 'subcategory'],
            },
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory', models.CharField(blank=True, max_length=25, null=True)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('item', models.CharField(default=None, max_length=100, null=True)),
                ('cases', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('qty', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('unit_price', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('description', models.TextField(default=None, max_length=1000)),
                ('receipt_link', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('budget_lead', models.ForeignKey(limit_choices_to=models.Q(models.Q(('category', 2), ('is_active', True), ('is_staff', True)), ('is_superuser', True), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, related_name='budget_lead', to='accounts.customeruser')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_type', to='finance.budgetcategory')),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
    ]
