# Generated by Django 3.2.6 on 2024-08-04 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_customeruser_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeruser',
            name='zipcode',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
