# Generated by Django 2.2.10 on 2020-11-12 07:03

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hoitymoppet', '0006_auto_20201112_0617'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_uom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='hoitymoppet.ProductUom'),
        ),
        migrations.AlterField(
            model_name='age',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 189698)),
        ),
        migrations.AlterField(
            model_name='careinstructions',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 207089)),
        ),
        migrations.AlterField(
            model_name='color',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 188514)),
        ),
        migrations.AlterField(
            model_name='company',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 218889)),
        ),
        migrations.AlterField(
            model_name='deliveryplaces',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 235552)),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 194668)),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 196493)),
        ),
        migrations.AlterField(
            model_name='lookbook',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 206091)),
        ),
        migrations.AlterField(
            model_name='lookbookcategories',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 204821)),
        ),
        migrations.AlterField(
            model_name='measurement_master',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 240380)),
        ),
        migrations.AlterField(
            model_name='measurements',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 192502)),
        ),
        migrations.AlterField(
            model_name='measures',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 241455)),
        ),
        migrations.AlterField(
            model_name='paymentreference',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 243806)),
        ),
        migrations.AlterField(
            model_name='productsize',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 208244)),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 209127)),
        ),
        migrations.AlterField(
            model_name='productuom',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 211884)),
        ),
        migrations.AlterField(
            model_name='recenltyviewedproducts',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 224786)),
        ),
        migrations.AlterField(
            model_name='savedcard',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 230991)),
        ),
        migrations.AlterField(
            model_name='stockdetails',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 193687)),
        ),
        migrations.AlterField(
            model_name='styles',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 195622)),
        ),
        migrations.AlterField(
            model_name='usercustommeasuresmaster',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 7, 3, 44, 221594)),
        ),
    ]
