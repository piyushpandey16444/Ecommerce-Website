# Generated by Django 2.2.10 on 2020-11-06 16:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry_order', '0002_auto_20201106_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderupdate',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 6, 16, 40, 16, 433370)),
        ),
        migrations.AlterField(
            model_name='statusoption',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 6, 16, 40, 16, 436840)),
        ),
        migrations.AlterField(
            model_name='userqueries',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 6, 16, 40, 16, 439408)),
        ),
    ]