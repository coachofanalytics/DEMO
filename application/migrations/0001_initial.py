# Generated by Django 3.2.6 on 2024-04-13 21:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Balancesheet_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category_type', models.CharField(choices=[('assets', 'Asset'), ('liability', 'Liability'), ('equity', 'Equity')], default='assets', max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name_plural': 'Balance Sheet Categories',
                'unique_together': {('name', 'category_type')},
            },
        ),
        migrations.CreateModel(
            name='BalanceSheet_Summary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Balance Sheets',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Balancesheet_entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('balance_sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='application.balancesheet_summary')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.balancesheet_category')),
            ],
            options={
                'verbose_name_plural': 'Balance Sheet Entries',
            },
        ),
        migrations.CreateModel(
            name='Balancesheet_categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category_type', models.CharField(choices=[('assets', 'Asset'), ('liability', 'Liability'), ('equity', 'Equity')], default='assets', max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name_plural': 'Balance Sheet Categories',
                'unique_together': {('name', 'category_type')},
            },
        ),
    ]
