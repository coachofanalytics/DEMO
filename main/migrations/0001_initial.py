
# Generated by Django 3.2.6 on 2022-09-06 12:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sender', models.CharField(default=None, max_length=100, null=True)),
                ('receiver', models.CharField(default=None, max_length=100, null=True)),
                ('phone', models.CharField(default=None, max_length=50, null=True)),
                ('activity_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('receipt', models.FileField(upload_to='Uploads/Receipt_doc/')),
                ('quantity', models.IntegerField()),
                ('amount', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('description', models.TextField(default=None)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Mpesa', 'Mpesa'), ('Check', 'Check'), ('Other', 'Other')], default='Other', max_length=25)),
                ('department', models.CharField(choices=[('HR Department', 'HR Department'), ('IT Department', 'IT Department'), ('Marketing Department', 'Marketing Department'), ('Finance Department', 'Finance Department'), ('Security Department', 'Security Department'), ('Management Department', 'Management Department'), ('Health Department', 'Health Department'), ('Other', 'Other')], default='Other', max_length=100)),
                ('category', models.CharField(choices=[('Salary', 'Salary'), ('Health', 'Health'), ('Transport', 'Transport'), ('Food & Accomodation', 'Food & Accomodation'), ('Internet & Airtime', 'Internet & Airtime'), ('Recruitment', 'Recruitment'), ('Labour', 'Labour'), ('Management', 'Management'), ('Electricity', 'Electricity'), ('Construction', 'Construction'), ('Other', 'Other')], default='Other', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Expenses',
            },
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_name', models.CharField(default=None, max_length=100, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('backgroundImage', models.ImageField(default='default.jpg', upload_to='background')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('image_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('service', models.ForeignKey(blank=True, max_length=200, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.service')),
            ],
        ),
    ]
