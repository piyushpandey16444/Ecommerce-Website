from django.db import models
from django.contrib.auth.models import User, Associated_Company
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

# from django.hoitymoppet.models import ResCountry


User._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='profile')
    pancard_name = models.CharField(max_length=255, null=True, blank=True)
    pancard_number = models.CharField(max_length=255, null=True, blank=True)
    aadharcard_name = models.CharField(max_length=255, null=True, blank=True)
    aadharcard_number = models.CharField(max_length=255, null=True, blank=True)
    user_contact_number = models.CharField(max_length=20, verbose_name="Phone", null=True, blank=True)
    user_sex = models.CharField(max_length=10, verbose_name="Gender", null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_by', editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="profile_changed_by", editable=False, null=True, blank=True)
    

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return self.__str__()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    # below is commented because because getting error while forgot password
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()
    # End

    def first_name(self):
        from django.utils.html import mark_safe
        if self.user.first_name:
            return mark_safe('<div>%s</div>'%(self.user.first_name))

    def last_name(self):
        from django.utils.html import mark_safe
        if self.user.last_name:
            return mark_safe('<div>%s</div>'%(self.user.last_name))

    def email(self):
        from django.utils.html import mark_safe
        if self.user.email:
            return mark_safe('<div>%s</div>'%(self.user.email))


    # def my_button_field(self):
    #     from django.utils.html import format_html
    #     from django.utils.html import mark_safe
    #     return mark_safe('<a href="#" class="btn btn-primary btn-sm">Details</a>')
    # email.short_description = 'Action'
    # email.allow_tags = True


    def address(self):
        from django.utils.html import format_html
        from django.utils.html import mark_safe

        return format_html("<hr>".join([str(p) for p in self.address_set.all()]))


    def childs(self):
        from django.utils.html import format_html
        from django.utils.html import mark_safe

        return format_html("<hr>".join([str(p) for p in self.child_set.all()]))


    def orders(self):
        from django.utils.html import format_html
        from django.utils.html import mark_safe

        return format_html("<hr>".join([str(p) for p in self.order_set.all()]))


    def usercustomsizes(self):
        from django.utils.html import format_html
        from django.utils.html import mark_safe

        return format_html("<hr>".join([str(p) for p in self.usercustomsize_set.all()]))


    def customercart(self):
        from django.utils.html import format_html
        from django.utils.html import mark_safe

        return format_html("<hr>".join([str(p) for p in self.usercart_set.all()]))


    def admin_permission(self):
        from django.utils.html import mark_safe
        if self.user.is_staff:
            return mark_safe('<div style="font-weight:bold; color:#53af02;">%s</div>'%(self.user.is_staff))
        else:
            return mark_safe('<div style="font-weight:bold; color:#999999;">False</div>')

    class Meta:
        verbose_name_plural = "Customers"


# Piyush: code for creating currency model on 07-10-2020
class HoityCurrency(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    symbol = models.CharField(max_length=255, blank=True, null=True)
    rounding = models.FloatField('Rounding Precision', blank=True, null=True)
    status = models.CharField(max_length=20,choices=(('active', 'Active'),('inactive', 'Inactive')), default='active')
    position = models.CharField(max_length=255, blank=True, null=True)
    currency_unit_label = models.CharField(max_length=255, blank=True, null=True)
    currency_subunit_label = models.CharField(max_length=255, blank=True, null=True)
    # create_date = models.DateField(default=datetime.now(), blank=True)
    write_date = models.DateField(auto_now=True)
    create_uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='hoity_currency_name')

    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here
 
    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()
 
    # def symbol(self):
    #     from django.utils.html import mark_safe
    #     if self.currency_symbol:
    #         return mark_safe('<div>%s</div>'%(self.currency_symbol))
    #     else:
    #         return 'No'
 
    class Meta:
        db_table = 'hoitymoppet_hoitycurrency'
        app_label = 'generic_links'
        verbose_name_plural = "Hoity Currency"

    def next(self):
        try:
            return HoityCurrency.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return HoityCurrency.objects.get(pk=self.pk-1)
        except:
            return None

# Piyush: code for creating currency model on 07-10-2020 ends here


# Piyush: code for creating currency rate model on 07-10-2020
class HoityCurrencyRate(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    rate = models.IntegerField(blank=True, null=True)
    currency_id = models.ForeignKey(HoityCurrency, on_delete=models.CASCADE, blank=True, null=True)
    company_id = models.ForeignKey(Associated_Company, on_delete=models.CASCADE, null=True, blank=True)
    create_uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='hoity_parent_created')
    write_uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='hoity_parent_edited')
    # create_date = models.DateField(default=datetime.now(), blank=True)
    write_date = models.DateField(auto_now=True)

    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here
 
    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()
 
    # def symbol(self):
    #     from django.utils.html import mark_safe
    #     if self.currency_symbol:
    #         return mark_safe('<div>%s</div>'%(self.currency_symbol))
    #     else:
    #         return 'No'
 
    class Meta:
        db_table = 'hoitymoppet_hoitycurrencyrate'
        app_label = 'generic_links'
        verbose_name_plural = "Hoity Currency Rate"

    def next(self):
        try:
            return HoityCurrencyRate.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return HoityCurrencyRate.objects.get(pk=self.pk-1)
        except:
            return None

# Piyush: code for creating country model on 07-10-2020 ends here


# Piyush: code for creating country model on 07-10-2020
class HoityCountry(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    address_format = models.TextField(default='', blank=True, null=True)
    address_view_id = models.IntegerField(blank=True, null=True)
    currency_id = models.ForeignKey(HoityCurrency, on_delete=models.CASCADE, blank=True, null=True)
    phone_code = models.IntegerField(blank=True, null=True)
    name_position = models.CharField(max_length=255, blank=True, null=True)
    create_uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='hoity_pcreated')
    # create_date = models.DateField(default=datetime.now(), blank=True)
    write_date = models.DateField(auto_now=True)

    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here
 
    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()
 
    # def symbol(self):
    #     from django.utils.html import mark_safe
    #     if self.currency_symbol:
    #         return mark_safe('<div>%s</div>'%(self.currency_symbol))
    #     else:
    #         return 'No'
 
    class Meta:
        db_table = 'hoitymoppet_hoitycountry'
        app_label = 'generic_links'
        verbose_name_plural = "Hoity Country"

    def next(self):
        try:
            return HoityCountry.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return HoityCountry.objects.get(pk=self.pk-1)
        except:
            return None

# Piyush: code for creating country model on 07-10-2020 ends here


# Piyush: code for creating state model on 07-10-2020
class HoityState(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.ForeignKey(HoityCountry, on_delete=models.CASCADE, null=True, blank=True)
    create_uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='hoity_pcreate')
    # create_date = models.DateField(default=datetime.now(), blank=True)
    write_date = models.DateField(auto_now=True)

    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here
 
    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()
 
    # def symbol(self):
    #     from django.utils.html import mark_safe
    #     if self.currency_symbol:
    #         return mark_safe('<div>%s</div>'%(self.currency_symbol))
    #     else:
    #         return 'No'
 
    class Meta:
        db_table = 'hoitymoppet_hoitystate'
        app_label = 'generic_links'
        verbose_name_plural = "Hoity State"

    def next(self):
        try:
            return HoityState.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return HoityState.objects.get(pk=self.pk-1)
        except:
            return None

# Piyush: code for creating HoityState model on 07-10-2020 ends here


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user')
    name = models.CharField(max_length=255, null=True, blank=True)
    mobile_no = models.CharField(max_length=20, null=True, blank=True)
    pincode = models.CharField(max_length=255, null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    # state = models.CharField(max_length=50, null=True, blank=True)
    # state = models.CharField(max_length=50, null=True, blank=True)
    
    user_state = models.ForeignKey(HoityState, on_delete=models.PROTECT, null=True, blank=True)
    user_country = models.ForeignKey(HoityCountry, on_delete=models.PROTECT, null=True, blank=True)

    # country = models.CharField(max_length=50, null=True, blank=True)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    alternate_no = models.CharField(max_length=20, null=True, blank=True)
    default = models.BooleanField(default=False, null=True,)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="address_changed_by", editable=False, null=True, blank=True)
    editable = models.CharField(max_length=20, choices=(('true', 'True'), ('false', 'False'),), default='true')
    # Piyush: fields added for integration on 25-08-2020
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here

    def save(self, *args, **kwargs):
        self.profile = self.user.profile
        super(Address, self).save(*args, **kwargs)

    # def __str__(self):
    #     return self.name
    
    def __str__(self):
        return self.name + ', ' + self.address + ', ' + self.mobile_no + ', ' + self.city + ', '\
               + self.pincode + ', ' + self.landmark + ', ' + self.alternate_no

    def __repr__(self):
        return self.__str__()


    def next(self):
        try:
            return Address.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return Address.objects.get(pk=self.pk-1)
        except:
            return None

class Child(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='child')
    child_name = models.CharField(max_length=255, null=True, blank=True)
    child_birth_date = models.DateField()
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='child_created_by', editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="child_changed_by", editable=False, null=True, blank=True)

    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here

    def save(self, *args, **kwargs):
        self.profile = self.user.profile
        super(Child, self).save(*args, **kwargs)

    def __str__(self):
        return self.child_name + ', ' + str(self.child_birth_date)

    def __repr__(self):
        return self.__str__()


    def next(self):
        try:
            return Child.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return Child.objects.get(pk=self.pk-1)
        except:
            return None


# Piyush: code for creating email template model on 28-10-2020
class EmailDescription(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email_description = models.TextField(max_length=300, null=True, blank=True)
    subject = models.CharField(max_length=20,
                               choices=(
                                   ('registration', 'Registration Template'),
                                   ('order_confirmed', 'Order Confirmed'),
                                   ('order_delivered', "Order Delivered"),
                                   ('order_received', 'Order Received'),
                                   ('order_dispatched', 'Order Dispatched'),
                                   ('forget_password', 'Forget Password'),
                               ),
                               default='registration', null=True, blank=True)
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()

    class Meta:
        db_table = 'accounts_email_description'
        app_label = 'generic_links'
        verbose_name_plural = "Email Description"

    def next(self):
        try:
            return EmailDescription.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return EmailDescription.objects.get(pk=self.pk - 1)
        except:
            return None
# Piyush: code for creating EmailDescription model on 28-10-2020 ends here
