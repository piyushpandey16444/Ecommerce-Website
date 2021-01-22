from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib import messages

from django.contrib import admin
from django.shortcuts import redirect
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import *


class RemoveAdminDefaultMessageMixin:

    def remove_default_message(self, request):
        storage = messages.get_messages(request)
        try:
            del storage._queued_messages[-1]
        except KeyError:
            pass
        return True

    def response_add(self, request, obj, post_url_continue=None):
        """override"""
        response = super().response_add(request, obj, post_url_continue)
        self.remove_default_message(request)
        return response

    def response_change(self, request, obj):
        """override"""
        response = super().response_change(request, obj)
        self.remove_default_message(request)
        return response

    def response_delete(self, request, obj_display, obj_id):
        """override"""
        response = super().response_delete(request, obj_display, obj_id)
        self.remove_default_message(request)
        return response


class PhotoInlineCompany(admin.StackedInline):
    model = Companyphoto
    extra = 2


class AboutUsAdmin(RemoveAdminDefaultMessageMixin, admin.ModelAdmin):
    list_display = ('id', 'heading', 'summary', 'overview', 'associated_company', 'country', 'image_thumbnail', 'status')
    list_display_links = ('id', 'heading')

    readonly_fields = ["thumbnails",]


    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = AboutUs.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = AboutUs.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view


    def thumbnails(self, obj):
        from django.utils.html import mark_safe
        return mark_safe('<img src="{url}" width="75px" height="auto" style="border:1px solid #cccccc;" />'.format(
            url = obj.upload_image.url,
            )
        )

    # def save_model(self, request, obj, form, change):
    #     obj.save()
    #     for afile in request.FILES.getlist('photos_multiple'):
    #         photos = Companyphoto(company=obj, image=afile)
    #         photos.save()

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user# company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self,request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)
        
        country = form.base_fields["country"]

        country.widget.can_add_related = False
        country.widget.can_delete_related = False
        country.widget.can_change_related = False

        return form

    def save_model(self, request, obj, form, change):
        if obj.status == 'active':
            item = AboutUs.objects.filter(status ='active')
            if item:
                if item[0].id == obj.id:
                    super().save_model(request, obj, form, change)
                    messages.success(request, "Record changed successfully.")
                else:
                    messages.warning(request, "Active record already exists")
            else:
                super().save_model(request, obj, form, change)
                messages.success(request, "Record added successfully.")
        else:
            super().save_model(request, obj, form, change)
            messages.success(request, "Record added/changed successfully.")


class CompanyAdmin(admin.ModelAdmin):
    inlines = [PhotoInlineCompany]
    list_display = ('id', 'company_name', 'country', 'company_summary', 'company_overview', 'image_thumbnail', 'status')
    list_display_links = ('id', 'company_name')

    readonly_fields = ["thumbnails",]

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Company.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Company.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def thumbnails(self, obj):
        from django.utils.html import mark_safe
        return mark_safe('<img src="{url}" width="75px" height="auto" style="border:1px solid #cccccc;" />'.format(
            url = obj.company_image.url,
            )
        )

    def save_model(self, request, obj, form, change):
        obj.save()
        for afile in request.FILES.getlist('photos_multiple'):
            photos = Companyphoto(company=obj, image=afile)
            photos.save()

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user# company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self,request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)
        
        country = form.base_fields["country"]

        country.widget.can_add_related = False
        country.widget.can_delete_related = False
        country.widget.can_change_related = False

        return form


class HomevideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'video_heading', 'country', 'video_category', 'video_summary', 'video_overview', 'video_thumbnail', 'status')
    list_display_links = ('id', 'video_heading')

    list_filter = ['status',]

    readonly_fields = ["thumbnails",]


    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Homevideo.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Homevideo.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def thumbnails(self, obj):
        from django.utils.html import mark_safe
        return mark_safe('<iframe src="{url}" width="100px" height="100px" frameborder="0" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(
            url = obj.video_file.url,
            )
        )


    def changelist_view(self, request, extra_context=None):
        if len(request.GET) == 0:
            get_param = "status__exact=active"
            return redirect("{url}?{get_parms}".format(url=request.path, get_parms=get_param))
        return super(HomevideoAdmin, self).changelist_view(request, extra_context=extra_context)

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user# company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self,request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)
        
        country = form.base_fields["country"]
        video_category = form.base_fields["video_category"]

        country.widget.can_add_related = False
        country.widget.can_delete_related = False
        country.widget.can_change_related = False

        video_category.widget.can_add_related = False
        video_category.widget.can_delete_related = False
        video_category.widget.can_change_related = False

        return form


class HomePageSliderAdmin(admin.ModelAdmin):
    list_display = ('id', 'sliders_category', 'country', 'slide_name', 'slide_summary', 'image_thumbnail', 'slider_image_position', 'status')
    list_display_links = ('id', 'sliders_category', 'slide_name')

    list_filter = ['status',]

    readonly_fields = ["thumbnails",]


    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = HomePageSlider.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = HomePageSlider.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view


    def thumbnails(self, obj):
        from django.utils.html import mark_safe
        return mark_safe('<img src="{url}" width="75px" height="auto" style="border:1px solid #cccccc;" />'.format(
            url = obj.slider_image.url,
            )
        )

    def changelist_view(self, request, extra_context=None):
        if len(request.GET) == 0:
            get_param = "status__exact=active"
            return redirect("{url}?{get_parms}".format(url=request.path, get_parms=get_param))
        return super(HomePageSliderAdmin, self).changelist_view(request, extra_context=extra_context)

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user# company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self,request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)
        
        country = form.base_fields["country"]
        sliders_category = form.base_fields["sliders_category"]

        country.widget.can_add_related = False
        country.widget.can_delete_related = False
        country.widget.can_change_related = False

        sliders_category.widget.can_add_related = False
        sliders_category.widget.can_delete_related = False
        sliders_category.widget.can_change_related = False

        return form


class HomePageAdvertiseAdmin(admin.ModelAdmin):
    list_display = ('id', 'ads_category', 'country', 'advertise_name', 'advertise_summary', 'image_thumbnail', 'status')
    list_display_links = ('id', 'ads_category', 'advertise_name')

    list_filter = ['status',]

    readonly_fields = ["thumbnails",]


    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = HomePageAdvertise.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = HomePageAdvertise.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view


    def thumbnails(self, obj):
        from django.utils.html import mark_safe
        return mark_safe('<img src="{url}" width="75px" height="auto" style="border:1px solid #cccccc;" />'.format(
            url = obj.ads_image.url,
            )
        )

    def changelist_view(self, request, extra_context=None):
        if len(request.GET) == 0:
            get_param = "status__exact=active"
            return redirect("{url}?{get_parms}".format(url=request.path, get_parms=get_param))
        return super(HomePageAdvertiseAdmin, self).changelist_view(request, extra_context=extra_context)

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user# company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self,request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)
        
        country = form.base_fields["country"]
        ads_category = form.base_fields["ads_category"]

        country.widget.can_add_related = False
        country.widget.can_delete_related = False
        country.widget.can_change_related = False

        ads_category.widget.can_add_related = False
        ads_category.widget.can_delete_related = False
        ads_category.widget.can_change_related = False

        return form


class PrivacypolicyAdmin(RemoveAdminDefaultMessageMixin, admin.ModelAdmin):
    list_display = ('id', 'privacypolicy_name', 'country', 'privacy_policy_details', 'image_thumbnail', 'status')
    list_display_links = ('id', 'privacypolicy_name')


    readonly_fields = ["thumbnails",]
    
    def thumbnails(self, obj):
        from django.utils.html import mark_safe
        return mark_safe('<img src="{url}" width="75px" height="auto" style="border:1px solid #cccccc;" />'.format(
            url = obj.upload_image.url,
            )
        )

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Privacypolicy.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Privacypolicy.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view


    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user# company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self,request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)
        
        country = form.base_fields["country"]

        country.widget.can_add_related = False
        country.widget.can_delete_related = False
        country.widget.can_change_related = False

        return form

    def save_model(self, request, obj, form, change):
        if obj.status == 'active':
            item = Privacypolicy.objects.filter(status ='active')
            if item:
                if item[0].id == obj.id:
                    super().save_model(request, obj, form, change)
                    messages.success(request, "Record changed successfully.")
                else:
                    messages.warning(request, "Active record already exists")
            else:
                super().save_model(request, obj, form, change)
                messages.success(request, "Record added successfully.")
        else:
            super().save_model(request, obj, form, change)
            messages.success(request, "Record added/changed successfully.")


class DisclaimerAdmin(RemoveAdminDefaultMessageMixin, admin.ModelAdmin):
    list_display = ('id', 'disclaimer_name', 'country', 'disclaimer_details_view', 'image_thumbnail', 'status')
    list_display_links = ('id', 'disclaimer_name')

    readonly_fields = ["thumbnails",]
    
    def thumbnails(self, obj):
        from django.utils.html import mark_safe
        return mark_safe('<img src="{url}" width="75px" height="auto" style="border:1px solid #cccccc;" />'.format(
            url = obj.upload_image.url,
            )
        )

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Disclaimer.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Disclaimer.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view


    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user# company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self,request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)
        
        country = form.base_fields["country"]

        country.widget.can_add_related = False
        country.widget.can_delete_related = False
        country.widget.can_change_related = False

        return form

    def save_model(self, request, obj, form, change):
        if obj.status == 'active':
            item = Disclaimer.objects.filter(status ='active')
            if item:
                if item[0].id == obj.id:
                    super().save_model(request, obj, form, change)
                    messages.success(request, "Record changed successfully.")
                else:
                    messages.warning(request, "Active record already exists")
            else:
                super().save_model(request, obj, form, change)
                messages.success(request, "Record added successfully.")
        else:
            super().save_model(request, obj, form, change)
            messages.success(request, "Record added/changed successfully.")


class TermsAdmin(RemoveAdminDefaultMessageMixin, admin.ModelAdmin):
    list_display = ('id', 'terms_name', 'country', 'terms_conditions_details', 'image_thumbnail', 'status')
    list_display_links = ('id', 'terms_name')

    readonly_fields = ["thumbnails",]
    
    def thumbnails(self, obj):
        from django.utils.html import mark_safe
        return mark_safe('<img src="{url}" width="75px" height="auto" style="border:1px solid #cccccc;" />'.format(
            url = obj.upload_image.url,
            )
        )

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Terms.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Terms.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view


    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user# company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self,request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)
        
        country = form.base_fields["country"]

        country.widget.can_add_related = False
        country.widget.can_delete_related = False
        country.widget.can_change_related = False

        return form

    def save_model(self, request, obj, form, change):
        if obj.status == 'active':
            item = Terms.objects.filter(status ='active')
            if item:
                if item[0].id == obj.id:
                    super().save_model(request, obj, form, change)
                    messages.success(request, "Record changed successfully.")
                else:
                    messages.warning(request, "Active record already exists")
            else:
                super().save_model(request, obj, form, change)
                messages.success(request, "Record added successfully.")
        else:
            super().save_model(request, obj, form, change)
            messages.success(request, "Record added/changed successfully.")


class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'contactno', 'email', 'message', 'response_summary', 'image', 'query_status')
    list_display_links = ('id', 'fullname')

    readonly_fields = ['fullname', 'contactno', 'email', 'message']

    # def has_delete_permission(self, request, obj=None):
    #     return False


    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Enquiry.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Enquiry.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view


    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user# company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self,request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)
        
        query_status = form.base_fields["query_status"]

        query_status.widget.can_add_related = False
        query_status.widget.can_delete_related = False
        query_status.widget.can_change_related = False

        return form


class FaqAdmin(admin.ModelAdmin):
    list_display = ('id', 'faq_name', 'country', 'faq_details', 'status')
    list_display_links = ('id', 'faq_name')

    # def has_delete_permission(self, request, obj=None):
    #     return False


    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Faq.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Faq.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view


    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user# company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self,request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)
        
        country = form.base_fields["country"]

        country.widget.can_add_related = False
        country.widget.can_delete_related = False
        country.widget.can_change_related = False

        return form


class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'country', 'customer_feedback', 'image_thumbnail', 'status')
    list_display_links = ('id', 'customer_name')

    readonly_fields = ["thumbnails",]


    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Testimonials.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Testimonials.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view


    def thumbnails(self, obj):
        from django.utils.html import mark_safe
        return mark_safe('<img src="{url}" width="75px" height="auto" style="border:1px solid #cccccc;" />'.format(
            url = obj.customer_image.url,
            )
        )

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user# company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self,request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)
        
        country = form.base_fields["country"]

        country.widget.can_add_related = False
        country.widget.can_delete_related = False
        country.widget.can_change_related = False

        return form


class PaymentOptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code_name', 'associated_company', 'status')
    list_display_links = ('id', 'name', 'associated_company')

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = UiConfiguration.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = UiConfiguration.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view


class UiConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_display_in_row', 'item_display', 'paymentoption', 'enable', 'status')
    list_display_links = ('id', 'item_display_in_row', 'item_display')

    filter_horizontal = ('paymentoptions',)

    # def has_delete_permission(self, request, obj=None):
    #     return False


    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = UiConfiguration.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = UiConfiguration.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view


    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])

        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]

        if not obj.created_by:
            obj.created_by = request.user
        else:
            obj.changed_by = request.user
        obj.save()


admin.site.register(AboutUs, AboutUsAdmin)
# admin.site.register(Company, CompanyAdmin)
admin.site.register(HomePageSlider, HomePageSliderAdmin)
admin.site.register(Homevideo, HomevideoAdmin)
admin.site.register(HomePageAdvertise, HomePageAdvertiseAdmin)
admin.site.register(Privacypolicy, PrivacypolicyAdmin)
admin.site.register(Disclaimer, DisclaimerAdmin)
admin.site.register(Terms, TermsAdmin)
admin.site.register(Enquiry, EnquiryAdmin)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Testimonials, TestimonialsAdmin)
admin.site.register(PaymentOptions, PaymentOptionsAdmin)
admin.site.register(UiConfiguration, UiConfigurationAdmin)