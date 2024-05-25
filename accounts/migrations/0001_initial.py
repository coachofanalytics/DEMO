# Generated by Django 3.2.6 on 2024-05-25 07:09

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='employees_tracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=25)),
                ('sub_category', models.CharField(max_length=25)),
                ('task', models.CharField(max_length=25)),
                ('plan', models.CharField(max_length=255)),
                ('empname', models.IntegerField()),
                ('author', models.IntegerField()),
                ('employee', models.CharField(max_length=255)),
                ('login_date', models.DateTimeField()),
                ('start_time', models.TimeField(null=True)),
                ('duration', models.IntegerField(null=True)),
                ('time', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('email', models.CharField(max_length=255)),
                ('gender', models.IntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female')], null=True)),
                ('phone', models.CharField(default='90001', max_length=255)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('category', models.IntegerField(choices=[(1, 'Job Applicant'), (2, 'Coda Staff Member'), (3, 'Jobsupport'), (4, 'Student'), (5, 'Investor'), (6, 'Vendor'), (7, 'General User')], default=999)),
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
    ]
