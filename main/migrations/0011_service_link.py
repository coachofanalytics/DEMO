# Generated by Django 3.2.6 on 2024-08-04 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_service_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='link',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
