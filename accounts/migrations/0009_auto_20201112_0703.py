# Generated by Django 2.2.10 on 2020-11-12 07:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20201112_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 72261)),
        ),
        migrations.AlterField(
            model_name='child',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 74214)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 64523)),
        ),
    ]
