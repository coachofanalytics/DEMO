# Generated by Django 3.2.6 on 2025-01-21 17:32

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


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
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('email', models.CharField(max_length=255)),
                ('category', models.IntegerField(choices=[(1, 'Ordinary Member (Free)'), (2, 'Active Member'), (3, 'Executive Member'), (4, 'FBO & Ordinary (Free)'), (5, 'Active Organization'), (6, 'Royal Organization')], default=999)),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is admin')),
                ('is_member', models.BooleanField(default=False, verbose_name='Is Member')),
                ('email_verified', models.BooleanField(default=False)),
                ('verification_token', models.UUIDField(blank=True, null=True, unique=True)),
                ('groups', models.ManyToManyField(related_name='custom_user_set', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(related_name='custom_user_set', to='auth.Permission')),
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
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('currency', models.CharField(default='KES', max_length=10)),
                ('status', models.CharField(choices=[('PAID', 'Paid'), ('NOT_PAID', 'Not Paid')], default='NOT_PAID', max_length=10)),
                ('paid_date', models.DateTimeField(blank=True, null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
