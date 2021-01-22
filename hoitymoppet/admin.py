from django.contrib import admin
from django.shortcuts import redirect
from django_tabbed_changeform_admin.admin import DjangoTabbedChangeformAdmin
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.auth.models import User, Associated_Company
from .models import *
from easy_select2 import select2_modelform
from vali.decorator import vali_models_group

admin.site.site_header = 'Hoitymoppet Admin'

@vali_models_group('Product Master')
class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'color_name', 'color_published', 'patent_color_published',)
    list_display_links = ('id', 'color_name')

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Color.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Color.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        parent_color = form.base_fields["parent_color"]
        associated_company = form.base_fields["associated_company"]

        parent_color.widget.can_add_related = False
        parent_color.widget.can_delete_related = False
        parent_color.widget.can_change_related = False

        associated_company.widget.can_add_related = False
        associated_company.widget.can_delete_related = False
        associated_company.widget.can_change_related = False

        return form


@vali_models_group('Product Master')
class FabricAdmin(admin.ModelAdmin):
    list_display = ('id', 'fabric', 'fabric_detail', 'status')
    list_display_links = ('id', 'fabric')

    ordering = ['-id']

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Fabric.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Fabric.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        associated_company = form.base_fields["associated_company"]

        associated_company.widget.can_add_related = False
        associated_company.widget.can_delete_related = False
        associated_company.widget.can_change_related = False

        return form


@vali_models_group('Product Master')
class StylesAdmin(admin.ModelAdmin):
    list_display = ('id', 'style_name', 'parent_style', 'status')
    list_display_links = ('id', 'style_name')

    ordering = ['-id']

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Styles.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Styles.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        associated_company = form.base_fields["associated_company"]
        parent_style = form.base_fields["parent_style"]

        associated_company.widget.can_add_related = False
        associated_company.widget.can_delete_related = False
        associated_company.widget.can_change_related = False

        parent_style.widget.can_add_related = False
        parent_style.widget.can_delete_related = False
        parent_style.widget.can_change_related = False

        return form


# class CategoriesAdmin(admin.ModelAdmin):
#     list_display = ('id','category', 'parent_category', 'create_date', 'country', 'associated_company', 'image_thumbnail', 'status')
#     list_display_links = ('id', 'category',)

#     ordering = ['-id']

#     exclude = ('associated_company',)

#     # def has_delete_permission(self, request, obj=None):
#     #     return False


#     # def get_queryset(self, request):
#     #     qs = super(CategoriesAdmin,self).get_queryset(request)
#     #     if request.user.is_superuser:
#     #         print("associated companyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy", request.user.associated_company.all())
#     #         print("default companyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy", request.user.default_company)
#     #         rq = ([str(p) for p in request.user.associated_company.all()])
#     #         return qs.filter(associated_company__associated_company_name__in=rq)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'parent_category', 'country', 'image_thumbnail', 'associated_company', 'invisible', 'status')
    list_display_links = ('id', 'category')
    list_filter = ('category', 'status')

    ordering = ['-id']

    readonly_fields = ["thumbnails", ]

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Categories.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Categories.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def thumbnails(self, obj):
        from django.utils.html import mark_safe
        return mark_safe('<img src="{url}" width="75px" height="auto" style="border:1px solid #cccccc;" />'.format(
            url=obj.category_image.url,
        )
        )

    # def changelist_view(self, request, extra_context=None):
    #     referrer = request.META.get('HTTP_REFERER', '')
    #     get_param = "status__exact=active"
    #     if len(request.GET) == 0 and '?' not in referrer:
    #         return redirect("{url}?{get_parms}".format(url=request.path, get_parms=get_param))
    #     return super(CategoriesAdmin,self).changelist_view(request, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        if len(request.GET) == 0:
            get_param = "status__exact=active"
            return redirect("{url}?{get_parms}".format(url=request.path, get_parms=get_param))
        return super(CategoriesAdmin, self).changelist_view(request, extra_context=extra_context)

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     return super(CategoriesAdmin,self).get_queryset(request).filter(status="active")

    # default_filters = ("status='active'",)

    # def get_queryset(self, request):
    #     qs = super(CategoriesAdmin, self).get_queryset(request)
    #     return qs.filter(status='active')

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        parent_category = form.base_fields["parent_category"]
        associated_company = form.base_fields["associated_company"]
        country = form.base_fields["country"]

        parent_category.widget.can_add_related = False
        parent_category.widget.can_delete_related = False
        parent_category.widget.can_change_related = False

        associated_company.widget.can_add_related = False
        associated_company.widget.can_delete_related = False
        associated_company.widget.can_change_related = False

        country.widget.can_add_related = False
        country.widget.can_delete_related = False
        country.widget.can_change_related = False

        return form

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "associated_company":
    #         kwargs["queryset"] = Associated_Company.objects.filter(associated_company_name=request.user.default_company)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # def get_queryset(self, request):
    #     qs = super(CategoriesAdmin,self).get_queryset(request)
    #     if request.user.is_superuser:
    #         # print(request.user.default_company)
    #         # rq = ([str(p) for p in request.user.associated_company.all()])
    #         # print(rq)
    #         return qs.filter(associated_company=request.user.default_company)
    #         # return qs.filter(associated_company__associated_company_name__in=rq)
    #         # return qs.filter(associated_company__id__in=[rq]) 


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'currency', 'country_code',)
    list_display_links = ('id', 'country',)

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Country.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Country.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    # exclude = ('country_name',)

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()


class CurrencycodeAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'currency_name', 'base_currency', 'conversion_rate', 'currency_symbol', 'currency_abbreviation',)
    list_display_links = ('id',)

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Currencycode.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Currencycode.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()


class MeasuresInline(admin.TabularInline):
    model = Measures
    extra = 0
    classes = ["tab-measurements-inline"]


@vali_models_group('Product Master')
class AgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'age', 'associated_company', 'status')
    list_display_links = ('id', 'age')

    ordering = ['-id']

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Age.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Age.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    inlines = [MeasuresInline]

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        associated_company = form.base_fields["associated_company"]

        associated_company.widget.can_add_related = False
        associated_company.widget.can_delete_related = False
        associated_company.widget.can_change_related = False

        return form


@vali_models_group('Product Master')
class MeasurementsAdmin(admin.ModelAdmin):
    list_display = ('id', 'measurement', 'user', 'age', 'shoulder_to_apex', 'status')
    list_display_links = ('id', 'measurement')

    ordering = ['-id']

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Measurements.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Measurements.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()


@vali_models_group('Product Master')
class Measurement_MasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name')

    ordering = ['-id']

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Measurement_Master.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Measurement_Master.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()


@vali_models_group('Product Master')
class MeasuresAdmin(admin.ModelAdmin):
    list_display = ('id', 'age', 'mesure_name', 'value')
    list_display_links = ('id', 'age', 'mesure_name')

    ordering = ['-id']

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Measures.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Measures.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view


    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()


@vali_models_group('Product Master')
class UserCustomMeasuresAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'measures', 'standard_value', 'custom_value', 'custom_measures_master', 'status')
    list_display_links = ('id', 'user')

    ordering = ['-id']

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = UserCustomMeasures.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = UserCustomMeasures.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()


@vali_models_group('Product Master')
class UserCustomMeasuresMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_custom_size_name', 'user', 'age', 'status')
    list_display_links = ('id', 'user_custom_size_name', 'user',)

    ordering = ['-id']

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = UserCustomMeasuresMaster.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = UserCustomMeasuresMaster.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()


class StockdetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'stock', 'status')
    list_display_links = ('id', 'stock')

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Stockdetails.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Stockdetails.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()


class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 2
    classes = ["tab-character-inline"]

    readonly_fields = ["id", "thumbnails"]

    def thumbnails(self, obj):
        from django.utils.html import mark_safe
        return mark_safe('<img src="{url}" width="75px" height="auto" style="border:1px solid #cccccc;" />'.format(
            url = obj.image.url,
            # width=obj.productimage.width,
            # height=obj.productimage.height,
        )
        )


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image', 'image_thumbnail')

    readonly_fields = ["id", "thumbnails"]

    def thumbnails(self, obj):
        from django.utils.html import mark_safe
        return mark_safe('<img src="{url}" width="75px" height="auto" style="border:1px solid #cccccc;" />'.format(
            url=obj.image.url,
            # width=obj.productimage.width,
            # height=obj.productimage.height,
        )
        )


ProductForm = select2_modelform(Product, attrs={'width': '100%'})


@vali_models_group('Product Master')
class ProductAdmin(DjangoTabbedChangeformAdmin, admin.ModelAdmin):
    list_display = (
    'id', 'product_name', 'slug', 'category', 'categories_erp', 'ages', 'product_type', 'item_detail', 'price',
    'image',)
    list_display_links = ('id', 'product_name')

    readonly_fields = ["id", "image_thumbnail", ]

    inlines = [PhotoInline]

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Product.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Product.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def changelist_view(self, request, extra_context=None):
        if len(request.GET) == 0:
            get_param = "status__exact=active"
            return redirect("{url}?{get_parms}".format(url=request.path, get_parms=get_param))
        return super(ProductAdmin, self).changelist_view(request, extra_context=extra_context)

    # save_on_top = True
    # filter_horizontal = ('age', 'color', 'categories', 'relative_product',)
    # raw_id_fields = ('age', 'color', 'categories', 'relative_product',)
    # search_fields = ['product_name', ]
    list_filter = ['categories', 'age', 'price', 'status']

    prepopulated_fields = {'slug': ('product_name',)}

    form = ProductForm

    ordering = ['-id']

    def ages(self, obj):
        return ",".join([str(p.age) for p in obj.age.all()])

    def colors(self, obj):
        from django.utils.html import format_html
        from django.utils.html import mark_safe

        # return "\n".join([str(p.color_name) for p in obj.color.all()])

        color_name = ([str(p.color_name) for p in obj.color.all()])
        color_rgb = ([str(p.color) for p in obj.color.all()])
        new_dict = dict(zip(color_name, color_rgb))

        res = format_html("\n ".join((
                                     "{} <div style='background:{};width:12px;height:12px;border-radius:100%;display:inline-block;border:1px solid #999999;'>&nbsp;</div>,".format(
                                         *i) for i in new_dict.items())))
        return res

        # return "%s %s" % ([str(p.color_name) for p in obj.color.all()], [str(p.color) for p in obj.color.all()])

    def categories(self, obj):
        return "\n".join([p.categories for p in obj.categories.all()])

    def save_model(self, request, obj, form, change):
        obj.save()
        for afile in request.FILES.getlist('photos_multiple'):
            photos = Photo(product=obj, image=afile)
            photos.save()

    # list_per_page = 10

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def image_thumbnail(self, obj):
        from django.utils.html import mark_safe
        return mark_safe('<img src="{url}" width="75px" height="auto" style="border:1px solid #cccccc;" />'.format(
            url=obj.productimage.url,
            # width=obj.productimage.width,
            # height=obj.productimage.height,
        )
        )

    # convert all fields in tabs
    # jatin added one field shipping_charges
    fieldsets = [
        (None, {
            "fields": ["product_name", "slug", "product_type", "categories", "categories_erp", "shipping_charges",
                       "age", "price", "discount_price", "productimage", "product_fabric", "image_thumbnail"],
            "classes": ["tab-first"],
        }),
        (None, {
            "fields": ["color", "relative_product", "item_detail", "size", "reference_id", "migrate_data",
                       "expected_delivery_date"],
            "classes": ["tab-second"],
        }),
        (None, {
            "fields": ["style", "country", "associated_company", "lookbook_category", "careinstructions", "product_uom"],
            "classes": ["tab-third"],
        }),
        (None, {
            "fields": ["style_code", "stock", "status", "video_file", ],
            "classes": ["tab-fourth"],
        }),
    ]

    tabs = [
        ("Basic 1", ["tab-first"]),
        ("Basic 2", ["tab-second"]),
        ("Basic 3", ["tab-third"]),
        ("Basic 4", ["tab-fourth"]),
        ("Upload More Photos", ["tab-character-inline"]),
    ]

    # End

    def get_form(self, request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)

        product_type = form.base_fields["product_type"]
        categories = form.base_fields["categories"]
        categories_erp = form.base_fields["categories_erp"]

        age = form.base_fields["age"]
        country = form.base_fields["country"]
        associated_company = form.base_fields["associated_company"]
        product_fabric = form.base_fields["product_fabric"]
        size = form.base_fields["size"]
        relative_product = form.base_fields["relative_product"]
        color = form.base_fields["color"]
        style = form.base_fields["style"]
        lookbook_category = form.base_fields["lookbook_category"]
        careinstructions = form.base_fields["careinstructions"]

        product_type.widget.can_add_related = False
        product_type.widget.can_delete_related = False
        product_type.widget.can_change_related = False

        categories.widget.can_add_related = False
        categories.widget.can_delete_related = False
        categories.widget.can_change_related = False

        categories_erp.widget.can_add_related = False
        categories_erp.widget.can_delete_related = False
        categories_erp.widget.can_change_related = False

        age.widget.can_add_related = False
        age.widget.can_delete_related = False
        age.widget.can_change_related = False

        country.widget.can_add_related = False
        country.widget.can_delete_related = False
        country.widget.can_change_related = False

        associated_company.widget.can_add_related = False
        associated_company.widget.can_delete_related = False
        associated_company.widget.can_change_related = False

        product_fabric.widget.can_add_related = False
        product_fabric.widget.can_delete_related = False
        product_fabric.widget.can_change_related = False

        size.widget.can_add_related = False
        size.widget.can_delete_related = False
        size.widget.can_change_related = False

        relative_product.widget.can_add_related = False
        relative_product.widget.can_delete_related = False
        relative_product.widget.can_change_related = False

        color.widget.can_add_related = False
        color.widget.can_delete_related = False
        color.widget.can_change_related = False

        style.widget.can_add_related = False
        style.widget.can_delete_related = False
        style.widget.can_change_related = False

        lookbook_category.widget.can_add_related = False
        lookbook_category.widget.can_delete_related = False
        lookbook_category.widget.can_change_related = False

        careinstructions.widget.can_add_related = False
        careinstructions.widget.can_delete_related = False
        careinstructions.widget.can_change_related = False

        return form

        # def has_delete_permission(self, request, obj=None):
    #     return False


class UserCustomSizeAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'user', 'user_custom_size_name', 'create_date', 'modified_date', 'shoulder_to_apex', 'cap_sleeve_length',
    'short_sleeve_length', 'three_fourth_to_apex', 'full_sleeve_length', 'knee_round')
    list_display_links = ('id', 'user', 'user_custom_size_name')

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = UserCustomSize.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = UserCustomSize.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        user = form.base_fields["user"]

        user.widget.can_add_related = False
        user.widget.can_delete_related = False
        user.widget.can_change_related = False
        return form


class CouponHistoryInline(admin.TabularInline):
    model = CouponHistory
    fields = (('create_date', 'coupon_id', 'order_id', 'user'))
    list_display = ('create_date', 'coupon_id', 'order_id', 'user')
    readonly_fields = ['create_date', 'coupon_id', 'order_id', 'user']

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_add_permission(self, request, obj=None):
    #     return False


class CouponAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'code', 'discount_type', 'discount', 'customers', 'create_date', 'valid_from', 'valid_to', 'active')
    list_display_links = ('id', 'code')

    filter_horizontal = ('customer',)
    readonly_fields = ['create_date']
    # list_filter = ['customer']
    inlines = [CouponHistoryInline]

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        customer = form.base_fields["customer"]

        customer.widget.can_add_related = False
        customer.widget.can_delete_related = False
        customer.widget.can_change_related = False

        return form


class CouponHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'coupon_id', 'order_id', 'user')
    list_display_links = ('id', 'coupon_id', 'order_id', 'user')
    fields = (('coupon_id', 'order_id'), ('user', 'create_date'))
    readonly_fields = ['coupon_id', 'order_id', 'user', 'create_date']
    ordering = ('-order_id',)

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = CouponHistory.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = CouponHistory.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    # def has_delete_permission(self, request, obj=None):
    #     return False


class LookbookcategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'country', 'category_summary', 'image_thumbnail', 'status')
    list_display_links = ('id', 'category_name')

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Lookbookcategories.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Lookbookcategories.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        associated_company = form.base_fields["associated_company"]
        country = form.base_fields["country"]

        associated_company.widget.can_add_related = False
        associated_company.widget.can_delete_related = False
        associated_company.widget.can_change_related = False

        country.widget.can_add_related = False
        country.widget.can_delete_related = False
        country.widget.can_change_related = False

        return form


class LookbookAdmin(admin.ModelAdmin):
    list_display = ('id', 'lookbook_name', 'lookbook_summary', 'lookbook_details')
    list_display_links = ('id', 'lookbook_name')

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Lookbook.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Lookbook.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        associated_company = form.base_fields["associated_company"]

        associated_company.widget.can_add_related = False
        associated_company.widget.can_delete_related = False
        associated_company.widget.can_change_related = False

        return form


@vali_models_group('Product Master')
class CareinstructionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'cares_name', 'care_instructions_details', 'status')
    list_display_links = ('id', 'cares_name')

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Careinstructions.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Careinstructions.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        associated_company = form.base_fields["associated_company"]

        associated_company.widget.can_add_related = False
        associated_company.widget.can_delete_related = False
        associated_company.widget.can_change_related = False

        return form


@vali_models_group('Product Master')
class ProductsizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'size_name', 'Product_size_details', 'status')
    list_display_links = ('id', 'size_name')

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Productsize.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Productsize.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        associated_company = form.base_fields["associated_company"]

        associated_company.widget.can_add_related = False
        associated_company.widget.can_delete_related = False
        associated_company.widget.can_change_related = False

        return form


@vali_models_group('Product Master')
class ProducttypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name', 'type_details', 'status')
    list_display_links = ('id', 'type_name')

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Producttype.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Producttype.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        associated_company = form.base_fields["associated_company"]

        associated_company.widget.can_add_related = False
        associated_company.widget.can_delete_related = False
        associated_company.widget.can_change_related = False

        return form


class UserCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product_id', 'image', 'product_age', 'user_custom_size_master', 'color', 'quantity',
                    'get_total_discount_item_price', 'create_date', 'modified_date', 'ordered')
    list_display_links = ('id', 'user', 'product_id')

    def has_add_permission(self, request, obj=None):
        return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = UserCart.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = UserCart.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        user = form.base_fields["user"]
        product_id = form.base_fields["product_id"]

        user.widget.can_add_related = False
        user.widget.can_delete_related = False
        user.widget.can_change_related = False

        product_id.widget.can_add_related = False
        product_id.widget.can_delete_related = False
        product_id.widget.can_change_related = False

        return form


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    fields = (
    ('product_id', 'image', 'product_age', 'user_custom_size_master', 'color', 'quantity', 'price', 'total_price'))
    readonly_fields = ['product_id', 'image', 'product_age', 'user_custom_size_master', 'color', 'quantity', 'price',
                       'total_price']

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def has_add_permission(self, request, obj=None):
        return False


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'profile', 'ref_code', 'ordered_date', 'ordered', 'status_name', 'change_status',)
    list_display_links = ('id', 'user', 'profile', 'ref_code',)
    readonly_fields = ['status_name', 'user', 'profile', 'ref_code', 'ordered', 'ordered_date', 'address_id']

    list_filter = ('status_name', 'user',)

    change_form_template = "admin/hoitymoppet/order/change_form.html"
    inlines = [OrderDetailInline]

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Order.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Order.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': False,
            'show_save_and_continue': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    #####abhishek start 27-6-2020 Adding a Change Status Button on Order admin Panel Tree View
    def change_status(self, obj=None):
        from django.utils.html import format_html
        from django.utils.html import mark_safe
        url = '/hoitymoppet/change_status/' + str(obj.id)
        url_button = "<a onclick='return showAddAnotherPopup(this);'  href=" + url + " class='btn btn-primary btn-sm'>Change Status</a>"
        return format_html(
            url_button,
        )
    #####abhishek end 27-6-2020 Adding a Change Status Button on Order admin Panel Tree View


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = (
    'order_id', 'user', 'profile', 'product_id', 'image', 'product_age', 'user_custom_size_master', 'color', 'quantity',
    'ordered_date', 'address', 'price', 'total_price')
    readonly_fields = ['order_id', 'user', 'profile', 'product_id', 'image', 'product_age', 'user_custom_size_master',
                       'color', 'quantity', 'ordered_date', 'address', 'price', 'total_price']

    ordering = ['-id']

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = OrderDetail.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = OrderDetail.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': False,
            'show_save_and_continue': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)


class TrackingStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_id', 'status_name', 'description', 'status_date')
    list_display_links = ('id', 'user', 'order_id')

    ordering = ['-id']

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = TrackingStatus.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = TrackingStatus.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        user = form.base_fields["user"]
        order_id = form.base_fields["order_id"]

        user.widget.can_add_related = False
        user.widget.can_delete_related = False
        user.widget.can_change_related = False

        order_id.widget.can_add_related = False
        order_id.widget.can_delete_related = False
        order_id.widget.can_change_related = False

        return form


class OrderUpdateAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_id', 'update_desc')

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = OrderUpdate.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = OrderUpdate.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        user = form.base_fields["user"]

        user.widget.can_add_related = False
        user.widget.can_delete_related = False
        user.widget.can_change_related = False

        return form


# class DeliveryPlacesAdmin(admin.ModelAdmin):
#     list_display = ('id', 'delivery_place_name', 'pincode')
#     list_display_links = ('id', 'delivery_place_name', 'pincode')


class UserWishListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product_id', 'create_date', 'modified_date')
    list_display_links = ('id', 'user', 'product_id')

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = UserWishList.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = UserWishList.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        user = form.base_fields["user"]
        product_id = form.base_fields["product_id"]

        user.widget.can_add_related = False
        user.widget.can_delete_related = False
        user.widget.can_change_related = False

        product_id.widget.can_add_related = False
        product_id.widget.can_delete_related = False
        product_id.widget.can_change_related = False

        return form


class StatusoptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_name', 'status_summary', 'status')
    list_display_links = ('id', 'status_name')

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Statusoption.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Statusoption.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()


class SavedCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'card_holder_name', 'card_no', 'expiry_month', 'expiry_year')
    list_display_links = ('id', 'user', 'card_holder_name')

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = SavedCard.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = SavedCard.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        user = form.base_fields["user"]

        user.widget.can_add_related = False
        user.widget.can_delete_related = False
        user.widget.can_change_related = False

        return form


class UserQueriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_id', 'query_summary', 'query_details', 'solution', 'query_status')
    list_display_links = ('id', 'user')

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = UserQueries.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = UserQueries.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        user = form.base_fields["user"]
        query_status = form.base_fields["query_status"]

        user.widget.can_add_related = False
        user.widget.can_delete_related = False
        user.widget.can_change_related = False

        query_status.widget.can_add_related = False
        query_status.widget.can_delete_related = False
        query_status.widget.can_change_related = False

        return form


class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    readonly_fields = ('action_time',)
    # list_filter = ['user', 'content_type']
    # search_fields = ['object_repr', 'change_message']
    list_display = ['__str__', 'content_type', 'action_time', 'user', 'object_link']

    # list_per_page = 10

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = obj.object_repr
        else:
            ct = obj.content_type
            try:
                link = mark_safe('<a href="%s">%s</a>' % (
                    reverse('admin:%s_%s_change' % (ct.app_label, ct.model),
                            args=[obj.object_id]),
                    escape(obj.object_repr),
                ))
            # except NoReverseMatch:
            except:
                link = obj.object_repr
        return link

    object_link.admin_order_field = 'object_repr'
    object_link.short_description = 'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')


class RecenltyviewedproductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product_id', 'view_date')
    list_display_links = ('id', 'user')

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Recenltyviewedproducts.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Recenltyviewedproducts.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    ordering = ['-id']

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        user = form.base_fields["user"]
        product_id = form.base_fields["product_id"]

        user.widget.can_add_related = False
        user.widget.can_delete_related = False
        user.widget.can_change_related = False

        product_id.widget.can_add_related = False
        product_id.widget.can_delete_related = False
        product_id.widget.can_change_related = False

        return form


#####abhishek start 30-09-2020
class PaymentReferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'order_no', 'amount', 'address', 'payment_date', 'payment_mode',)
    list_display_links = ('id', 'username', 'order_no', 'amount', 'address', 'payment_date', 'payment_mode',)
    readonly_fields = ['username', 'order_no', 'amount', 'address', 'payment_date', 'payment_mode', ]
    list_filter = ('username', 'order_no', 'payment_mode',)

    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = PaymentReference.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = PaymentReference.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view

    # def has_add_permission(self, request, obj=None):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False

    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.user
        # else:
        #     obj.changed_by = request.user
        obj.save()


#####abhishek end 30-09-2020


# Piyush: code for adding currency model in admin on 07-10-2020
class ResCurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'symbol', 'currency_unit_label', 'currency_subunit_label', 'migrate_data', 'status',)
    list_display_links = ('id', 'name')

    # def has_delete_permission(self, request, obj=None):
    #     return False


# Piyush: code for adding currency model in admin on 07-10-2020 ends here


# Piyush: code for adding currency rate model in admin on 07-10-2020
class ResCurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'currency_id', 'rate', 'company_id', 'migrate_data',)
    list_display_links = ('id', 'name')

    # def has_delete_permission(self, request, obj=None):
    #     return False


# Piyush: code for adding currency rate model in admin on 07-10-2020 ends here


# Piyush: code for adding country model in admin on 07-10-2020
class ResCountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'currency_id', 'code', 'phone_code', 'migrate_data', 'reference_id')
    list_display_links = ('id', 'name',)

    # def has_delete_permission(self, request, obj=None):
    #     return False


# Piyush: code for adding country model in admin on 07-10-2020 ends here


# Piyush: code for adding country model in admin on 07-10-2020
class ResStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'country_id', 'migrate_data',)
    list_display_links = ('id', 'name')

    # def has_delete_permission(self, request, obj=None):
    #     return False


# Piyush: code for adding country model in admin on 07-10-2020 ends here


@vali_models_group('Product Master')
class ProductUomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company_id', 'rounding', 'status', 'migrate_data', 'reference_id')
    list_display_links = ('id', 'name', 'company_id')

    # def has_delete_permission(self, request, obj=None):
    #     return False


# JAtin :code for shipping charges
@vali_models_group('Product Master')
class ShippingChargesAdmin(admin.ModelAdmin):
    list_display = ('id', 'associated_company', 'free_order_value', 'charge_type', 'max_charge', 'specific_charge')
    list_display_links = ('id', 'associated_company')
# Jatin code end


class BackgroundImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'associated_company', 'image_thumbnail', 'video', 'status')
    list_display_links = ('id', 'item', 'associated_company',)
    
    # def has_delete_permission(self, request, obj=None):
    #     return False

    readonly_fields = ["thumbnails",]

    def thumbnails(self, obj):
        from django.utils.html import mark_safe
        return mark_safe('<img src="{url}" width="75px" height="auto" style="border:1px solid #cccccc;" />'.format(
            url = obj.image.url,
            )
        )


# Piyush :code for shipping product
@vali_models_group('Product Master')
class ShippingProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_id', 'shipping_charge', 'percentage', 'reference_id', 'migrate_data')
    list_display_links = ('id', 'name', 'product_id', 'shipping_charge', 'percentage', 'reference_id', 'migrate_data')
# code ends here


admin.site.register(Color, ColorAdmin)
admin.site.register(Fabric, FabricAdmin)
admin.site.register(Styles, StylesAdmin)
admin.site.register(Categories, CategoriesAdmin)
# admin.site.register(Country, CountryAdmin)
# admin.site.register(Currencycode, CurrencycodeAdmin)
admin.site.register(Age, AgeAdmin)
# admin.site.register(Measurements, MeasurementsAdmin)
admin.site.register(Measurement_Master, Measurement_MasterAdmin)
admin.site.register(Measures, MeasuresAdmin)
admin.site.register(UserCustomMeasures, UserCustomMeasuresAdmin)
admin.site.register(UserCustomMeasuresMaster, UserCustomMeasuresMasterAdmin)
admin.site.register(Careinstructions, CareinstructionsAdmin)
admin.site.register(Productsize, ProductsizeAdmin)
admin.site.register(Producttype, ProducttypeAdmin)
# admin.site.register(Stockdetails, StockdetailsAdmin)
admin.site.register(Product, ProductAdmin)
# admin.site.register(Lookbookcategories, LookbookcategoriesAdmin)
# admin.site.register(Lookbook, LookbookAdmin)
# admin.site.register(Photo, PhotoAdmin)
admin.site.register(UserCart, UserCartAdmin)
# admin.site.register(UserCustomSize, UserCustomSizeAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(CouponHistory, CouponHistoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderUpdate, OrderUpdateAdmin)
# admin.site.register(DeliveryPlaces, DeliveryPlacesAdmin)
admin.site.register(UserWishList, UserWishListAdmin)
admin.site.register(Statusoption, StatusoptionAdmin)
admin.site.register(UserQueries, UserQueriesAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
# admin.site.register(SavedCard, SavedCardAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(TrackingStatus, TrackingStatusAdmin)
admin.site.register(Recenltyviewedproducts, RecenltyviewedproductsAdmin)
admin.site.register(PaymentReference, PaymentReferenceAdmin)
# Piyush: code for adding currency in admin
# admin.site.register(ResCurrency, ResCurrencyAdmin)
# admin.site.register(ResCurrencyRate, ResCurrencyRateAdmin)
# admin.site.register(ResCountry, ResCountryAdmin)
# admin.site.register(ResState, ResStateAdmin)
admin.site.register(ProductUom, ProductUomAdmin)
admin.site.register(ShippingProduct, ShippingProductAdmin)
# Jatin added for shipping charges
admin.site.register(ShippingCharges, ShippingChargesAdmin)
admin.site.register(BackgroundImage, BackgroundImageAdmin)