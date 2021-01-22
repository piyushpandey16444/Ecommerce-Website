from django.db import models
from django.contrib import messages
from django.core.exceptions import ValidationError
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from datetime import datetime
from hoitymoppet.models import *


class HomePageSlider(models.Model):
    status = models.CharField(max_length=20,
        choices=(
            ('active', 'Active'), 
            ('inactive', 'Inactive'),
        ),
        default='active')
    associated_company  = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True,)
    sliders_category = models.ForeignKey(Categories, verbose_name="Category", on_delete=models.PROTECT,)
    slider_name = RichTextUploadingField(null=True, blank=True)
    slider_summary = RichTextUploadingField(null=True, blank=True)
    slider_image = models.ImageField(upload_to="hoitymoppet/sliderimages", null=True, blank=True)

    slider_image_position = models.CharField(max_length=20,
        choices=(
            ('bottom', 'Bottom'), 
            ('center center', 'Center & Center'),
            ('center top', 'Center & Top'),
            ('left top', 'Left & Top'),
            ('right top', 'Right & Top'),
            ('top', 'Top'),
        ),
        blank=True, null=True)

    video_file = models.FileField(upload_to="hoitymoppet/sliderimages", null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="homepageslider_changed_by", editable=False, null=True, blank=True)

    def __str__(self):
        return self.slider_name

    def __repr__(self):
        return self.__str__()

    def slide_name(self):
        from django.utils.html import strip_tags

        if self.slider_name:
            return strip_tags(self.slider_name)

    def slide_summary(self):
        from django.utils.html import strip_tags

        if self.slider_summary:
            return strip_tags(self.slider_summary)

    class Meta:
        verbose_name_plural = "slider"
        
    def image_thumbnail(self):
        from django.utils.html import mark_safe
        if self.slider_image:
            return mark_safe('<img src="%s" width="100px" height="auto" />'%(self.slider_image.url))
        else:
            return 'No Image Found'


    def next(self):
        try:
            return HomePageSlider.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return HomePageSlider.objects.get(pk=self.pk-1)
        except:
            return None


class HomePageAdvertise(models.Model):
    status = models.CharField(max_length=20,
        choices=(
            ('active', 'Active'), 
            ('inactive', 'Inactive'),
        ),
        default='active')
    associated_company  = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True,)
    ads_category = models.ForeignKey(Categories, verbose_name="Category", on_delete=models.PROTECT,)
    ads_name = RichTextUploadingField(null=True, blank=True)
    ads_summary = RichTextUploadingField(null=True, blank=True)
    ads_image = models.ImageField(upload_to="hoitymoppet/advertiseimages", null=True, blank=True)
    video_file = models.FileField(upload_to="hoitymoppet/advertiseimages", null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="homepageadvertise_changed_by", editable=False, null=True, blank=True)

    def __str__(self):
        return self.ads_name

    def __repr__(self):
        return self.__str__()

    def advertise_name(self):
        from django.utils.html import strip_tags

        if self.ads_name:
            return strip_tags(self.ads_name)

    def advertise_summary(self):
        from django.utils.html import strip_tags

        if self.ads_summary:
            return strip_tags(self.ads_summary)

    class Meta:
        verbose_name_plural = "advertise"

    def image_thumbnail(self):
        from django.utils.html import mark_safe
        if self.ads_image:
            return mark_safe('<img src="%s" width="100px" height="auto" />'%(self.ads_image.url))
        else:
            return 'No Image Found'

    def next(self):
        try:
            return HomePageAdvertise.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return HomePageAdvertise.objects.get(pk=self.pk-1)
        except:
            return None


class Homevideo(models.Model):
    status = models.CharField(max_length=20,
        choices=(
            ('active', 'Active'), 
            ('inactive', 'Inactive'),
        ),
        default='active')
    associated_company  = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True,)
    video_category = models.ForeignKey(Categories, verbose_name="Category", on_delete=models.PROTECT,)
    video_heading = RichTextUploadingField(null=True, blank=True)
    video_summary = RichTextUploadingField(null=True, blank=True)
    video_details = RichTextUploadingField(null=True, blank=True)
    video_file = models.FileField(upload_to="hoitymoppet/homepagevideos", null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="homepagevideo_changed_by", editable=False, null=True, blank=True)

    def __str__(self):
        return self.video_heading

    def __repr__(self):
        return self.__str__()

    def video_overview(self):
        from django.utils.html import strip_tags

        if self.video_details:
            return strip_tags(self.video_details)

    def video_thumbnail(self):
        from django.utils.html import mark_safe
        if self.video_file:
            return mark_safe('<iframe src="%s" width="100px" height="100px" frameborder="0" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'%(self.video_file.url))
        else:
            return 'No Image Found'

    class Meta:
        verbose_name_plural = "Home Video"

    def next(self):
        try:
            return Homevideo.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return Homevideo.objects.get(pk=self.pk-1)
        except:
            return None


class AboutUs(models.Model):
    status = models.CharField(max_length=20,
        choices=(
            ('active', 'Active'), 
            ('inactive', 'Inactive'),
        ),
        default='active')
    associated_company  = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    heading = models.CharField(max_length=255, default="")
    summary = models.TextField(max_length=255, null=True, blank=True,)
    details = RichTextUploadingField(null=True, blank=True,)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True,)
    upload_image = models.ImageField(upload_to="hoitymoppet/companyimages", default="")
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="aboutus_changed_by", editable=False, null=True, blank=True)

    def __str__(self):
        return self.heading

    def __repr__(self):
        return self.__str__()

    def overview(self):
        from django.utils.html import strip_tags

        if self.details:
            return strip_tags(self.details)

    class Meta:
        verbose_name_plural = "About Us"

    def image_thumbnail(self):
        from django.utils.html import mark_safe
        if self.upload_image:
            return mark_safe('<img src="%s" width="100px" height="auto" />'%(self.upload_image.url))
        else:
            return 'No Image Found'

    def next(self):
        try:
            return AboutUs.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return AboutUs.objects.get(pk=self.pk-1)
        except:
            return None


class Company(models.Model):
    status = models.CharField(max_length=20,
        choices=(
            ('active', 'Active'), 
            ('inactive', 'Inactive'),
        ),
        default='active')
    associated_company  = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    company_name = models.CharField(max_length=255)
    company_summary = models.TextField(max_length=255, default="")
    # company_details = models.TextField(default="")
    company_details = RichTextUploadingField()
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True,)
    company_image = models.ImageField(upload_to="hoitymoppet/companyimages", default="")
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='company_created_by', editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="company_changed_by", editable=False, null=True, blank=True)

    def __str__(self):
        return self.company_name

    def __repr__(self):
        return self.__str__()

    def company_overview(self):
        from django.utils.html import strip_tags

        if self.company_details:
            return strip_tags(self.company_details)

    class Meta:
        verbose_name_plural = "Company"

    def image_thumbnail(self):
        from django.utils.html import mark_safe
        if self.company_image:
            return mark_safe('<img src="%s" width="100px" height="auto" />'%(self.company_image.url))
        else:
            return 'No Image Found'

    def next(self):
        try:
            return Company.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return Company.objects.get(pk=self.pk-1)
        except:
            return None


class Companyphoto(models.Model):
    companypics = models.ForeignKey(Company, on_delete = models.CASCADE, related_name='company_id', null=True)
    image = models.ImageField(upload_to='hoitymoppet/companyimages')

    def __str__(self):
        return str(self.companypics.company_name) + "Images"


class Privacypolicy(models.Model):
    status = models.CharField(max_length=20,
        choices=(
            ('active', 'Active'), 
            ('inactive', 'Inactive'),
        ),
        default='active')
    associated_company  = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    privacypolicy_name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True,)
    privacypolicy_details = RichTextUploadingField(blank=True)
    upload_image = models.ImageField(upload_to="hoitymoppet/companyimages", default="")
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="privacypolicy_changed_by", editable=False, null=True, blank=True)

    def privacy_policy_details(self):
        from django.utils.html import strip_tags

        if self.privacypolicy_details:
            return strip_tags(self.privacypolicy_details)

    class Meta:
        verbose_name_plural = "privacy policy"
        # unique_together = [("status",)]


    def image_thumbnail(self):
        from django.utils.html import mark_safe
        if self.upload_image:
            return mark_safe('<img src="%s" width="100px" height="auto" />'%(self.upload_image.url))
        else:
            return 'No Image Found'


    def next(self):
        try:
            return Privacypolicy.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return Privacypolicy.objects.get(pk=self.pk-1)
        except:
            return None


class Disclaimer(models.Model):
    status = models.CharField(max_length=20,
        choices=(
            ('active', 'Active'), 
            ('inactive', 'Inactive'),
        ),
        default='active')
    associated_company  = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    disclaimer_name = models.CharField(verbose_name="Shipping & Handling Name", max_length=255)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True,)
    disclaimer_details = RichTextUploadingField(verbose_name="Shipping & Handling Details", blank=True)
    upload_image = models.ImageField(upload_to="hoitymoppet/companyimages", default="")
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="disclaimer_changed_by", editable=False, null=True, blank=True)

    def disclaimer_details_view(self):
        from django.utils.html import strip_tags

        if self.disclaimer_details:
            return strip_tags(self.disclaimer_details)

    class Meta:
        verbose_name_plural = "Shipping & Handling"
        # unique_together = [("status",)]


    def image_thumbnail(self):
        from django.utils.html import mark_safe
        if self.upload_image:
            return mark_safe('<img src="%s" width="100px" height="auto" />'%(self.upload_image.url))
        else:
            return 'No Image Found'


    def next(self):
        try:
            return Disclaimer.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return Disclaimer.objects.get(pk=self.pk-1)
        except:
            return None


class Terms(models.Model):
    status = models.CharField(max_length=20,
        choices=(
            ('active', 'Active'), 
            ('inactive', 'Inactive'),
        ),
        default='active')
    associated_company  = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    terms_name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True,)
    terms_details = RichTextUploadingField(blank=True)
    upload_image = models.ImageField(upload_to="hoitymoppet/companyimages", default="")
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="terms_changed_by", editable=False, null=True, blank=True)

    def terms_conditions_details(self):
        from django.utils.html import strip_tags

        if self.terms_details:
            return strip_tags(self.terms_details)

    class Meta:
        verbose_name_plural = "terms & conditions"
        # unique_together = [("status",)]


    def image_thumbnail(self):
        from django.utils.html import mark_safe
        if self.upload_image:
            return mark_safe('<img src="%s" width="100px" height="auto" />'%(self.upload_image.url))
        else:
            return 'No Image Found'


    def next(self):
        try:
            return Terms.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return Terms.objects.get(pk=self.pk-1)
        except:
            return None


class Enquiry(models.Model):
    fullname = models.CharField(max_length=255, null=True, blank=True)
    contactno = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(max_length=300, default="")
    response_summary = models.TextField(max_length=300, default="")
    upload_image = models.ImageField(upload_to='hoitymoppet/enquiryimages',)
    query_status   = models.ForeignKey(Statusoption, on_delete=models.PROTECT,)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='enquiry_created_by', editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="enquiry_changed_by", editable=False, null=True, blank=True)

    def __str__(self):
        return self.fullname

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "enquiry"

    def image(self):
        from django.utils.html import mark_safe
        if self.upload_image:
            return mark_safe('<img src="%s" width="75px" height="auto" />'%(self.upload_image.url))
        else:
            return 'No Image Found'

    def next(self):
        try:
            return Enquiry.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return Enquiry.objects.get(pk=self.pk-1)
        except:
            return None


class Faq(models.Model):
    status = models.CharField(max_length=20,
        choices=(
            ('active', 'Active'), 
            ('inactive', 'Inactive'),
        ),
        default='active')
    associated_company  = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    faq_name = models.CharField(max_length=255, default="")
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True,)
    faq_details = RichTextUploadingField(default="", null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="faq_changed_by", editable=False, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Faq"

    def next(self):
        try:
            return Faq.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return Faq.objects.get(pk=self.pk-1)
        except:
            return None


class Testimonials(models.Model):
    status = models.CharField(max_length=20,
        choices=(
            ('active', 'Active'), 
            ('inactive', 'Inactive'),
        ),
        default='active')
    associated_company  = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    customer_name = models.CharField(max_length=255, default="")
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True,)
    # customer_designation = models.CharField(max_length=255, null=True, blank=True)
    customer_feedback = models.TextField(default="", null=True, blank=True)
    customer_image = models.ImageField(upload_to='hoitymoppet/testimonialsimages')
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="testimonials_changed_by", editable=False, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Testimonials"
    
    def image_thumbnail(self):
        from django.utils.html import mark_safe
        if self.customer_image:
            return mark_safe('<img src="%s" width="100px" height="100px" />'%(self.customer_image.url))
        else:
            return 'No Image Found'

    def next(self):
        try:
            return Testimonials.objects.get(pk=self.pk+1)
        except:
            return None

    def previous(self):
        try:
            return Testimonials.objects.get(pk=self.pk-1)
        except:
            return None


class PaymentOptions(models.Model):
    status = models.CharField(max_length=20,
        choices=(
            ('active', 'Active'), 
            ('inactive', 'Inactive'),
        ),
        default='active')
    name = models.CharField(max_length=255, unique=True, verbose_name="Display Name",)
    code_name = models.CharField(max_length=255,)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="payment_options_changed_by", editable=False, null=True, blank=True)
    associated_company = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)

    # Piyush: fields added for integration on 25-08-2020
    migrate_data = models.BooleanField(default=False, blank=True, null=True)
    reference_id = models.IntegerField(blank=True, null=True)
    # code ends here

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "Payment Options"


class UiConfiguration(models.Model):
    status = models.CharField(max_length=20,
        choices=(
            ('active', 'Active'), 
            ('inactive', 'Inactive'),
        ),
        default='active')
    item_display_in_row = models.CharField(max_length=20,
        choices=(
            ('category', 'Category display in homepage'), 
            ('product', 'Products display in category page'),
            ('cod', 'Enable cash on delivery functionality'),
            ('paymentoptions', 'Select your payment options'),
            ('recentlyviewed', 'Display recently viewed products'),
        ),
        unique=True, blank=True, null=True)
    item_display = models.CharField(max_length=20,
        choices=(
            ('6', '6'),
            ('4', '4'), 
            ('3', '3'),
            ('2', '2'),
        ),
        default='4')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="notify_user", null=True, blank=True)
    number_of_days = models.IntegerField(blank=True, null=True)
    number_of_times = models.IntegerField(blank=True, null=True)
    paymentoptions = models.ManyToManyField(PaymentOptions, blank=True)
    enable = models.BooleanField(default=False, blank=True, null=True)
    associated_company  = models.ForeignKey(Associated_Company, on_delete=models.PROTECT, null=True, blank=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    edit_date = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="uiconfiguration_changed_by", editable=False, null=True, blank=True)
    
    def __str__(self):
        return self.item_display_in_row

    def __repr__(self):
        return self.__str__()

    def paymentoption(self):
        return ",\n".join([str(p) for p in self.paymentoptions.all()])

    class Meta:
        verbose_name_plural = "Ui Configuration"
