# Generated by Django 2.2.10 on 2020-12-30 09:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry_order', '0011_auto_20201118_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderupdate',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 30, 9, 9, 5, 161088)),
        ),
        migrations.AlterField(
            model_name='statusoption',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 30, 9, 9, 5, 164473)),
        ),
        migrations.AlterField(
            model_name='userqueries',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 30, 9, 9, 5, 166870)),
        ),
    ]
