# Generated by Django 2.2.10 on 2020-11-06 16:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20201106_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 6, 16, 40, 16, 238458)),
        ),
        migrations.AlterField(
            model_name='child',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 6, 16, 40, 16, 239633)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 6, 16, 40, 16, 233862)),
        ),
    ]
