# Generated by Django 2.2.10 on 2020-11-07 08:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20201107_0544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 7, 8, 18, 22, 979633)),
        ),
        migrations.AlterField(
            model_name='child',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 7, 8, 18, 22, 980870)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 7, 8, 18, 22, 974580)),
        ),
    ]
