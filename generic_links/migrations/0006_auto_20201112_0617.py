# Generated by Django 2.2.10 on 2020-11-12 06:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generic_links', '0005_auto_20201107_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutus',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 644920)),
        ),
        migrations.AlterField(
            model_name='categories',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 597985)),
        ),
        migrations.AlterField(
            model_name='company',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 646248)),
        ),
        migrations.AlterField(
            model_name='country',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 591453)),
        ),
        migrations.AlterField(
            model_name='currencycode',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 584708)),
        ),
        migrations.AlterField(
            model_name='disclaimer',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 649531)),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 652013)),
        ),
        migrations.AlterField(
            model_name='faq',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 653180)),
        ),
        migrations.AlterField(
            model_name='homepageadvertise',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 642482)),
        ),
        migrations.AlterField(
            model_name='homepageslider',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 641062)),
        ),
        migrations.AlterField(
            model_name='homevideo',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 643736)),
        ),
        migrations.AlterField(
            model_name='paymentoptions',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 655704)),
        ),
        migrations.AlterField(
            model_name='privacypolicy',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 648269)),
        ),
        migrations.AlterField(
            model_name='terms',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 650732)),
        ),
        migrations.AlterField(
            model_name='testimonials',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 654511)),
        ),
        migrations.AlterField(
            model_name='uiconfiguration',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 12, 6, 17, 37, 656766)),
        ),
    ]
