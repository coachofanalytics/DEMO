# Generated by Django 3.2.6 on 2022-06-07 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0007_requirement'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirement',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]
