# Generated by Django 3.2.6 on 2024-01-16 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20240116_1040'),
        ('management', '0002_category_link_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='category',
        ),
        migrations.AddField(
            model_name='subcategory',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.department'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
