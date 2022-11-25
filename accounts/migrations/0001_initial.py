# Generated by Django 3.2.6 on 2022-11-20 07:17

import accounts.models
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
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
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
                ('category', models.IntegerField(choices=[(1, 'Applicant Or Job Applicant'), (2, 'Coda Staff Member'), (3, 'Client Or Customer Or Student')], default=999)),
                ('sub_category', models.IntegerField(blank=True, choices=[(0, 'No Selection'), (1, 'Job Support'), (2, 'Student'), (3, 'Full Time'), (4, 'Contractual'), (5, 'Agent'), (6, 'Other')], null=True)),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is admin')),
                ('is_employee', models.BooleanField(default=False, verbose_name='Is employee')),
                ('is_client', models.BooleanField(default=False, verbose_name='Is Client')),
                ('is_applicant', models.BooleanField(default=False, verbose_name='Is applicant')),
                ('resume_file', models.FileField(blank=True, null=True, upload_to='resumes/doc/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['username'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('HR Department', 'HR Department'), ('IT Department', 'IT Department'), ('Marketing Department', 'Marketing Department'), ('Finance Department', 'Finance Department'), ('Security Department', 'Security Department'), ('Management Department', 'Management Department'), ('Health Department', 'Health Department'), ('Other', 'Other')], default='Other', max_length=100)),
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
            name='TaskGroups',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='Group A', max_length=55, unique=True)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Job_Support', 'Job_Support'), ('Interview', 'Interview'), ('Training', 'Training'), ('Mentorship', 'Mentorship'), ('Other', 'Other')], max_length=25)),
                ('sub_category', models.CharField(choices=[('Requirements', 'Requirements'), ('Troubleshooting', 'Troubleshooting'), ('Development', 'Development'), ('Testing', 'Testing'), ('Other', 'Other')], default='Other', max_length=25)),
                ('task', models.CharField(choices=[('reporting', 'reporting'), ('database', 'database'), ('Business Analysis', 'Business Analysis'), ('Data Cleaning', 'Data Cleaning'), ('Other', 'Other')], max_length=25)),
                ('plan', models.CharField(default='B', help_text='Required', max_length=255, verbose_name='group')),
                ('employee', models.CharField(default='CODA', help_text='Required', max_length=255, verbose_name='Company/End Client')),
                ('login_date', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.TimeField(auto_now_add=True)),
                ('duration', models.IntegerField(choices=[(1, 'One Hour'), (2, 'Two Hours'), (3, 'Three Hours'), (4, 'Four Hours'), (5, 'Five Hours'), (8, 'Eight Hours'), (10, 'Ten Hours')], default=2)),
                ('time', models.PositiveIntegerField(default=120, error_messages={'name': {' max_length': 'The maximum hours must be between 0 and 199'}}, help_text='Maximum 200')),
                ('author', models.ForeignKey(blank=True, limit_choices_to={'is_active': True, 'is_client': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Client', to=settings.AUTH_USER_MODEL, verbose_name='Client')),
                ('empname', models.ForeignKey(blank=True, limit_choices_to={'is_active': True, 'is_employee': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Employee', to=settings.AUTH_USER_MODEL, verbose_name='Employee')),
            ],
            options={
                'ordering': ['login_date'],
            },
        ),
        migrations.CreateModel(
            name='CredentialCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(help_text='Required', max_length=255, unique=True, verbose_name='Category Name')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='category safe URL')),
                ('description', models.TextField(default=None, max_length=1000)),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='entered on')),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=True)),
                ('department', models.ForeignKey(default=accounts.models.Department.get_default_pk, on_delete=django.db.models.deletion.CASCADE, to='accounts.department')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required', max_length=255, verbose_name='credential Name')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='credential safe URL')),
                ('description', models.TextField(default=None, max_length=1000)),
                ('link_name', models.CharField(default='General', max_length=255)),
                ('link', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(blank=True, default='No Password Needed', max_length=255, null=True)),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='entered on')),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=True)),
                ('user_types', models.CharField(choices=[('Superuser', 'Superuser'), ('Admin', 'Admin'), ('Employee', 'Employee'), ('Other', 'Other')], default='Other', max_length=25)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('category', models.ManyToManyField(blank=True, related_name='credentialcategory', to='accounts.CredentialCategory')),
            ],
            options={
                'verbose_name_plural': 'credentials',
            },
        ),
    ]
