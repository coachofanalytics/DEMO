<<<<<<< HEAD
# Generated by Django 3.2.6 on 2022-09-12 22:23
=======
# Generated by Django 3.2.6 on 2022-09-06 12:44
>>>>>>> 9b94d33786fd53ef58deaed57fc5bf898fe8d169

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('document_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('doc_type', models.CharField(blank=True, max_length=100, null=True)),
                ('doc_name', models.CharField(blank=True, max_length=100, null=True)),
                ('doc', models.FileField(upload_to='document/doc/')),
            ],
            options={
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='Uploads',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('document_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('doc_type', models.CharField(blank=True, max_length=100, null=True)),
                ('doc_name', models.CharField(blank=True, max_length=100, null=True)),
                ('doc', models.FileField(upload_to='Uploads/doc/')),
                ('link', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Uploads',
            },
        ),
    ]
