# Generated by Django 2.2.10 on 2020-11-12 07:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry_order', '0007_auto_20201112_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderupdate',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 234675)),
        ),
        migrations.AlterField(
            model_name='statusoption',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 237250)),
        ),
        migrations.AlterField(
            model_name='userqueries',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 239173)),
        ),
    ]
