# Generated by Django 3.2.6 on 2024-06-28 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('published_date', models.DateField()),
                ('is_event', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='news_images/')),
            ],
        ),
    ]
