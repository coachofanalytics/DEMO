# Generated by Django 3.2.6 on 2022-09-06 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashappMail',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True)),
                ('from_mail', models.EmailField(max_length=254)),
                ('to_mail', models.EmailField(max_length=254)),
                ('file_name', models.CharField(max_length=50)),
                ('full_path', models.CharField(max_length=255)),
                ('text_mail', models.TextField()),
                ('received_date', models.CharField(max_length=255)),
                ('parsed_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Daily_Date',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dates', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Driver_Details',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('driver_name', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location_Data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('country', models.CharField(blank=True, max_length=500, null=True)),
                ('state', models.CharField(blank=True, max_length=500, null=True)),
                ('city', models.CharField(blank=True, max_length=500, null=True)),
                ('location_name', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Traffic_Data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total_vechicle', models.IntegerField(blank=True, null=True)),
                ('speed_limit', models.FloatField(blank=True, null=True)),
                ('max_speed', models.FloatField(blank=True, null=True)),
                ('min_speed', models.FloatField(blank=True, null=True)),
                ('average_speed', models.FloatField(blank=True, null=True)),
                ('traffic_occur_perday_count', models.IntegerField(blank=True, null=True)),
                ('traffic_reason', models.CharField(blank=True, max_length=500, null=True)),
                ('traffic_level', models.CharField(blank=True, max_length=500, null=True)),
                ('road_category', models.CharField(blank=True, max_length=500, null=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Driver_Details_3', to='getdata.driver_details')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getdata.location_data')),
                ('traffic_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getdata.daily_date')),
            ],
        ),
        migrations.CreateModel(
            name='NTSA_Crash_Data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('crash_time', models.CharField(blank=True, max_length=100, null=True)),
                ('crash_severity', models.CharField(blank=True, max_length=500, null=True)),
                ('crash_type', models.CharField(blank=True, max_length=500, null=True)),
                ('crash_vehicle_count', models.CharField(blank=True, max_length=500, null=True)),
                ('vechicle_name', models.CharField(blank=True, max_length=500, null=True)),
                ('vechicle_type', models.CharField(blank=True, max_length=500, null=True)),
                ('crash_reason', models.CharField(blank=True, max_length=500, null=True)),
                ('weather_type', models.CharField(blank=True, max_length=500, null=True)),
                ('crash_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getdata.daily_date')),
                ('crash_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getdata.location_data')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Driver_Details_2', to='getdata.driver_details')),
            ],
        ),
        migrations.CreateModel(
            name='Meteorological_Data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('meteorological_time', models.CharField(blank=True, max_length=100, null=True)),
                ('temperature', models.FloatField(blank=True, null=True)),
                ('wind_speed', models.FloatField(blank=True, null=True)),
                ('rainfall', models.FloatField(blank=True, null=True)),
                ('humidity', models.FloatField(blank=True, null=True)),
                ('pressure', models.FloatField(blank=True, null=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Driver_Details_1', to='getdata.driver_details')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getdata.location_data')),
                ('meteorological_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getdata.daily_date')),
            ],
        ),
        migrations.CreateModel(
            name='Air_Quality_Data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('air_quality_time', models.CharField(blank=True, max_length=100, null=True)),
                ('particulate_matter', models.FloatField(blank=True, null=True)),
                ('air_quality_index', models.IntegerField(blank=True, null=True)),
                ('air_quality_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getdata.daily_date')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Driver_Details_4', to='getdata.driver_details')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getdata.location_data')),
            ],
        ),
    ]
