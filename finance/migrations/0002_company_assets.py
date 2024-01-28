# Generated by Django 3.2.6 on 2024-01-28 17:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company_Assets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('unit_amt', models.DecimalField(decimal_places=2, max_digits=10)),
                ('serial_number', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('purchase_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
