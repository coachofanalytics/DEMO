# Generated by Django 3.2.6 on 2024-05-02 21:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('company', models.CharField(blank=True, max_length=254, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=500, null=True)),
                ('section', models.CharField(blank=True, default='A', max_length=2)),
                ('image', models.ImageField(blank=True, default='default.jpg', upload_to='Application_Profile_pics')),
                ('upload_a', models.FileField(blank=True, null=True, upload_to='Application_Profile/uploads')),
                ('upload_b', models.FileField(blank=True, null=True, upload_to='Application_Profile/uploads')),
                ('upload_c', models.FileField(blank=True, null=True, upload_to='Application_Profile/uploads')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is featured')),
                ('laptop_status', models.BooleanField(default=True, verbose_name='Is lap_status')),
                ('national_id_no', models.CharField(blank=True, max_length=254, null=True)),
                ('id_file', models.ImageField(blank=True, null=True, upload_to='id_files/')),
                ('emergency_name', models.CharField(blank=True, max_length=254, null=True)),
                ('emergency_address', models.CharField(blank=True, max_length=254, null=True)),
                ('emergency_citizenship', models.CharField(blank=True, max_length=254, null=True)),
                ('emergency_national_id_no', models.CharField(blank=True, max_length=254, null=True)),
                ('emergency_phone', models.CharField(blank=True, max_length=254, null=True)),
                ('emergency_email', models.CharField(blank=True, max_length=254, null=True)),
                ('image2', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='profile_image', to='main.assets')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
