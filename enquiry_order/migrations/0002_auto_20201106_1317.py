# Generated by Django 2.2.10 on 2020-11-06 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_auto_20201106_1317'),
        ('hoitymoppet', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
        ('enquiry_order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userwishlist',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hoitymoppet.Product'),
        ),
        migrations.AddField(
            model_name='userwishlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userqueries',
            name='associated_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='auth.Associated_Company'),
        ),
        migrations.AddField(
            model_name='userqueries',
            name='changed_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='userqueries_changed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userqueries',
            name='query_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='enquiry_order.Statusoption'),
        ),
        migrations.AddField(
            model_name='userqueries',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usercart',
            name='associated_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='auth.Associated_Company'),
        ),
        migrations.AddField(
            model_name='usercart',
            name='changed_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='usercart_changed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usercart',
            name='prod_color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='hoitymoppet.Color', verbose_name='Color of Product'),
        ),
        migrations.AddField(
            model_name='usercart',
            name='product_age',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='hoitymoppet.Age'),
        ),
        migrations.AddField(
            model_name='usercart',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hoitymoppet.Product'),
        ),
        migrations.AddField(
            model_name='usercart',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.Profile'),
        ),
        migrations.AddField(
            model_name='usercart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usercart',
            name='user_custom_size_master',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='hoitymoppet.UserCustomMeasuresMaster'),
        ),
        migrations.AddField(
            model_name='trackingstatus',
            name='associated_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='auth.Associated_Company'),
        ),
        migrations.AddField(
            model_name='trackingstatus',
            name='changed_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trackingstatus_changed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='trackingstatus',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='enquiry_order.Order'),
        ),
        migrations.AddField(
            model_name='trackingstatus',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='statusoption',
            name='associated_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='auth.Associated_Company'),
        ),
        migrations.AddField(
            model_name='statusoption',
            name='changed_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='statusoption_changed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='statusoption',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderupdate',
            name='associated_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='auth.Associated_Company'),
        ),
        migrations.AddField(
            model_name='orderupdate',
            name='changed_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orderupdate_changed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderupdate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='associated_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='auth.Associated_Company'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='changed_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orderdetail_changed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_detail', to='enquiry_order.Order'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='prod_color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='hoitymoppet.Color', verbose_name='Color of Product'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='product_age',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='hoitymoppet.Age'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hoitymoppet.Product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.Profile'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='user_custom_size_master',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='hoitymoppet.UserCustomMeasuresMaster'),
        ),
        migrations.AddField(
            model_name='order',
            name='address_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='accounts.Address', verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='order',
            name='associated_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='auth.Associated_Company'),
        ),
        migrations.AddField(
            model_name='order',
            name='changed_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_changed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='custom_size_master',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='hoitymoppet.UserCustomMeasuresMaster'),
        ),
        migrations.AddField(
            model_name='order',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.Profile'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='couponhistory',
            name='associated_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='auth.Associated_Company'),
        ),
        migrations.AddField(
            model_name='couponhistory',
            name='changed_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='couponhistory_changed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='couponhistory',
            name='coupon_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='enquiry_order.Coupon'),
        ),
        migrations.AddField(
            model_name='couponhistory',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='enquiry_order.Order'),
        ),
        migrations.AddField(
            model_name='couponhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coupon',
            name='company_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Associated_Company'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='customer',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
