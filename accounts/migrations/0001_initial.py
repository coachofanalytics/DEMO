# Generated by Django 3.2.6 on 2024-04-10 01:57

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('email', models.CharField(max_length=100)),
                ('gender', models.IntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female')], null=True)),
                ('phone', models.CharField(default='90001', max_length=100)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('category', models.IntegerField(choices=[(1, 'Job Applicant'), (2, 'Coda Staff Member'), (3, 'Jobsupport'), (4, 'Student'), (5, 'Investor'), (6, 'General User')], default=999)),
                ('sub_category', models.IntegerField(blank=True, choices=[(0, 'No Selection'), (1, 'Full Time'), (2, 'Contractual'), (3, 'Agent'), (4, 'Short Term'), (5, 'Long Term'), (6, 'Other')], null=True)),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is admin')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Is employee')),
                ('is_client', models.BooleanField(default=False, verbose_name='Is Client')),
                ('is_applicant', models.BooleanField(default=False, verbose_name='Is applicant')),
                ('is_employee_contract_signed', models.BooleanField(default=False)),
                ('resume_file', models.FileField(blank=True, null=True, upload_to='resumes/doc/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Users',
                'ordering': ['username'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='departments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Basic', 'BASIC Department'), ('HR Department', 'HR Department'), ('IT Department', 'IT Department'), ('Marketing Department', 'Marketing Department'), ('Finance Department', 'Finance Department'), ('Project', 'Project'), ('Security Department', 'Security Department'), ('Management Department', 'Management Department'), ('Health Department', 'Health Department'), ('Other', 'Other')], default='Other', max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Department safe URL')),
                ('is_featured', models.BooleanField(default=True, verbose_name='Is featured')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='OverBoughtSold',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('last', models.CharField(blank=True, max_length=255, null=True)),
                ('volume', models.CharField(blank=True, max_length=255, null=True)),
                ('RSI', models.CharField(blank=True, max_length=255, null=True)),
                ('EPS', models.CharField(blank=True, max_length=255, null=True)),
                ('PE', models.CharField(blank=True, max_length=255, null=True)),
                ('rank', models.CharField(blank=True, max_length=255, null=True)),
                ('profit_margins', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Oversold',
            },
        ),
        migrations.CreateModel(
            name='Ticker_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=255, null=True)),
                ('overallrisk', models.DecimalField(blank=True, decimal_places=3, max_digits=17, null=True)),
                ('sharesshort', models.DecimalField(blank=True, decimal_places=3, max_digits=17, null=True)),
                ('enterprisetoebitda', models.DecimalField(blank=True, decimal_places=3, max_digits=17, null=True)),
                ('ebitda', models.DecimalField(blank=True, decimal_places=3, max_digits=17, null=True)),
                ('quickratio', models.DecimalField(blank=True, decimal_places=3, max_digits=17, null=True)),
                ('currentratio', models.DecimalField(blank=True, decimal_places=3, max_digits=17, null=True)),
                ('revenuegrowth', models.DecimalField(blank=True, decimal_places=3, max_digits=17, null=True)),
                ('fetched_date', models.DateField(auto_now_add=True, null=True)),
                ('industry', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'verbose_name_plural': 'Option Measures',
            },
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
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Mpesa', 'Mpesa'), ('Check', 'Check'), ('Other', 'Other')], default='Other', max_length=25)),
                ('category', models.CharField(choices=[('Salary', 'Salary'), ('Health', 'Health'), ('Transport', 'Transport'), ('Food_Accomodation', 'Food & Accomodation'), ('Internet_Airtime', 'Internet & Airtime'), ('Recruitment', 'Recruitment'), ('Labour', 'Labour'), ('Management', 'Management'), ('Electricity', 'Electricity'), ('Construction', 'Construction'), ('Other', 'Other')], default='Other', max_length=100)),
                ('department', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='accounts.departments')),
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
                ('subplan', models.IntegerField(null=True)),
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
                ('subplan', models.IntegerField(null=True)),
                ('payment_method', models.CharField(max_length=100)),
                ('contract_submitted_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('client_signature', models.CharField(max_length=1000)),
                ('company_rep', models.CharField(max_length=1000)),
                ('client_date', models.CharField(blank=True, max_length=100, null=True)),
                ('rep_date', models.CharField(blank=True, max_length=100, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_payment_history', to=settings.AUTH_USER_MODEL, verbose_name='Client Name')),
            ],
        ),
    ]
