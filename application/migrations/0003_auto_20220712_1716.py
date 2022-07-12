# Generated by Django 3.2.6 on 2022-07-12 22:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0002_alter_applicant_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='applicant_profile',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is featured'),
        ),
        migrations.AlterField(
            model_name='applicant_profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Application_Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(blank=True, default='A', max_length=2)),
                ('image', models.ImageField(blank=True, default='default.jpg', upload_to='Application_Profile_pics')),
                ('upload_a', models.FileField(upload_to='Application_Profile/uploads')),
                ('upload_b', models.FileField(upload_to='Application_Profile/uploads')),
                ('upload_c', models.FileField(upload_to='Application_Profile/uploads')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True, verbose_name='Is featured')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
