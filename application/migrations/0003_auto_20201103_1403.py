# Generated by Django 3.0.7 on 2020-11-03 20:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_rated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Uploads',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, null=True)),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('interviewppt', models.FileField(upload_to='interviewppt/ppt/')),
            ],
        ),
        migrations.AlterField(
            model_name='inteviewuploads',
            name='SQL',
            field=models.FileField(upload_to='interviewdb/dba/'),
        ),
        migrations.AlterField(
            model_name='inteviewuploads',
            name='other',
            field=models.FileField(upload_to='interviewother/general/'),
        ),
        migrations.AlterField(
            model_name='inteviewuploads',
            name='tableau',
            field=models.FileField(upload_to='interviewtab/tab/'),
        ),
    ]
