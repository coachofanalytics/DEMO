# Generated by Django 3.0.7 on 2020-11-18 09:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('application_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('resume', models.FileField(upload_to='resumes/doc/')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('topic', models.CharField(default=None, max_length=100)),
                ('employee_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('punctuality', models.IntegerField(choices=[(1, 'Very Poor'), (2, 'Poor'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')])),
                ('communication', models.IntegerField(choices=[(1, 'Very Poor'), (2, 'Poor'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')])),
                ('understanding', models.IntegerField(choices=[(1, 'Very Poor'), (2, 'Poor'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')])),
                ('rated_by', models.CharField(default='CEO', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Rated',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('topic', models.CharField(default=None, max_length=100)),
                ('rating_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('punctuality', models.IntegerField(choices=[(1, 'Very Poor'), (2, 'Poor'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')])),
                ('communication', models.IntegerField(choices=[(1, 'Very Poor'), (2, 'Poor'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')])),
                ('understanding', models.IntegerField(choices=[(1, 'Very Poor'), (2, 'Poor'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')])),
            ],
        ),
        migrations.CreateModel(
            name='Iupload',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('ppt', models.FileField(upload_to='Powerpoints/doc/')),
                ('report', models.FileField(blank=True, null=True, upload_to='Reports/doc/')),
                ('workflow', models.FileField(blank=True, null=True, upload_to='Workflows/doc/')),
                ('proc', models.FileField(blank=True, null=True, upload_to='Procedures/doc/')),
                ('Applicant', models.ManyToManyField(to='application.Application')),
            ],
        ),
        migrations.CreateModel(
            name='InteviewUploads',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, null=True)),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ppt', models.FileField(default=None, upload_to='Powerpoints/doc/')),
                ('report', models.FileField(default=None, upload_to='Reports/doc/')),
                ('workflow', models.FileField(default=None, upload_to='Workflows/doc/')),
                ('proc', models.FileField(default=None, upload_to='Procedures/doc/')),
                ('other', models.FileField(default=None, upload_to='Others/doc/')),
                ('Applicant', models.ManyToManyField(to='application.Application')),
            ],
        ),
        migrations.CreateModel(
            name='Applicant_Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='applicant_profile_pics')),
                ('applicant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
