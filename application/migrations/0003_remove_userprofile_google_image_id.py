# Generated by Django 3.2.6 on 2023-12-25 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_userprofile_google_image_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='google_image_id',
        ),
    ]
