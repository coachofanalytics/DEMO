# Generated by Django 3.2.6 on 2023-03-17 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20230317_0558'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='serial',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='serial',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),

    ]
