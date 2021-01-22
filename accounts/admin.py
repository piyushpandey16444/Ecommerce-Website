from django.contrib import admin
from django_tabbed_changeform_admin.admin import DjangoTabbedChangeformAdmin
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from hoitymoppet.models import *


class ProfileDetailInline(admin.TabularInline):
    model = Address
    extra = 2
    classes = ["tab-address-inline"]
    fields = (('name','mobile_no','pincode','locality','address','city','user_state', 'user_country', 'landmark', 'alternate_no'))
    readonly_fields = ['name','mobile_no','pincode','locality','address','city','user_state', 'user_country', 'landmark', 'alternate_no']

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def has_add_permission(self, request, obj=None):
        return False


class ProfileChildInline(admin.TabularInline):
    model = Child
    extra = 2
    classes = ["tab-child-inline"]
    fields = ('child_birth_date','child_name')
    readonly_fields = ['child_name','child_birth_date']

    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


class ProfileOrderInline(admin.TabularInline):
    model = OrderDetail
    extra = 2
    classes = ["tab-order-inline"]
    fields = ('order_id', 'product_id', 'image', 'product_age', 'user_custom_size_master', 'color', 'quantity', 'price', 'total_price')
    readonly_fields = ['order_id', 'product_id', 'image', 'product_age', 'user_custom_size_master', 'color', 'quantity', 'price', 'total_price']

    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


class ProfileUserCustomMeasuresMasterInline(admin.TabularInline):
    model = UserCustomMeasuresMaster
    extra = 2
    classes = ["tab-usercustommeasuresmaster-inline"]
    fields = ('id', 'user_custom_size_name', 'user', 'age', 'status',)
    readonly_fields = ['id', 'user_custom_size_name', 'user', 'age', 'status',]

    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


class ProfileUserCartInline(admin.TabularInline):
    model = UserCart
    extra = 2
    classes = ["tab-usercart-inline"]
    fields = ('user', 'product_id', 'image', 'product_age', 'user_custom_size_master', 'color', 'quantity', 'get_total_discount_item_price', 'create_date', 'modified_date',)
    readonly_fields = ['user', 'product_id', 'image', 'product_age', 'user_custom_size_master', 'color', 'quantity', 'get_total_discount_item_price', 'create_date', 'modified_date',]

    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


class ProfileAdmin(DjangoTabbedChangeformAdmin,admin.ModelAdmin):
    # list_display =('id', 'user', 'email', 'first_name', 'last_name', 'user_contact_number', 'user_sex', 'address', 'childs', 'action_field',)
    # readonly_fields = ['id', 'user', 'email', 'first_name', 'last_name', 'user_contact_number', 'user_sex', 'address', 'childs', 'action_field', 'pancard_name','pancard_number','aadharcard_name', 'aadharcard_number']

    list_display =('id', 'user', 'email', 'first_name', 'last_name', 'order_count', 'user_contact_number', 'user_sex',)
    readonly_fields = ['id', 'user', 'email', 'first_name', 'last_name', 'order_count', 'user_contact_number', 'user_sex', 'pancard_name','pancard_number','aadharcard_name', 'aadharcard_number']
    list_display_links = ('id', 'user', 'email')

    # list_filter = ['user', 'first_name', 'last_name',]


    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Profile.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Profile.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view


    change_form_template = "admin/accounts/profile/change_form.html"
    inlines = [ProfileDetailInline, ProfileChildInline, ProfileOrderInline, ProfileUserCustomMeasuresMasterInline, ProfileUserCartInline]

    def order_count(self, request):
        q = User.objects.all().filter(username=request).first()
        # print(q.id)
        queryset = Order.objects.filter(user_id=q.id).count()
        # print(queryset)
        return queryset

    def action_field(self, obj=None):
        from django.utils.html import format_html
        from django.utils.html import mark_safe
        # return mark_safe('obj.email')
        return format_html(
            # "<button data-toggle='modal' data-target='#myModal' class='btn btn-primary btn-sm'>Details</button>",
            # "<button onclick='doSomething({})' data-toggle='modal' data-target='#myModal' class='btn btn-primary btn-sm'>Details</button>",
            # "<button onclick='return showAddAnotherPopup(this);' class='btn btn-primary btn-sm'>Details</button>",
            "<a href='{}' data-toggle='modal' data-target='#myModal' class='btn btn-primary btn-sm' style='color:#ffffff;'>Details</a>",
            obj.id, 
            obj.email,
            template = 'hoitymoppet/details.html'
        )

    def has_add_permission(self, request, obj=None):
        return False

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

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': False,
            'show_save_and_continue': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def get_queryset(self, request):
        customers = User.objects.filter(is_superuser=False)
        customers_list = []
        if customers:
            for user in customers:
                customers_list.append(user.id)
        return self.model.objects.filter(user__in = customers_list)


    # convert all fields in tabs
    fieldsets = [
        (None, {
            "fields": ["user", "email", "first_name", "last_name", "user_contact_number", "user_sex", ],
            "classes": ["tab-first"],
        }),
    ]

    tabs = [
        ("General Info", ["tab-first"]),
        ("Address Info", ["tab-address-inline"]),
        ("Childs Info", ["tab-child-inline"]),
        ("Orders Info", ["tab-order-inline"]),
        ("User Custom Sizes", ["tab-usercustommeasuresmaster-inline"]),
        ("Customer Cart", ["tab-usercart-inline"]),
    ]
    # End


class Employee(Profile):
    class Meta:
        proxy = True


class EmployeeAdmin(ProfileAdmin):
    def get_queryset(self, request):
        admin_users = User.objects.filter(is_superuser=True)
        admin_user_id_list = []
        if admin_users:
            for user in admin_users:
                admin_user_id_list.append(user.id)
        return self.model.objects.filter(user__in = admin_user_id_list)


class AddressAdmin(admin.ModelAdmin):
    list_display =('id','user','name','mobile_no','pincode','locality','address','city','user_state', 'user_country', 'landmark','alternate_no', 'profile', 'default')
    # list_display_links = ('id', 'user', 'name')
    readonly_fields = ['id', 'user', 'name', 'mobile_no', 'pincode', 'locality', 'address', 'city', 'user_state', 'user_country', 'landmark','alternate_no', 'profile']

    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Address.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Address.objects.filter(associated_company_id=company_id[0].id)
    #     return list_view


    def save_model(self, request, obj, form, change):
        # company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
        # 
        # if not obj.associated_company:
        #     obj.associated_company = company_id[0]
        # 
        # if not obj.created_by:
        #     obj.created_by = request.usercompany_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
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


class ChildAdmin(admin.ModelAdmin):
    list_display  = ('id','user','child_name','child_birth_date', 'profile')
    # list_display_links = ('id', 'user')
    readonly_fields = ['id','user','child_name','child_birth_date', 'profile']


    def has_add_permission(self, request, obj=None):
        return False


    # def get_queryset(self, request):
    #     if 'associated_company__exact' in request.GET and request.GET.get('associated_company__exact'):
    #         company = request.GET.get('associated_company__exact')[0]
    #         list_view = Child.objects.filter(associated_company_id=int(company))
    #     else:
    #         if 'company' in request.session:
    #             print("The value of the company issssssssssssssssss", request.session['company'])
    #             company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #             list_view = Child.objects.filter(associated_company_id=company_id[0].id)
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
        #     obj.created_by = request.usercompany_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
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




# Piyush: code for adding currency model in admin on 07-10-2020
class HoityCurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'symbol', 'currency_unit_label', 'currency_subunit_label', 'migrate_data', 'status',)
    list_display_links = ('id', 'name')

    # def has_delete_permission(self, request, obj=None):
    #     return False
# Piyush: code for adding currency model in admin on 07-10-2020 ends here


# Piyush: code for adding currency rate model in admin on 07-10-2020
class HoityCurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'currency_id', 'rate', 'company_id', 'migrate_data',)
    list_display_links = ('id', 'name')

    # def has_delete_permission(self, request, obj=None):
    #     return False
# Piyush: code for adding currency rate model in admin on 07-10-2020 ends here


# Piyush: code for adding country model in admin on 07-10-2020
class HoityCountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'currency_id', 'code', 'phone_code', 'migrate_data', 'reference_id')
    list_display_links = ('id', 'name',)

    # def has_delete_permission(self, request, obj=None):
    #     return False
# Piyush: code for adding country model in admin on 07-10-2020 ends here


# Piyush: code for adding country model in admin on 07-10-2020
class HoityStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'country_id', 'migrate_data',)
    list_display_links = ('id', 'name')

    # def has_delete_permission(self, request, obj=None):
    #     return False
# Piyush: code for adding country model in admin on 07-10-2020 ends here


# Piyush: code for email description on 28-10-2020
class EmailDescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject', 'email_description', 'reference_id', 'migrate_data')
    list_display_links = ('id', 'name', 'subject')
# code ends here


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Child, ChildAdmin)
# Piyush: code for adding currency in admin 
admin.site.register(HoityCurrency, HoityCurrencyAdmin)
admin.site.register(HoityCurrencyRate, HoityCurrencyRateAdmin)
admin.site.register(HoityCountry, HoityCountryAdmin)
admin.site.register(HoityState, HoityStateAdmin)
admin.site.register(EmailDescription, EmailDescriptionAdmin)
