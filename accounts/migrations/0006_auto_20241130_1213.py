# Generated by Django 3.2.6 on 2024-11-30 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customeruser',
            name='address',
        ),
        migrations.RemoveField(
            model_name='customeruser',
            name='city',
        ),
        migrations.RemoveField(
            model_name='customeruser',
            name='country',
        ),
        migrations.RemoveField(
            model_name='customeruser',
            name='is_applicant',
        ),
        migrations.RemoveField(
            model_name='customeruser',
            name='is_employee_contract_signed',
        ),
        migrations.RemoveField(
            model_name='customeruser',
            name='resume_file',
        ),
        migrations.RemoveField(
            model_name='customeruser',
            name='state',
        ),
        migrations.RemoveField(
            model_name='customeruser',
            name='zipcode',
        ),
    ]
