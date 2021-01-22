from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User, Associated_Company
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from accounts.models import *
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField
from datetime import datetime, date


class Color(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    # color         = models.CharField(max_length=30)
    # parent_color  = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='pcolor')

    color_name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    color = ColorField(default='#FF0000', unique=True)

    parent_color = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='pcolor')
    # parent_color = ColorField(null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="color_changed_by", editable=False,
                                   null=True, blank=True)

    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here

    def __str__(self):
        return self.color

    def __repr__(self):
        return self.__str__()

    def color_published(self):
        from django.utils.html import format_html
        from django.utils.html import mark_safe
        colorcode = '%s'
        if self.color:
            return format_html(
                '<div style="background:{}; width:80px; border-radius:10px; text-align:center;">{}</div>', self.color,
                self.color)

    def patent_color_published(self):
        from django.utils.html import format_html
        from django.utils.html import mark_safe
        colorcode = '%s'
        if self.parent_color:
            return format_html(
                '<div style="background:{}; width:80px; border-radius:10px; text-align:center;">{}</div>',
                self.parent_color, self.parent_color)

    class Meta:
        verbose_name_plural = "color"

    def next(self):
        try:
            return Color.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Color.objects.get(pk=self.pk - 1)
        except:
            return None


class Age(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    age = models.CharField(max_length=20, unique=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="age_changed_by", editable=False,
                                   null=True, blank=True)

    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here

    def __str__(self):
        return str(self.age) + ' year'

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.age

    class Meta:
        verbose_name_plural = "age"

    def next(self):
        try:
            return Age.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Age.objects.get(pk=self.pk - 1)
        except:
            return None


class Measurements(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    measurement = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    age = models.ForeignKey(Age, on_delete=models.PROTECT, )
    shoulder_to_apex = models.CharField(max_length=255, null=True, blank=True)
    cap_sleeve_length = models.CharField(max_length=255, null=True, blank=True)
    short_sleeve_length = models.CharField(max_length=255, null=True, blank=True)
    three_fourth_to_apex = models.CharField(max_length=255, null=True, blank=True)
    full_sleeve_length = models.CharField(max_length=255, null=True, blank=True)
    knee_round = models.CharField(max_length=255, null=True, blank=True)
    calf = models.CharField(max_length=255, null=True, blank=True)
    ankle_round = models.CharField(max_length=255, null=True, blank=True)
    waist_length = models.CharField(max_length=255, null=True, blank=True)
    neck_round = models.CharField(max_length=255, null=True, blank=True)
    front_neck_depth = models.CharField(max_length=255, null=True, blank=True)
    cross_front = models.CharField(max_length=255, null=True, blank=True)
    bust = models.CharField(max_length=255, null=True, blank=True)
    under_bust = models.CharField(max_length=255, null=True, blank=True)
    waist = models.CharField(max_length=255, null=True, blank=True)
    lower_waist = models.CharField(max_length=255, null=True, blank=True)
    wrist = models.CharField(max_length=255, null=True, blank=True)
    thigh_round = models.CharField(max_length=255, null=True, blank=True)
    lower_thigh = models.CharField(max_length=255, null=True, blank=True)
    arm_hole = models.CharField(max_length=255, null=True, blank=True)
    knee_length = models.CharField(max_length=255, null=True, blank=True)
    full_length = models.CharField(max_length=255, null=True, blank=True)
    shoulder = models.CharField(max_length=255, null=True, blank=True)
    back_neck_depth = models.CharField(max_length=255, null=True, blank=True)
    biceps = models.CharField(max_length=255, null=True, blank=True)
    elbow_round = models.CharField(max_length=255, null=True, blank=True)
    hips = models.CharField(max_length=255, null=True, blank=True)
    bottom_length = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.measurement

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "Measurement"


class Stockdetails(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    stock = models.CharField(max_length=255, unique=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="stockdetails_changed_by",
                                   editable=False, null=True, blank=True)

    def __str__(self):
        return self.stock

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "stock detail"

    def next(self):
        try:
            return Stockdetails.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Stockdetails.objects.get(pk=self.pk - 1)
        except:
            return None


class Enquiry(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    fullname = models.CharField(max_length=255, null=True, blank=True)
    contactno = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(max_length=300, )
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="hoityenquiry_changed_by",
                                   editable=False, null=True, blank=True)

    def __str__(self):
        return self.fullname

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "enquiry"

    def next(self):
        try:
            return Enquiry.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Enquiry.objects.get(pk=self.pk - 1)
        except:
            return None


class Styles(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    style_name = models.CharField(max_length=255, unique=True)
    parent_style = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='pstyle')
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="styles_changed_by", editable=False,
                                   null=True, blank=True)

    def __str__(self):
        return self.style_name

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "styles"

    def next(self):
        try:
            return Styles.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Styles.objects.get(pk=self.pk - 1)
        except:
            return None


class Fabric(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    fabric = models.CharField(max_length=255, unique=True)
    fabric_detail = models.TextField(null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="fabric_changed_by", editable=False,
                                   null=True, blank=True)

    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here

    def __str__(self):
        return self.fabric

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "fabric"

    def next(self):
        try:
            return Fabric.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Fabric.objects.get(pk=self.pk - 1)
        except:
            return None


class Currencycode(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    currency_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    base_currency = models.CharField(max_length=255, null=True, blank=True)
    conversion_rate = models.FloatField(null=True, blank=True)
    currency_symbol = models.CharField(max_length=255, unique=True, null=True, blank=True)
    currency_abbreviation = models.CharField(max_length=255, null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="currencycode_changed_by",
                                   editable=False, null=True, blank=True)

    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)

    # code ends here

    def __str__(self):
        return str(self.base_currency)

    def __repr__(self):
        return self.__str__()

    class Meta:
        db_table = 'hoitymoppet_currencycode'
        app_label = 'generic_links'
        verbose_name_plural = "Currency"

    def symbol(self):
        from django.utils.html import mark_safe
        if self.currency_symbol:
            return mark_safe('<div>%s</div>' % (self.currency_symbol))
        else:
            return 'No'


# class Country(models.Model):
#     status = models.CharField(max_length=20,
#         choices=(
#             ('active', 'Active'), 
#             ('inactive', 'Inactive'),
#         ),
#         default='active')
#     country_name = models.CharField(max_length=255, unique=True)
#     website_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
#     currency_symbol = models.ForeignKey(Currencycode, on_delete=models.PROTECT, null=True, blank=True, default=1)

#     def __str__(self):
#         return self.country_name

#     def __repr__(self):
#         return self.__str__()

#     def symbol(self):
#         from django.utils.html import mark_safe
#         if self.currency_symbol:
#             return mark_safe('<div>%s</div>'%(self.currency_symbol))
#         else:
#             return 'No'

#     class Meta:
#         verbose_name_plural = "Country"


class Country(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    country = CountryField(blank_label='(select country)', null=True, blank=True)
    currency = models.ForeignKey(Currencycode, on_delete=models.PROTECT, null=True, blank=True, )
    country_code = models.CharField(max_length=255, unique=True, null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="country_changed_by", editable=False,
                                   null=True, blank=True)
    # countrycode = models.CharField(max_length=255, null=True, blank=True)
    # website_name = models.CharField(max_length=255, null=True, blank=True)
    # currency_symbol = models.ForeignKey(Currencycode, on_delete=models.PROTECT, null=True, blank=True,)

    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here

    def __str__(self):
        return str(self.country)

    def __repr__(self):
        return self.__str__()

    # def symbol(self):
    #     from django.utils.html import mark_safe
    #     if self.currency_symbol:
    #         return mark_safe('<div>%s</div>'%(self.currency_symbol))
    #     else:
    #         return 'No'

    class Meta:
        db_table = 'hoitymoppet_country'
        app_label = 'generic_links'
        verbose_name_plural = "Country"

    def next(self):
        try:
            return Country.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Country.objects.get(pk=self.pk - 1)
        except:
            return None


class Lookbookcategories(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    category_name = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True, )
    category_summary = models.CharField(max_length=255, unique=True, null=True, blank=True)
    lookbookcategoryimage = models.ImageField(upload_to="hoitymoppet/lookbookcategoryimages", default="")
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="lookbookcategories_changed_by",
                                   editable=False, null=True, blank=True)

    def __str__(self):
        return self.category_name

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "lookbook categories"

    def image_thumbnail(self):
        from django.utils.html import mark_safe
        if self.lookbookcategoryimage:
            return mark_safe('<img src="%s" width="75px" height="auto" />' % (self.lookbookcategoryimage.url))
        else:
            return 'No Image Found'

    def next(self):
        try:
            return Lookbookcategories.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Lookbookcategories.objects.get(pk=self.pk - 1)
        except:
            return None


class Lookbook(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    lookbook_name = models.CharField(max_length=255)
    lookbook_summary = models.TextField(max_length=255, default="")
    # lookbook_details = models.TextField(default="")
    lookbook_details = RichTextUploadingField()
    lookbook_image = models.ImageField(upload_to="hoitymoppet/lookbookimages", default="")
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="lookbook_changed_by", editable=False,
                                   null=True, blank=True)

    def __str__(self):
        return self.lookbook_name

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "lookbook"

    def next(self):
        try:
            return Lookbook.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Lookbook.objects.get(pk=self.pk - 1)
        except:
            return None


class Careinstructions(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    cares_name = models.CharField(max_length=255, unique=True)
    # cares_details = models.TextField(default="")
    cares_details = RichTextUploadingField()
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="careinstructions_changed_by",
                                   editable=False, null=True, blank=True)

    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here

    def __str__(self):
        return self.cares_name

    def __repr__(self):
        return self.__str__()

    def care_instructions_details(self):
        from django.utils.html import strip_tags

        if self.cares_details:
            return strip_tags(self.cares_details)

    def next(self):
        try:
            return Careinstructions.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Careinstructions.objects.get(pk=self.pk - 1)
        except:
            return None

    class Meta:
        verbose_name_plural = "care instructions"


class Productsize(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    size_name = models.CharField(max_length=255, unique=True)
    size_details = RichTextUploadingField()
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="productsize_changed_by",
                                   editable=False, null=True, blank=True)

    def __str__(self):
        return self.size_name

    def __repr__(self):
        return self.__str__()

    def Product_size_details(self):
        from django.utils.html import strip_tags

        if self.size_details:
            return strip_tags(self.size_details)

    class Meta:
        verbose_name_plural = "Product Size"

    def next(self):
        try:
            return Productsize.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Productsize.objects.get(pk=self.pk - 1)
        except:
            return None


class Producttype(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    type_name = models.CharField(max_length=255, unique=True)
    type_details = models.TextField(null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="producttype_changed_by",
                                   editable=False, null=True, blank=True)

    def __str__(self):
        return self.type_name

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "Product Type"

    def next(self):
        try:
            return Producttype.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Producttype.objects.get(pk=self.pk - 1)
        except:
            return None

class Categories(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    category = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True, )
    parent_category = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True,
                                        related_name='pcategory')
    category_image = models.ImageField(upload_to='hoitymoppet/categoryimages', null=True, blank=True)
    invisible = models.BooleanField(default=False, blank=True, null=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="categories_changed_by", editable=False,
                                   null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)

    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here

    def __str__(self):
        return self.category

    def __repr__(self):
        return self.__str__()

    class Meta:
        db_table = 'hoitymoppet_categories'
        app_label = 'generic_links'
        verbose_name_plural = "Category UI"

    def next(self):
        try:
            return Categories.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Categories.objects.get(pk=self.pk - 1)
        except:
            return None

    def image_thumbnail(self):
        from django.utils.html import mark_safe
        if self.category_image:
            return mark_safe('<img src="%s" width="75px" height="auto" />' % (self.category_image.url))
        else:
            return 'No Image Found'


class Slider(models.Model):
    slider_name = models.CharField(max_length=255)


class Advertise(models.Model):
    ads_name = models.CharField(max_length=255)


# Piyush:  code for creating Unit of measurement
class ProductUom(models.Model):
    name = models.CharField(max_length=50)
    rounding = models.FloatField("Rounding Precision", null=True, blank=True)
    company_id = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=20, choices=(('active', 'Active'), ('inactive', 'Inactive'),),
                              default='active')
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="productuom_changed_by", editable=False,
                                   null=True, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Product(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')

    product_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    # categories        = models.ForeignKey(Categories, on_delete=models.PROTECT)
    product_type = models.ForeignKey(Producttype, on_delete=models.PROTECT, null=True, blank=True)
    categories = models.ManyToManyField(Categories, blank=True)
    categories_erp = models.ForeignKey(Categories, on_delete=models.PROTECT, null=True, blank=True,
                                       related_name='category_erp')
    age = models.ManyToManyField(Age, )
    country = models.ForeignKey(HoityCountry, on_delete=models.PROTECT, null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    product_fabric = models.ForeignKey(Fabric, on_delete=models.PROTECT, null=True, blank=True)
    size = models.ForeignKey(Productsize, on_delete=models.PROTECT, null=True, blank=True)
    relative_product = models.ManyToManyField('self', blank=True, verbose_name="Related Product", )
    color = models.ManyToManyField(Color, blank=True)
    style = models.ForeignKey(Styles, on_delete=models.PROTECT, null=True, blank=True)
    item_detail = models.TextField(verbose_name="Product Details", null=True, blank=True)
    style_code = models.CharField(max_length=255, unique=True, verbose_name="Product Code", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2)
    stock = models.ForeignKey(Stockdetails, on_delete=models.PROTECT, null=True, blank=True)
    lookbook_category = models.ForeignKey(Lookbookcategories, on_delete=models.PROTECT, null=True, blank=True)
    productimage = models.ImageField(upload_to="hoitymoppet/productimages", )
    video_file = models.FileField(upload_to="hoitymoppet/productvideos", null=True, blank=True)
    careinstructions = models.ForeignKey(Careinstructions, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="product_changed_by", editable=False,
                                   null=True, blank=True)
    # tags                = TaggableManager()
    expected_delivery_date = models.IntegerField(verbose_name="Expected Delivery Days", blank=True, null=True)
    # Jatin added field for shipping charges
    shipping_charges = models.FloatField(null=True, blank=True, verbose_name="Shipping Charges")

    # Piyush: fields added for integration on 25-08-2020
    product_uom = models.ForeignKey(ProductUom, on_delete=models.PROTECT, null=True, blank=True)
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here

    def __str__(self):
        return self.product_name

    def __repr__(self):
        return self.__str__()

    def category(self):
        return "\n".join([str(p) for p in self.categories.all()])

    def relative_products(self):
        return ", ".join([str(p) for p in self.relative_product.all()])

    class Meta:
        verbose_name_plural = "product"

    def currentpage(self):
        try:
            return Product.objects.get(pk=self.pk)
        except:
            return None

    def total(self):
        try:
            return Product.objects.filter(status="active").count()
        except:
            return None

    def next(self):
        try:
            print("dohhhhhhhhhhhhhhhhhhhhhhh", Product.objects.get(pk=self.pk + 1))
            return Product.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            print("dohhhhhhhhhhhhhhhhhhhhhhh", Product.objects.get(pk=self.pk - 1))
            return Product.objects.get(pk=self.pk - 1)
        except:
            return None

    def image(self):
        from django.utils.html import mark_safe
        if self.productimage:
            return mark_safe('<img src="%s" width="75px" height="auto" style="border:1px solid #cccccc;" />' % (
                self.productimage.url))
        else:
            return 'No Image Found'

    # image.allow_tags = True
    # image.short_description = 'Image'

    # def get_absolute_url(self):
    #     return reverse('category_wise_products', kwargs={'slug': self.slug})

    # def get_absolute_url(self):
    #     url = reverse('productdetails', kwargs={'id': self.id, 'slug': self.slug})
    #     return url

    # def get_absolute_url(self):
    #     return reverse('productdetails', kwargs={'slug': self.slug, 'id':self.id})

    # def get_absolute_url(self):
    #     return urlresolvers.reverse('productdetails', kwargs={'pk': self.id, 'slug': self.slug})

    # def save(self, *args, **kwargs): # new
    #     if not self.slug:
    #         self.slug = slugify(self.product_name)
    #     return super().save(*args, **kwargs)

    # def save(self, *args, **kwargs): 
    #     slug = self.slug
    #     exists = Product.objects.filter(slug=slug).exists
    #     if exists:
    #         self.slug ='%s-%s'%(slug,self.id)
    #     super(Product, self).save(*args, **kwargs)


class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_id', null=True)
    image = models.ImageField(upload_to='hoitymoppet/productimages')
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.product.product_name) + "Images"

    class Meta:
        verbose_name_plural = "photo"

    def image_thumbnail(self):
        from django.utils.html import mark_safe
        if self.image:
            return mark_safe('<img src="%s" width="100px" height="100px" />' % (self.image.url))
        else:
            return 'No Image Found'


class Company(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    company_name = models.CharField(max_length=255)
    company_summary = models.TextField(max_length=255, default="")
    # company_details = models.TextField(default="")
    company_details = RichTextUploadingField()
    company_image = models.ImageField(upload_to="hoitymoppet/companyimages", default="")
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="hoitycompany_changed_by",
                                   editable=False, null=True, blank=True)

    def __str__(self):
        return self.company_name

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "company"


class Companyphoto(models.Model):
    companypics = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_id', null=True)
    image = models.ImageField(upload_to='hoitymoppet/companyimages')

    def __str__(self):
        return str(self.companypics.company_name) + "Images"


class Privacypolicy(models.Model):
    privacypolicy_name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "privacy policy"

class Disclaimer(models.Model):
    disclaimer_name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "disclaimer"

class Terms(models.Model):
    terms_name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "terms & conditions"


class UserCustomMeasuresMaster(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    user_custom_size_name = models.CharField(max_length=255, )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    age = models.ForeignKey(Age, on_delete=models.PROTECT, )
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="profile_usercustommeasuresmaster", null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="usercustommeasuresmaster_changed_by",
                                   editable=False, null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here

    def save(self, *args, **kwargs):
        self.profile = self.user.profile
        super(UserCustomMeasuresMaster, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user_custom_size_name)

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "User Custom Measures Master"


class UserCart(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)

    product_age = models.ForeignKey(Age, on_delete=models.PROTECT, null=True, blank=True)
    # user_custom_size = models.CharField(max_length=50, default=1)
    user_custom_size_master = models.ForeignKey(UserCustomMeasuresMaster, on_delete=models.PROTECT, null=True,
                                                blank=True)
    prod_color = models.ForeignKey(Color, verbose_name="Color of Product", on_delete=models.PROTECT, null=True,
                                   blank=True)

    product_color = ColorField()
    quantity = models.IntegerField('Quantity', default=0)
    total_price = models.FloatField("Total Price", blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField()
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="usercart_changed_by", editable=False,
                                   null=True, blank=True)

    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here

    def save(self, *args, **kwargs):
        self.profile = self.user.profile
        super(UserCart, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_id.product_name

    def get_total_item_price(self):
        return self.quantity * self.product_id.price

    def get_total_discount_item_price(self):
        a = self.quantity * (self.product_id.discount_price or self.product_id.price)
        return round(a,2) 
    get_total_discount_item_price.short_description = "Total Price"

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.product_id.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    def color(self):
        from django.utils.html import mark_safe
        if self.prod_color:
            return mark_safe('<div style="width:15px; height:15px; background:%s;"></div>' % (self.prod_color))
        else:
            return 'No'

    def image(self):
        from django.utils.html import mark_safe
        if self.product_id.productimage:
            return mark_safe('<img src="%s" width="50px" height="auto" style="border:1px solid #cccccc;"/>' % (
                self.product_id.productimage.url))
        else:
            return 'No Image Found'

    class Meta:
        db_table = 'hoitymoppet_usercart'
        app_label = 'enquiry_order'
        verbose_name_plural = "Customer Cart"

    def next(self):
        try:
            return UserCart.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return UserCart.objects.get(pk=self.pk - 1)
        except:
            return None


class UserWishList(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="userwishlist_changed_by",
                                   editable=False, null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here

    class Meta:
        db_table = 'hoitymoppet_userwishList'
        app_label = 'enquiry_order'
        verbose_name_plural = "user wishlist"

    # def __str__(self):
    #     return self.product_id

    def __str__(self):
        return str(self.product_id)

    def get_absolute_url(self):
        return reverse('category-wise-products', args=[self.product_id])

        # def next(self):
    #     try:
    #         return UserWishList.objects.get(pk=self.pk+1)
    #     except:
    #         return None

    # def previous(self):
    #     try:
    #         return UserWishList.objects.get(pk=self.pk-1)
    #     except:
    #         return None


class Recenltyviewedproducts(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)
    view_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="recentlyviewedproducts_changed_by",
                                   editable=False, null=True, blank=True)

    def __str__(self):
        return self.product_id.product_name

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "Recenlty Viewed Products"

    def next(self):
        try:
            return Recenltyviewedproducts.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Recenltyviewedproducts.objects.get(pk=self.pk - 1)
        except:
            return None


class UserCustomSize(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    age = models.ForeignKey(Age, on_delete=models.PROTECT, )
    measurements = models.ForeignKey(Measurements, on_delete=models.PROTECT, )
    user_custom_size_name = models.CharField(max_length=255, default=1)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    shoulder_to_apex = models.CharField(max_length=255, null=True, blank=True)
    cap_sleeve_length = models.CharField(max_length=255, null=True, blank=True)
    short_sleeve_length = models.CharField(max_length=255, null=True, blank=True)
    three_fourth_to_apex = models.CharField(max_length=255, null=True, blank=True)
    full_sleeve_length = models.CharField(max_length=255, null=True, blank=True)
    knee_round = models.CharField(max_length=255, null=True, blank=True)
    calf = models.CharField(max_length=255, null=True, blank=True)
    ankle_round = models.CharField(max_length=255, null=True, blank=True)
    waist_length = models.CharField(max_length=255, null=True, blank=True)
    neck_round = models.CharField(max_length=255, null=True, blank=True)
    front_neck_depth = models.CharField(max_length=255, null=True, blank=True)
    cross_front = models.CharField(max_length=255, null=True, blank=True)
    bust = models.CharField(max_length=255, null=True, blank=True)
    under_bust = models.CharField(max_length=255, null=True, blank=True)
    waist = models.CharField(max_length=255, null=True, blank=True)
    lower_waist = models.CharField(max_length=255, null=True, blank=True)
    wrist = models.CharField(max_length=255, null=True, blank=True)
    thigh_round = models.CharField(max_length=255, null=True, blank=True)
    lower_thigh = models.CharField(max_length=255, null=True, blank=True)
    arm_hole = models.CharField(max_length=255, null=True, blank=True)
    knee_length = models.CharField(max_length=255, null=True, blank=True)
    full_length = models.CharField(max_length=255, null=True, blank=True)
    shoulder = models.CharField(max_length=255, null=True, blank=True)
    back_neck_depth = models.CharField(max_length=255, null=True, blank=True)
    biceps = models.CharField(max_length=255, null=True, blank=True)
    elbow_round = models.CharField(max_length=255, null=True, blank=True)
    hips = models.CharField(max_length=255, null=True, blank=True)
    bottom_length = models.CharField(max_length=255, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="usercustomsize_changed_by",
                                   editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.profile = self.user.profile
        super(UserCustomSize, self).save(*args, **kwargs)

    def __str__(self):
        return self.shoulder_to_apex

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "user custom size"

    def next(self):
        try:
            return UserCustomSize.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return UserCustomSize.objects.get(pk=self.pk - 1)
        except:
            return None


class Coupon(models.Model):
    code = models.CharField(max_length=15, unique=True)
    coupon_description = models.CharField(max_length=255, default="Details of the coupons")
    company_id = models.ForeignKey(Associated_Company, on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateField(default=date.today)
    valid_from = models.DateField(default=date.today)
    valid_to = models.DateField(default=date.today)
    minimum_amount = models.FloatField('Minimum Order Amount', default=0.0)
    limit_number = models.IntegerField("Number of Times Coupons Can be Used", blank=True, null=True)
    discount_type = models.CharField(max_length=255, choices=(('Fixed', 'Fixed'), ('Percentage', 'Percentage'),),
                                     default='Fixed')
    discount = models.FloatField('Coupon Value', default=0.0)
    customer = models.ManyToManyField(User, blank=True)
    all_customer = models.BooleanField(blank=True, default=False)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    active = models.BooleanField(default=True)
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.code

    def customers(self):
        return ", ".join([str(p) for p in self.customer.all()])

    class Meta:
        db_table = 'hoitymoppet_coupon'
        app_label = 'enquiry_order'
        verbose_name_plural = "coupon"

    def next(self):
        try:
            return Coupon.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Coupon.objects.get(pk=self.pk - 1)
        except:
            return None


class CouponHistory(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    coupon_id = models.ForeignKey(Coupon, on_delete=models.PROTECT)
    order_id = models.ForeignKey('Order', on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateField(default=datetime.now)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="couponhistory_changed_by",
                                   editable=False, null=True, blank=True)

    def __str__(self):
        return self.coupon_id.code

    class Meta:
        db_table = 'hoitymoppet_couponhistory'
        app_label = 'enquiry_order'
        verbose_name_plural = "coupon history"

    def next(self):
        try:
            return CouponHistory.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return CouponHistory.objects.get(pk=self.pk - 1)
        except:
            return None


class SavedCard(models.Model):
    MONTHS = (
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    )

    YEARS = (
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
    )
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    card_holder_name = models.CharField(max_length=50, blank=True, null=True)
    card_no = models.CharField(max_length=20, blank=True, null=True)
    expiry_month = models.CharField(max_length=6, choices=MONTHS)
    expiry_year = models.CharField(max_length=6, choices=YEARS)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="savedcard_changed_by", editable=False,
                                   null=True, blank=True)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    ref_code = models.CharField(max_length=20, verbose_name="Order Id", blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    address_id = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name="Address", default=1)
    status_name = models.CharField(max_length=255,
                                   choices=(
                                       ('ordered', 'Ordered'),
                                       ('confirmed', 'Confirmed'),
                                       ('dispatched', 'Dispatched'),
                                       ('delivered', 'Delivered'),
                                   ),
                                   null=True, blank=True)

    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="order_changed_by", editable=False,
                                   null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    # Piyush: fields added for integration on 25-08-2020
    sale_order_name = models.CharField(max_length=250, null=True, blank=True)
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    maximum_days = models.IntegerField(blank=True, null=True)
    # Jatin added field for shipping
    shipping_charges = models.FloatField(blank=True, null=True)
    # jatin end
    expected_delivery_days = models.IntegerField(verbose_name="Expected Delivery Days", blank=True, null=True)
    # code ends here

    # Trilok Added this field to make a relationship with UserCustomMeasuresMaster 09-10-2020
    custom_size_master = models.ForeignKey(UserCustomMeasuresMaster, null=True, on_delete=models.PROTECT, blank=True)

    def save(self, *args, **kwargs):
        self.profile = self.user.profile
        super(Order, self).save(*args, **kwargs)

    class Meta:
        db_table = 'hoitymoppet_order'
        app_label = 'enquiry_order'
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.ref_code

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    def color(self):
        from django.utils.html import mark_safe
        if self.product_id.product_color:
            return mark_safe(
                '<div style="width:15px; height:15px; background:%s;"></div>' % (self.product_id.product_color))
        else:
            return 'No'

    def image(self):
        from django.utils.html import mark_safe
        if self.product_id.productimage:
            return mark_safe('<img src="%s" width="50px" height="auto" style="border:1px solid #cccccc;"/>' % (
                self.product_id.productimage.url))
        else:
            return 'No Image Found'

    def next(self):
        try:
            return Order.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return Order.objects.get(pk=self.pk - 1)
        except:
            return None


class OrderDetail(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    order_id = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_detail')
    product_id = models.ForeignKey(Product, verbose_name="Product", on_delete=models.PROTECT)
    ordered_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    # product_size = models.CharField(max_length=20)
    # user_custom_size = models.CharField(max_length=50, default=1)

    product_age = models.ForeignKey(Age, on_delete=models.PROTECT, null=True, blank=True)
    user_custom_size_master = models.ForeignKey(UserCustomMeasuresMaster, on_delete=models.PROTECT, null=True,
                                                blank=True)
    prod_color = models.ForeignKey(Color, verbose_name="Color of Product", on_delete=models.PROTECT, null=True,
                                   blank=True)

    product_color = ColorField()
    quantity = models.IntegerField('Quantity', default=0)
    price = models.FloatField("Price", blank=True, null=True)
    total_price = models.FloatField("Total Price", blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orderdetail_changed_by",
                                   editable=False, null=True, blank=True)

    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here

    def save(self, *args, **kwargs):
        print("ggggggggggggggggggggggggggg", self)
        self.profile = self.user.profile
        print("hhhhhhhhhhhhhhhhhh", self.user.profile)
        super(OrderDetail, self).save(*args, **kwargs)

    class Meta:
        db_table = 'hoitymoppet_orderdetail'
        app_label = 'enquiry_order'
        verbose_name_plural = "Order Detail"

    def color(self):
        from django.utils.html import mark_safe
        if self.prod_color:
            return mark_safe('<div style="width:15px; height:15px; background:%s;"></div>' % (self.prod_color))
        else:
            return 'No'

    def address(self):
        from django.utils.html import mark_safe
        if self.order_id.address_id:
            return mark_safe('<div>%s, %s, %s, %s, %s, %s, %s, %s</div>' % (self.order_id.address_id.name,
                                                                            self.order_id.address_id.mobile_no,
                                                                            self.order_id.address_id.address,
                                                                            self.order_id.address_id.city,
                                                                            self.order_id.address_id.user_state,
                                                                            self.order_id.address_id.pincode,
                                                                            self.order_id.address_id.locality,
                                                                            self.order_id.address_id.alternate_no))
        else:
            return 'No Data Found'

    def image(self):
        from django.utils.html import mark_safe
        if self.product_id.productimage:
            return mark_safe('<img src="%s" width="50px" height="auto" style="border:1px solid #cccccc;"/>' % (
                self.product_id.productimage.url))
        else:
            return 'No Image Found'

    # def get_item_price(self):
    #     return self.product_id.discount_price or self.product_id.price 
    # get_item_price.short_description = "Price"

    # def price(self):
    #     return self.product_id.discount_price or self.product_id.price 
    # price.short_description = "Price"

    def next(self):
        try:
            return OrderDetail.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return OrderDetail.objects.get(pk=self.pk - 1)
        except:
            return None


class OrderUpdate(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    order_id = models.IntegerField(default="")
    update_desc = models.TextField(default="")
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orderupdate_changed_by",
                                   editable=False, null=True, blank=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."

    class Meta:
        db_table = 'hoitymoppet_orderupdate'
        app_label = 'enquiry_order'


class DeliveryPlaces(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    delivery_place_name = models.CharField(max_length=255, unique=True)
    pincode = models.IntegerField(unique=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="deliveryplaces_changed_by",
                                   editable=False, null=True, blank=True)

    def __str__(self):
        return self.delivery_place_name

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "Delivery Places"


class Faq(models.Model):
    faq_name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Faq"


class Testimonials(models.Model):
    customer_name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Testimonials"


class Statusoption(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    status_name = models.CharField(max_length=255, unique=True)
    status_summary = models.CharField(max_length=255, unique=True, null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="statusoption_changed_by",
                                   editable=False, null=True, blank=True)

    def __str__(self):
        return self.status_name

    def __repr__(self):
        return self.__str__()

    class Meta:
        db_table = 'hoitymoppet_statusoption'
        app_label = 'enquiry_order'
        verbose_name_plural = "Status Option"


class TrackingStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    order_id = models.ForeignKey(Order, on_delete=models.PROTECT)
    # status_name = models.CharField(max_length=255,
    #                                choices=(
    #                                    ('Confirm', 'Confirm'),
    #                                    ('Dispatch', 'Dispatch'),
    #                                    ('Shiped', 'Shiped'),
    #                                    ('Delivered', 'Delivered'),
    #                                ),
    #                                null=True, blank=True)

    status_name = models.CharField(max_length=255,
                                   choices=(
                                       ('ordered', 'Ordered'),
                                       ('confirmed', 'Confirmed'),
                                       ('dispatched', 'Dispatched'),
                                       ('delivered', 'Delivered'),
                                   ),
                                   null=True, blank=True)
    description = models.CharField(max_length=255)
    status_date = models.DateTimeField(auto_now_add=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="trackingstatus_changed_by",
                                   editable=False, null=True, blank=True)

    def __str__(self):
        return self.status_name

    def __repr__(self):
        return self.__str__()

    class Meta:
        db_table = 'hoitymoppet_trackingstatus'
        app_label = 'enquiry_order'
        verbose_name_plural = "tracking status"


class UserQueries(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    order_id = models.CharField(max_length=255, verbose_name="Query Type", null=True, blank=True)
    query_summary = models.CharField(max_length=255, null=True, blank=True)
    query_details = models.TextField(default="", null=True, blank=True)
    upload_image = models.ImageField(upload_to='hoitymoppet/Userqueryimages', null=True, blank=True)
    solution = models.CharField(max_length=255, default="", null=True, blank=True)
    query_status = models.ForeignKey(Statusoption, on_delete=models.PROTECT, null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="userqueries_changed_by",
                                   editable=False, null=True, blank=True)

    def __str__(self):
        return self.query_summary

    def __repr__(self):
        return self.__str__()

    class Meta:
        db_table = 'hoitymoppet_userqueries'
        app_label = 'enquiry_order'
        verbose_name_plural = "User Queries"

    def next(self):
        try:
            return UserQueries.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return UserQueries.objects.get(pk=self.pk - 1)
        except:
            return None


class Measurement_Master(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    name = models.CharField(max_length=255, unique=True)

    # Piyush: fields added for integration on 25-08-2020
    size_unit = models.CharField(max_length=20, choices=(('centimeter', 'centimeter'),
                                                         ('inches', 'inches'),), default='inches')
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="measurementmaster_changed_by",
                                   editable=False, null=True, blank=True)
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)

    # code ends here

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "Measurement Master"


class Measures(models.Model):

    age = models.ForeignKey(Age, on_delete=models.PROTECT, )
    mesure_name = models.ForeignKey(Measurement_Master, on_delete=models.PROTECT, )
    value = models.FloatField(null=True, blank=True)

    # Piyush: fields added for integration on 25-08-2020
    size_unit = models.CharField(max_length=20, choices=(('centimeter', 'centimeter'),
                                                         ('inches', 'inches'),), default='inches')
    status = models.CharField(max_length=20, choices=(('active', 'Active'), ('inactive', 'Inactive'),),
                              default='active')
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="measures_changed_by", editable=False,
                                   null=True, blank=True)
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)

    # code ends here

    def __str__(self):
        return str(self.mesure_name)

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "Measures"


class UserCustomMeasures(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    user_custom_size_name = models.CharField(max_length=255, )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    age = models.ForeignKey(Age, on_delete=models.PROTECT, )
    custom_measures_master = models.ForeignKey(UserCustomMeasuresMaster, on_delete=models.CASCADE,
                                               related_name="user_custom_name", blank=True, null=True)
    measures = models.ForeignKey(Measures, on_delete=models.PROTECT, )
    standard_value = models.FloatField(null=True, blank=True)
    custom_value = models.FloatField(null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="usercustommeasures_changed_by",
                                   editable=False, null=True, blank=True)

    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here

    def __str__(self):
        return self.user_custom_size_name

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "User Custom Measures"


#####abhishek start 30-09-2020
class PaymentReference(models.Model):
    status = models.CharField(max_length=20,
                              choices=(
                                  ('active', 'Active'),
                                  ('inactive', 'Inactive'),
                              ),
                              default='active')
    username = models.CharField(max_length=255, blank=True, null=True)
    order_no = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    payment_date = models.CharField(max_length=255, blank=True, null=True)
    payment_mode = models.CharField(max_length=255, blank=True, null=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="paymentreference_changed_by",
                                   editable=False, null=True, blank=True)
    # Piyush: fields added for integration on 28-11-2020
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here
#####abhishek end 30-09-2020


# Piyush: code for creating currency model on 07-10-2020
class ResCurrency(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    symbol = models.CharField(max_length=255, blank=True, null=True)
    rounding = models.FloatField('Rounding Precision', blank=True, null=True)
    status = models.CharField(max_length=20, choices=(('active', 'Active'), ('inactive', 'Inactive')), default='active')
    position = models.CharField(max_length=255, blank=True, null=True)
    currency_unit_label = models.CharField(max_length=255, blank=True, null=True)
    currency_subunit_label = models.CharField(max_length=255, blank=True, null=True)
    create_date = models.DateField(auto_now_add=True, blank=True)
    write_date = models.DateField(auto_now=True)
    create_uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)

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
        db_table = 'hoitymoppet_rescurrency'
        app_label = 'generic_links'
        verbose_name_plural = "Res Currency"

    def next(self):
        try:
            return ResCurrency.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return ResCurrency.objects.get(pk=self.pk - 1)
        except:
            return None


# Piyush: code for creating currency model on 07-10-2020 ends here


# Piyush: code for creating currency rate model on 07-10-2020
class ResCurrencyRate(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    currency_id = models.ForeignKey(ResCurrency, on_delete=models.CASCADE, blank=True, null=True)
    company_id = models.ForeignKey(Associated_Company, on_delete=models.CASCADE, null=True, blank=True)
    create_uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='parent_created')
    write_uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='parent_edited')
    create_date = models.DateField(auto_now_add=True)
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
        db_table = 'hoitymoppet_rescurrencyrate'
        app_label = 'generic_links'
        verbose_name_plural = "Res Currency Rate"

    def next(self):
        try:
            return ResCurrencyRate.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return ResCurrencyRate.objects.get(pk=self.pk - 1)
        except:
            return None


# Piyush: code for creating country model on 07-10-2020 ends here


# Piyush: code for creating country model on 07-10-2020
class ResCountry(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    address_format = models.TextField(default='', blank=True, null=True)
    address_view_id = models.IntegerField(blank=True, null=True)
    currency_id = models.ForeignKey(ResCurrency, on_delete=models.CASCADE, blank=True, null=True)
    phone_code = models.IntegerField(blank=True, null=True)
    name_position = models.CharField(max_length=255, blank=True, null=True)
    create_uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='pcreated')
    create_date = models.DateField(auto_now_add=True, blank=True)
    write_date = models.DateField(auto_now=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
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
        db_table = 'hoitymoppet_rescountry'
        app_label = 'generic_links'
        verbose_name_plural = "Res Country"

    def next(self):
        try:
            return ResCountry.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return ResCountry.objects.get(pk=self.pk - 1)
        except:
            return None


# Piyush: code for creating country model on 07-10-2020 ends here


# Piyush: code for creating state model on 07-10-2020
class ResState(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.ForeignKey(ResCountry, on_delete=models.CASCADE, null=True, blank=True)
    create_uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='pcreate')
    create_date = models.DateField(auto_now_add=True, blank=True)
    write_date = models.DateField(auto_now=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
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
        db_table = 'hoitymoppet_resstate'
        app_label = 'generic_links'
        verbose_name_plural = "Res State"

    def next(self):
        try:
            return ResState.objects.get(pk=self.pk + 1)
        except:
            return None

    def previous(self):
        try:
            return ResState.objects.get(pk=self.pk - 1)
        except:
            return None


# Piyush: code for creating ResState model on 07-10-2020 ends here


# Jatin added model for shipping charges
class ShippingCharges(models.Model):
    associated_company = models.ForeignKey(Associated_Company, null=True, blank=True, on_delete=models.PROTECT, )
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    free_order_value = models.FloatField(blank=True, null=True)
    charge_type = models.CharField(max_length=20,
                                   choices=(
                                       ('specific_amount', 'Charge Specific Amount'),
                                       ('prod_based_charge', 'Product Based Charge'),
                                   ),
                                   default='specific_amount')
    max_charge = models.CharField(max_length=20,
                                  choices=(
                                      ('max_value', 'Max Value'),
                                      ('sum_value', 'Sum Of Value'),
                                  ), null=True, blank=True)
    specific_charge = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.associated_company)

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "Shipping Charges"
# Jatin:code for shipping charges ended


class BackgroundImage(models.Model):
    status = models.CharField(max_length=20,
        choices=(
            ('active', 'Active'), 
            ('inactive', 'Inactive'),
        ),
        default='active')
    image = models.ImageField(upload_to="hoitymoppet/backgroundimages", blank=True, null=True)
    video = models.FileField(upload_to="hoitymoppet/genericvideos", null=True, blank=True)
    item = models.CharField(max_length=20,
        choices=(
            ('measureguide', 'Measure Guide'), 
            ('measurevideo', 'Measure Video'), 
            ('loginimage', 'Login / Registration Image'), 
            ('faqimage', 'Faq Image'), 
            ('testimonialsimage', 'Testimonials Image'),
        ),
        unique=True, blank=True, null=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="image_changed_by", editable=False, null=True, blank=True)
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)

    def image_thumbnail(self):
        from django.utils.html import mark_safe
        if self.image:
            return mark_safe('<img src="%s" width="100px" height="auto" />'%(self.image.url))
        else:
            return 'No Image Found'

    class Meta:
        app_label = 'generic_links'
        verbose_name_plural = "Background Images"


# Piyush: code for adding shipping product on 16dec
class ShippingProduct(models.Model):
    name = models.CharField(max_length=20)
    percentage = models.IntegerField()
    shipping_charge = models.CharField(max_length=255, choices=(
                                           ('courier_charges', 'Courier Charges'),),
                                       default='courier_charges')
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    product_id = models.IntegerField()
    reference_id = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "Shipping Product"
# Piyush: code for adding shipping product on 16dec ends here
