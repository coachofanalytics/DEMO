# Generated by Django 3.2.6 on 2024-01-16 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20240711_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeruser',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customeruser',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customeruser',
            name='email',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='customeruser',
            name='first_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='customeruser',
            name='last_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='customeruser',
            name='phone',
            field=models.CharField(default='90001', max_length=255),
        ),
        migrations.AlterField(
            model_name='customeruser',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
