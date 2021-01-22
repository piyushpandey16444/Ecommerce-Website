# Generated by Django 2.2.10 on 2020-11-06 13:17

import colorfield.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Businessorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('businessorder_name', models.CharField(max_length=255)),
                ('businessorder_url', models.CharField(default='', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'business Order',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15, unique=True)),
                ('coupon_description', models.CharField(default='Details of the coupons', max_length=255)),
                ('create_date', models.DateField(default=datetime.date.today)),
                ('valid_from', models.DateField(default=datetime.date.today)),
                ('valid_to', models.DateField(default=datetime.date.today)),
                ('minimum_amount', models.FloatField(default=0.0, verbose_name='Minimum Order Amount')),
                ('limit_number', models.IntegerField(blank=True, null=True, verbose_name='Number of Times Coupons Can be Used')),
                ('discount_type', models.CharField(choices=[('Fixed', 'Fixed'), ('Percentage', 'Percentage')], default='Fixed', max_length=255)),
                ('discount', models.FloatField(default=0.0, verbose_name='Coupon Value')),
                ('all_customer', models.BooleanField(blank=True, default=False)),
                ('edit_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('migrate_data', models.BooleanField(blank=True, default=False, null=True)),
                ('reference_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'coupon',
                'db_table': 'hoitymoppet_coupon',
            },
        ),
        migrations.CreateModel(
            name='CouponHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=20)),
                ('create_date', models.DateField(default=datetime.datetime.now)),
                ('edit_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'coupon history',
                'db_table': 'hoitymoppet_couponhistory',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Order Id')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('edit_date', models.DateTimeField(auto_now=True)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('ordered', models.BooleanField(default=False)),
                ('status_name', models.CharField(blank=True, choices=[('ordered', 'Ordered'), ('confirmed', 'Confirmed'), ('dispatched', 'Dispatched'), ('delivered', 'Delivered')], max_length=255, null=True)),
                ('sale_order_name', models.CharField(blank=True, max_length=250, null=True)),
                ('migrate_data', models.BooleanField(blank=True, default=False, null=True)),
                ('reference_id', models.IntegerField(blank=True, null=True)),
                ('maximum_days', models.IntegerField(blank=True, null=True)),
                ('shipping_charges', models.FloatField(blank=True, null=True)),
                ('expected_delivery_days', models.IntegerField(blank=True, null=True, verbose_name='Expected Delivery Days')),
            ],
            options={
                'verbose_name_plural': 'Orders',
                'db_table': 'hoitymoppet_order',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=20)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('edit_date', models.DateTimeField(auto_now=True)),
                ('product_color', colorfield.fields.ColorField(default='#FFFFFF', max_length=18)),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantity')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Price')),
                ('total_price', models.FloatField(blank=True, null=True, verbose_name='Total Price')),
                ('migrate_data', models.BooleanField(blank=True, default=False, null=True)),
                ('reference_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Order Detail',
                'db_table': 'hoitymoppet_orderdetail',
            },
        ),
        migrations.CreateModel(
            name='OrderUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=20)),
                ('order_id', models.IntegerField(default='')),
                ('update_desc', models.TextField(default='')),
                ('create_date', models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 6, 13, 17, 36, 564961))),
                ('edit_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'hoitymoppet_orderupdate',
            },
        ),
        migrations.CreateModel(
            name='Statusoption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=20)),
                ('status_name', models.CharField(max_length=255, unique=True)),
                ('status_summary', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('create_date', models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 6, 13, 17, 36, 567560))),
                ('edit_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Status Option',
                'db_table': 'hoitymoppet_statusoption',
            },
        ),
        migrations.CreateModel(
            name='TrackingStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(blank=True, choices=[('ordered', 'Ordered'), ('confirmed', 'Confirmed'), ('dispatched', 'Dispatched'), ('delivered', 'Delivered')], max_length=255, null=True)),
                ('description', models.CharField(max_length=255)),
                ('status_date', models.DateTimeField(auto_now_add=True)),
                ('edit_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'tracking status',
                'db_table': 'hoitymoppet_trackingstatus',
            },
        ),
        migrations.CreateModel(
            name='UserCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=20)),
                ('product_color', colorfield.fields.ColorField(default='#FFFFFF', max_length=18)),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantity')),
                ('total_price', models.FloatField(blank=True, null=True, verbose_name='Total Price')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('ordered', models.BooleanField()),
                ('migrate_data', models.BooleanField(blank=True, default=False, null=True)),
                ('reference_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Customer Cart',
                'db_table': 'hoitymoppet_usercart',
            },
        ),
        migrations.CreateModel(
            name='UserQueries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=255, null=True)),
                ('query_summary', models.CharField(blank=True, max_length=255, null=True)),
                ('query_details', models.TextField(blank=True, default='', null=True)),
                ('upload_image', models.ImageField(blank=True, null=True, upload_to='hoitymoppet/Userqueryimages')),
                ('solution', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('create_date', models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 6, 13, 17, 36, 569398))),
                ('edit_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'User Queries',
                'db_table': 'hoitymoppet_userqueries',
            },
        ),
        migrations.CreateModel(
            name='UserWishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=20)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('migrate_data', models.BooleanField(blank=True, default=False, null=True)),
                ('reference_id', models.IntegerField(blank=True, null=True)),
                ('associated_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='auth.Associated_Company')),
                ('changed_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='userwishlist_changed_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'user wishlist',
                'db_table': 'hoitymoppet_userwishList',
            },
        ),
    ]