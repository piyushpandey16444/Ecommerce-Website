# Generated by Django 2.2.10 on 2020-11-12 06:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoitymoppet', '0005_auto_20201107_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='age',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 577030)),
        ),
        migrations.AlterField(
            model_name='careinstructions',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 595119)),
        ),
        migrations.AlterField(
            model_name='color',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 575716)),
        ),
        migrations.AlterField(
            model_name='company',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 606459)),
        ),
        migrations.AlterField(
            model_name='deliveryplaces',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 624263)),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 580626)),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 583708)),
        ),
        migrations.AlterField(
            model_name='lookbook',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 594060)),
        ),
        migrations.AlterField(
            model_name='lookbookcategories',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 592822)),
        ),
        migrations.AlterField(
            model_name='measurement_master',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 629912)),
        ),
        migrations.AlterField(
            model_name='measurements',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 578582)),
        ),
        migrations.AlterField(
            model_name='measures',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 631015)),
        ),
        migrations.AlterField(
            model_name='paymentreference',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 633386)),
        ),
        migrations.AlterField(
            model_name='productsize',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 596206)),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 597067)),
        ),
        migrations.AlterField(
            model_name='productuom',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 628978)),
        ),
        migrations.AlterField(
            model_name='recenltyviewedproducts',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 612936)),
        ),
        migrations.AlterField(
            model_name='savedcard',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 618543)),
        ),
        migrations.AlterField(
            model_name='stockdetails',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 579733)),
        ),
        migrations.AlterField(
            model_name='styles',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 582765)),
        ),
        migrations.AlterField(
            model_name='usercustommeasuresmaster',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 609540)),
        ),
    ]
