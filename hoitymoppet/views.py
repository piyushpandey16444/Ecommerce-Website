from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib import messages
from .forms import UserCustomSizeform, AddressForm, CouponApplyForm
from django.core.paginator import Paginator
from accounts.models import *
from generic_links.models import *
#####abhishek 21-5-2020
from django.http import HttpResponse
#####abhishek 21-5-2020
from django.contrib.auth.models import User
#####abhishek 12-6-2020
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q
#####abhishek 12-6-2020

from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from django.http import HttpResponse
# from django.core.mail import EmailMessage
from mail_templated import EmailMessage

# Piyush: code for import statements for sending mails and apis
from hoitymoppet.serializers import CategoriesSerializer, CompanySerializer, UserSerializer, ProductSerializer, \
    CareinstructionsSerializer, \
    FabricSerializer, ColorSerializer, AgeSerializer, PhotoSerializer, MeasurementSerializer, MeasuresSerializer, \
    ResCurrencySerializer, ResCurrencyRateSerializer, ResCountrySerializer, ResStateSerializer, ProductUomSerializer, \
    AvailableCouponsSerializer, ShippingChargesSerializer, ShippingProductSerializer
from datetime import datetime, timedelta
from django.conf import settings
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import Associated_Company
import xmlrpc.client
import shutil
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from datetime import datetime, timedelta
import json
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt

import ipapi
from des.models import DynamicEmailConfiguration

# P: global var assigned for handling user creation from social login on 05-11-2020
REFERENCE_ID = None
MIGRATE_DATA = False
CREATED_INSTANCE = None


def get_categ_and_subcateg():
    categories = Categories.objects.filter(parent_category=None, status='active', invisible=False)
    categ_dict = {}
    for categ in categories:
        c_list = Categories.objects.filter(parent_category=categ, status='active').values()
        categ_dict[categ] = c_list
    return categ_dict


def sub_category(request, id):
    product_cat = get_object_or_404(Categories, id=id)
    sub_categories = Categories.objects.filter(parent_category=id, status='active')

    display_items = UiConfiguration.objects.filter(status='active')
    videos = Homevideo.objects.filter(status='active')
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter( status='active')
    disclaimer_items = Disclaimer.objects.filter( status='active')
    privacy_items = Privacypolicy.objects.filter( status='active')
    terms_items = Terms.objects.filter( status='active')

    context = {'product_cat':product_cat,'sub_categories':sub_categories, 'company_info':company_info, 'videos': videos, 'display_items':display_items, 
    'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 
    'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()}
    return render(request, "hoitymoppet/sub-category.html", context)


def index(request):
    sliders = HomePageSlider.objects.filter(status='active').order_by('-id')
    advertise = HomePageAdvertise.objects.filter(status='active').order_by('-id')
    categories = Categories.objects.filter(status='active', parent_category=None, invisible=False)
    product_obj = Categories.objects.filter(status='active', invisible=True)
    product_one = None
    if product_obj:
        product_one = Product.objects.filter(status='active', categories=product_obj[0])
    display_items = UiConfiguration.objects.filter(status='active')
    videos = Homevideo.objects.filter(status='active')
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter( status='active')
    disclaimer_items = Disclaimer.objects.filter( status='active')
    privacy_items = Privacypolicy.objects.filter( status='active')
    terms_items = Terms.objects.filter( status='active')
    reference_id_value = REFERENCE_ID
    migrate_data_value = MIGRATE_DATA
    created_instance = CREATED_INSTANCE
    if reference_id_value and created_instance:
        user_obj = User.objects.get(id=created_instance)
        if user_obj:
            user_obj.reference_id = reference_id_value
            user_obj.migrate_data = migrate_data_value
            user_obj.save()
    context = {'company_info':company_info, 'product_one': product_one, 'videos': videos, 'sliders': sliders, 'display_items':display_items, 'advertise':advertise, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'categories':categories, 'child_categ': get_categ_and_subcateg()}
    return render(request, "hoitymoppet/master.html", context)


def category_wise_products(request, id):
    product_cat = get_object_or_404(Categories, id=id)
    products = Product.objects.filter(categories=id, status='active').order_by('-id')
    display_items = UiConfiguration.objects.filter(status='active')
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter( status='active')
    testimonials_items = Testimonials.objects.filter( status='active')
    disclaimer_items = Disclaimer.objects.filter( status='active')
    privacy_items = Privacypolicy.objects.filter( status='active')
    terms_items = Terms.objects.filter( status='active')
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    # Code for on mouse over image on category page 27/04/2020
    prod_photos_all = Photo.objects.filter(product=id)
    # End
    photos = []
    #####abhishek start 7-5-2020
    wishlist_product_user_wise_list = []
    #####abhishek end7-5-2020

    for product in products:
        photos.append({product: Photo.objects.filter(product=product)})
        # prod_photos = Photo.objects.filter(product=product)

        #####abhishek start 7-5-2020
        if request.user.id:
            wishlist_product_user_wise = UserWishList.objects.filter(product_id=product.id, user=request.user)
            if wishlist_product_user_wise:
                wishlist_product_user_wise_list.append(product.id)
        #####abhishek end7-5-2020
    categories = Categories.objects.filter(parent_category=None, status='active', invisible=False)
    categ_dict = {}
    for categ in categories:
        c_list = Categories.objects.filter(parent_category=categ, status='active')
        categ_dict[categ] = c_list
    context = {'product_cat': product_cat, 'products': products, 'company_info':company_info,
               'display_items': display_items, 'categories': categories, 'photos': photos,
               'prod_photos_all': prod_photos_all,
               'child_categ': categ_dict, 'disable_attr': wishlist_product_user_wise_list, 'faq_items': faq_items,
               'testimonials_items': testimonials_items, 'disclaimer_items': disclaimer_items,
               'privacy_items': privacy_items,
               'terms_items': terms_items}
    return render(request, "hoitymoppet/category-wise-products.html", context)


def price_wise_products_low(request, id):
    product_cat = get_object_or_404(Categories, id=id)
    products = Product.objects.filter(categories=id, status='active').order_by('discount_price')
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter( status='active')
    testimonials_items = Testimonials.objects.filter( status='active')
    disclaimer_items = Disclaimer.objects.filter( status='active')
    privacy_items = Privacypolicy.objects.filter( status='active')
    terms_items = Terms.objects.filter( status='active')

    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    photos = []
    for product in products:
        photos.append({product: Photo.objects.filter(product=product)})
    categories = Categories.objects.filter( parent_category=None)
    categ_dict = {}
    for categ in categories:
        c_list = Categories.objects.filter(parent_category=categ)
        categ_dict[categ] = c_list
    context = {'company_info':company_info, 'product_cat': product_cat, 'products': products, 'categories': categories, 'photos': photos,
               'child_categ': categ_dict, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items,
               'privacy_items':privacy_items, 'terms_items':terms_items}
    return render(request, "hoitymoppet/category-wise-products.html", context)


def price_wise_products_high(request, id):
    product_cat = get_object_or_404(Categories, id=id)
    products = Product.objects.filter(categories=id, status='active').order_by('-discount_price')
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter( status='active')
    testimonials_items = Testimonials.objects.filter( status='active')
    disclaimer_items = Disclaimer.objects.filter( status='active')
    privacy_items = Privacypolicy.objects.filter( status='active')
    terms_items = Terms.objects.filter(status='active')

    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    photos = []
    for product in products:
        photos.append({product: Photo.objects.filter(product=product)})
    categories = Categories.objects.filter(parent_category=None)
    categ_dict = {}
    for categ in categories:
        c_list = Categories.objects.filter(parent_category=categ)
        categ_dict[categ] = c_list
    context = {'company_info':company_info, 'product_cat': product_cat, 'products': products, 'categories': categories, 'photos': photos,
               'child_categ': categ_dict, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items,
               'privacy_items':privacy_items, 'terms_items':terms_items}
    return render(request, "hoitymoppet/category-wise-products.html", context)


def price_wise_products_low_twofive(request, id):
    product_cat = get_object_or_404(Categories, id=id)
    products = Product.objects.filter(categories=id, status='active')
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter( status='active')
    privacy_items = Privacypolicy.objects.filter( status='active')
    terms_items = Terms.objects.filter(status='active')

    paginator = Paginator(products, 25)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    photos = []
    for product in products:
        photos.append({product: Photo.objects.filter(product=product)})
    categories = Categories.objects.filter(parent_category=None)
    categ_dict = {}
    for categ in categories:
        c_list = Categories.objects.filter(parent_category=categ)
        categ_dict[categ] = c_list
    context = {'company_info':company_info, 'product_cat': product_cat, 'products': products, 'categories': categories, 'photos': photos,
               'child_categ': categ_dict, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items,
               'privacy_items':privacy_items, 'terms_items':terms_items}
    return render(request, "hoitymoppet/category-wise-products.html", context)


def price_wise_products_low_fivezero(request, id):
    product_cat = get_object_or_404(Categories, id=id)
    products = Product.objects.filter(categories=id, status='active')
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter(status='active')
    privacy_items = Privacypolicy.objects.filter(status='active')
    terms_items = Terms.objects.filter(status='active')

    paginator = Paginator(products, 50)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    photos = []
    for product in products:
        photos.append({product: Photo.objects.filter(product=product)})
    categories = Categories.objects.filter( parent_category=None)
    categ_dict = {}
    for categ in categories:
        c_list = Categories.objects.filter(parent_category=categ)
        categ_dict[categ] = c_list
    context = {'company_info':company_info, 'product_cat': product_cat, 'products': products, 'categories': categories, 'photos': photos,
               'child_categ': categ_dict, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items,
               'privacy_items':privacy_items, 'terms_items':terms_items}
    return render(request, "hoitymoppet/category-wise-products.html", context)


@require_http_methods(['GET'])
def productsearch(request):
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter(status='active')
    privacy_items = Privacypolicy.objects.filter(status='active')
    terms_items = Terms.objects.filter(status='active')

    q = request.GET.get('q')
    if q:
        products = Product.objects.filter(product_name__icontains=q,  status='active')
        return render(request, 'hoitymoppet/search-results.html', {'company_info':company_info, 'products': products, 'query': q, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items,
               'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()})
    return render(request, "hoitymoppet/search-results.html" ,{'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items,
               'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()})


def cart_items_discount_price_total(cart_items):
    total_discount_price = 0.0
    if cart_items:
        for cart in cart_items:
            total_discount_price = total_discount_price + float(cart.get_total_discount_item_price())

    return total_discount_price


# ####abhishek start 28-10-2020 count expected delivery days from cart items
# def cart_items_expected_delivery_days(cart_items):
#     """
#     Expected Delivery Days should be the maximum no in all product expected delivery days
#     """
#     expected_delivery_days = 0
#     list1 = []
#     if cart_items:
#         for cart in cart_items:
#             list1.append(cart.product_id.expected_delivery_date)
#     if list1:
#         expected_delivery_days = max(list1)

#     return expected_delivery_days
# ####abhishek end 28-10-2020 count expected delivery days from cart items


####abhishek start 28-10-2020 count expected delivery days from cart items
def cart_items_expected_delivery_days(cart_items):
    """
    Expected Delivery Days should be the maximum no in all product expected delivery days
    """
    expected_delivery_days = 0
    list1 = []
    if cart_items:
        for cart in cart_items:
            if cart.product_id.expected_delivery_date != None:
                list1.append(cart.product_id.expected_delivery_date)
    if list1:
        expected_delivery_days = max(list1)

    return expected_delivery_days
####abhishek end 28-10-2020 count expected delivery days from cart items


def coupon_apply(request):
    coupon_id = ''
    if request.POST:
        coupon_code = request.POST.get('couponcode')
        # print ("GGGGGGGGGGGGGGGGGGGGG",coupon_code)
        coupon_id_get = Coupon.objects.filter(code=coupon_code)
        # print ("HHHHHHHHHH",coupon_id_get)
        if coupon_id_get:
            coupon_id = str(coupon_id_get[0].id)

    url = '/hoitymoppet/addtocart/' + '?cpn=' + coupon_id
    return redirect(url)


@login_required
def add_to_cart(request):
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter( status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter( status='active')
    privacy_items = Privacypolicy.objects.filter( status='active')
    terms_items = Terms.objects.filter( status='active')

    coupon = ''
    coupon_code = ''
    msg = ''
    coupon_dicount_amt = 0.0

    #####abhishek start 12-6-2020 get coupon code from url sent from addtocart page Apply Button
    items = UserCart.objects.filter(user=request.user)

    date_list = []
    for item in items:
        if item.product_id.expected_delivery_date:
            date_list.append(item.product_id.expected_delivery_date)
    if len(date_list) > 1:
        max_days = max(date_list)
    elif len(date_list) == 1:
        max_days = date_list[0]
    else:
        max_days = None

    # for item in items:
    #     if item.product_size == 'custom-size':
    #         #print("the custom size of item is", item.user_custom_size)
    #         user_custom = item.user_custom_size.split('(')[0].strip()
    #         #print("the final custom size is", user_custom)

    #####abhishek 13-5-2020 Used to calculate sum of discount price
    total_discount_price = cart_items_discount_price_total(items) or 0.0
    subtotal = cart_items_discount_price_total(items) or 0.0
    #####abhishek 13-5-2020 Used to calculate sum of discount price

    #####abhishek start 12-6-2020 get coupon code from url sent from addtocart page Apply Button
    #print ("FFFFFFFFF",request.GET)
    if request.GET:
        if request.GET.get('cpn'):
            coupon = request.GET.get('cpn')
            coupon_id = int(coupon)
            coupon_code_rec = Coupon.objects.filter(id=coupon_id)
            if coupon_code_rec:
                if coupon_code_rec[0].active == True:
                    coupon_code = coupon_code_rec[0].code or ''
                    valid_from = coupon_code_rec[0].valid_from
                    valid_from = datetime.strftime(valid_from, '%Y-%m-%d')
                    valid_from = datetime.strptime(valid_from, '%Y-%m-%d')
                    valid_to = coupon_code_rec[0].valid_to
                    valid_to = datetime.strftime(valid_to, '%Y-%m-%d')
                    valid_to = datetime.strptime(valid_to, '%Y-%m-%d')
                    local_dt = datetime.now()
                    local_dt = datetime.strftime(local_dt, '%Y-%m-%d')
                    local_dt = datetime.strptime(local_dt, '%Y-%m-%d')

                    if valid_from <= local_dt <= valid_to:

                        # Piyush: check for coupon limit
                        zero_check = coupon_code_rec[0].limit_number or False
                        if zero_check != 0:
                            required_user = request.user
                            coupon_limit = coupon_code_rec[0].limit_number
                            no_of_times_coupon_used = CouponHistory.objects.filter(coupon_id=coupon_id,
                                                                                   user=required_user).count()

                            if no_of_times_coupon_used < coupon_limit:

                                # Piyush: check for minimum amount
                                minimum_amount = coupon_code_rec[0].minimum_amount
                                if minimum_amount and minimum_amount <= subtotal:
                                    if coupon_code_rec[0].discount_type == 'Fixed':
                                        coupon_dicount_amt = round(coupon_code_rec[0].discount)
                                    elif coupon_code_rec[0].discount_type == 'Percentage':
                                        coupon_dicount_amt = round((total_discount_price * coupon_code_rec[0].discount) / 100)
                                    subtotal = total_discount_price - coupon_dicount_amt
                                else:
                                    msg = 'Minimum amount is {} for using this coupon !'.format(minimum_amount)
                            else:
                                msg = 'Coupon usage limit reached !'

                        else:
                            # Piyush: check for minimum amount
                            minimum_amount = coupon_code_rec[0].minimum_amount
                            if minimum_amount and minimum_amount <= subtotal:
                                if coupon_code_rec[0].discount_type == 'Fixed':
                                    coupon_dicount_amt = round(coupon_code_rec[0].discount)
                                elif coupon_code_rec[0].discount_type == 'Percentage':
                                    coupon_dicount_amt = round((total_discount_price * coupon_code_rec[0].discount) / 100)
                                subtotal = total_discount_price - coupon_dicount_amt
                            else:
                                msg = 'Minimum amount is {} for using this coupon !'.format(minimum_amount)
                    else:
                        msg = 'Coupon is not between the Valid Date !'
                else:
                    msg = 'Your coupon is not active !'
            else:
                msg = 'Invalid Coupon !'
        else:
            msg = 'Invalid Coupon !'
    messages.info(request, msg)

    return render(request, "hoitymoppet/shopping-cart.html", {'company_info':company_info, 'items': items, 'max_days':max_days, 'coupon_code': coupon_code, 'coupon': coupon,
        'coupon_dicount_amt': format(coupon_dicount_amt,'.2f'), 'total_discount_price': format(total_discount_price,'.2f'), 'subtotal': format(subtotal,'.2f'),
        'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items,
        'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg(), 'available_coupons': available_coupons(request)})


# Piyush: code for available coupon function on 01-10-2020
def available_coupons(request):
    coupons_dict = {}
    coupons_list = []
    new_list = []

    now = timezone.now()

    # append the coupons for all customer is True
    all_customer_coupons = Coupon.objects.filter(all_customer=True, active=True, valid_from__lte=now, valid_to__gte=now)
    for coup in all_customer_coupons:
        new_list.append(coup)
    # getting users
    user = request.user
    # get all the coupons related to this user and active in state
    all_coupons = Coupon.objects.filter(customer=user, active=True)
    # check coupons validity
    date_today = datetime.now().date()
    for dt in all_coupons:
        if (date_today >= dt.valid_from) and (date_today <= dt.valid_to):
            coupons_list.append(dt)
    # adding coupons to the context dict for accessing in the front end
    for coupon in coupons_list:
        req_coupon = Coupon.objects.filter(code=coupon)
        for i in req_coupon:
            new_list.append(i)
    coupons_dict['coupon'] = new_list
    if not new_list:
       messages.info(request, "No coupon available.")

    return coupons_dict
# code ends here


# Cart Functionalities
@login_required
def add_product_to_cart(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product_size = request.POST.get('size', '')
        # print("the value in the product size isssssssssssssssssss", product_size)
        item_in_cart = UserCart.objects.get_or_create(
            user=user,
            product_id=product,
            product_size=product_size,
            user_custom_size=user_custom_size,
            ordered=False
        )
        item_in_cart[0].quantity += 1
        item_in_cart[0].save()
        messages.info(request, "Item added/updated into Cart")
        return redirect("productdetails", product.id)


# @login_required
# def add_product_to_cart_wishlist(request, slug):
#     user = request.user
#     product = get_object_or_404(Product, slug=slug)
#     id = Product.objects.filter(slug = slug)[0].id

#     if request.method == 'POST':
#         size = request.POST.get('size', '')
#         custom_size = request.POST.get('usercustomsizes', '')
#         product_color = request.POST.get('product_color', '')

#         age = Age.objects.filter(age = size.split(" ")[0])
#         custom_size_master = UserCustomMeasuresMaster.objects.filter(user_custom_size_name__iexact = custom_size)

#         if age and custom_size_master:
#             item_in_cart = UserCart.objects.get_or_create(
#                 user=user,
#                 product_id=product,
#                 product_age=age[0],
#                 user_custom_size_master=custom_size_master[0],
#                 product_color=product_color,
#                 ordered=False
#             )
#         else:
#             item_in_cart = UserCart.objects.get_or_create(
#                 user=user,
#                 product_id=product,
#                 product_age=age[0],
#                 product_color=product_color,
#                 ordered=False
#             )
#         item_in_cart[0].quantity += 1
#         item_in_cart[0].save()
#         messages.info(request, "Item added/updated into Cart")

#         # return redirect(request.META.get('HTTP_REFERER'), product.slug)
#     return redirect("productdetails", product.slug)


@login_required
def add_product_to_cart_wishlist(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    id = Product.objects.filter(slug=slug)[0].id

    if request.method == 'POST':
        size = request.POST.get('size', '')
        custom_size = request.POST.get('usercustomsizes', '')
        product_color = request.POST.get('product_color', '')

        age = Age.objects.filter(age=size.split(" ")[0])
        custom_size_master = None
        if custom_size:
            custom_master = UserCustomMeasuresMaster.objects.filter(user_custom_size_name=custom_size, user=request.user)
            if custom_master:
                for req_ag in custom_master:
                    if req_ag.age == age[0]:
                        custom_size_master = req_ag

        pro_color = None
        if product_color:
            pro_color = Color.objects.filter(color__iexact=product_color)[:1]

        if custom_size_master and pro_color:
            item_in_cart = UserCart.objects.get_or_create(
                user=user,
                product_id=product,
                product_age=age[0],
                user_custom_size_master=custom_size_master or None,
                prod_color=pro_color[0] or None,
                ordered=False
            )

        elif pro_color:
            item_in_cart = UserCart.objects.get_or_create(
                user=user,
                product_id=product,
                product_age=age[0],
                prod_color=pro_color[0] or None,
                ordered=False
            )
        else:
            item_in_cart = UserCart.objects.get_or_create(
                user=user,
                user_custom_size_master=custom_size_master or None,
                product_id=product,
                product_age=age[0],
                ordered=False
            )
        item_in_cart[0].quantity += 1
        item_in_cart[0].save()
        messages.info(request, "Item added/updated into Cart")

        # return redirect(request.META.get('HTTP_REFERER'), product.slug)
    # return redirect("productdetails", product.slug)
    return redirect("addtocart")


def delete_product_from_cart(request, id):
    item = get_object_or_404(UserCart, id=id)
    item.delete()
    messages.info(request, "Item removed from your cart.")
    cart_items = UserCart.objects.filter(user=request.user).count()
    request.session['cart_count'] = cart_items
    return redirect('addtocart')


@login_required
def remove_single_item_from_cart(request, id):
    item = get_object_or_404(UserCart, id=id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
        messages.info(request, "The item quantity was updated")
        return redirect("addtocart")
    else:
        item.delete()
        messages.info(request, "This item was removed from your cart.")
        return redirect("addtocart")


@login_required
def add_single_item_from_cart(request, id):
    item = get_object_or_404(UserCart, id=id)
    item.quantity += 1
    item.save()
    messages.info(request, "The item quantity was updated")
    return redirect("addtocart")


def productdetails(request, cat=None, slug=None):
    category_name = ' '
    if cat:
        cat = cat
        category_name = Categories.objects.filter(id=cat)[0]

    # print("the value in the slug is", slug)
    product_details = get_object_or_404(Product, slug=slug)
    id = Product.objects.filter(slug = slug)[0].id

    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter( status='active')
    testimonials_items = Testimonials.objects.filter( status='active')
    disclaimer_items = Disclaimer.objects.filter( status='active')
    privacy_items = Privacypolicy.objects.filter( status='active')
    terms_items = Terms.objects.filter( status='active')

    measure_image = BackgroundImage.objects.filter(item='measureguide', status='active')
    measure_video = BackgroundImage.objects.filter(item='measurevideo', status='active')
    # print("measure_imagewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww", measure_image)

    # For user custom size
    if request.user.is_authenticated:
        items = UserCustomSize.objects.filter(user=request.user)
    else:
        items = {}
    # End

    prod_cat = Categories.objects.all()
    #print("prod_cat ........................", prod_cat)

    # For related products
    if Producttype.objects.filter(product=id):
        relatedprodsall = Producttype.objects.filter(product=id)
        #print("relatedprodsall ............................", relatedprodsall)

        relatedprods = Product.objects.filter(product_type=relatedprodsall[0]).order_by('-id')
        #print("relatedprods ............................", relatedprods)
    else:
        relatedprods = {}
    # End

    # For recently viewed products
    if request.user.is_authenticated:
        current_date = datetime.now()
        previous_date = current_date + relativedelta(months=-4)
        user = request.user
        product = get_object_or_404(Product, id=id)
        if not Recenltyviewedproducts.objects.filter(user=user, product_id=product).exists():
            recently_viewed_products = Recenltyviewedproducts(user=user, product_id=product)
            recently_viewed_products.save()

        recentlyviewed = Recenltyviewedproducts.objects.filter(Q(user= request.user) & Q(view_date__range=[previous_date, current_date])).order_by('-id')
    else:
        recentlyviewed = {}
        #print("items....................")
    # End

    prod_photos = Photo.objects.filter(product=id)
    categories = Categories.objects.filter( parent_category=None)
    # print("categories ........................", categories)
    return render(request, "hoitymoppet/product-details.html", context={'cat':cat, 'category_name':category_name, 'company_info':company_info, 'measure_image': measure_image, 'measure_video': measure_video, 'product_details': product_details, 'relatedprods':relatedprods, 'recentlyviewed': recentlyviewed, 'child_categ': get_categ_and_subcateg(), 'photos':prod_photos, 'items': items, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items})


@login_required
def shop(request):
    products = Product.objects.all()
    colors = Color.objects.all()
    styles = Styles.objects.all()
    categories = Categories.objects.all()
    context = {'products':products, 'colors':colors, 'styles':styles, 'categories':categories}
    return render(request, "hoitymoppet/shop.html", context)


def quickview(request, id):
    product_details = Product.objects.get(id=id)
    return render(request, "hoitymoppet/quickview.html", context={'product_details': product_details})


def productcompare(request):
    return render(request, "hoitymoppet/product-compare.html")


@login_required
def productwishlist(request):
    items = UserWishList.objects.filter(user=request.user)
    usercustomsizes = UserCustomSize.objects.filter(user=request.user)

    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter(status='active')
    privacy_items = Privacypolicy.objects.filter(status='active')
    terms_items = Terms.objects.filter(status='active')

    count = items.count()
    return render(request, "hoitymoppet/product-wishlist.html",{'child_categ': get_categ_and_subcateg(), 'company_info':company_info, 'items': items,
        'usercustomsizes':usercustomsizes, 'count': count, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items,
        'privacy_items':privacy_items, 'terms_items':terms_items})


@login_required
def addWishList(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    id = Product.objects.filter(slug = slug)[0].id

    if not UserWishList.objects.filter(product_id=product, user=request.user).exists():
        cart = UserWishList(user=user, product_id=product)
        cart.save()
    return redirect('productdetails', product.slug)


@login_required()
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    wished_item, created = UserWishList.objects.get_or_create(product_id_id=product.id, user=request.user)
    if created:
        messages.info(request, 'The item is added to your wishlist.')
    else:
        messages.info(request, 'The item is already in your wishlist.')
    # return redirect('category-wise-products', id=4)
    # return redirect(request.META.get('HTTP_REFERER'))
    return redirect('productwishlist')


@login_required()
def add_to_wishlist_item(request, id):
    product = get_object_or_404(Product, id=id)
    wished_item, created = UserWishList.objects.get_or_create(product_id_id=product.id, user=request.user)
    if created:
        messages.info(request, 'The item is added to your wishlist.')
    else:
        messages.info(request, 'The item is already in your wishlist.')
    return redirect('productwishlist')


@login_required
def deleteWishList(request, id):
    item = get_object_or_404(UserWishList, id=id)
    item.delete()
    wishlist_items = UserWishList.objects.filter(user=request.user).count()
    request.session['wishlist_count'] = wishlist_items
    return redirect('productwishlist')


##### abhishek start 26-5-2020 set id as argument and send tracking status into html
@login_required
def tracker(request, id):
    order_id = Order.objects.filter(id=id, user=request.user)

    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter( status='active')
    disclaimer_items = Disclaimer.objects.filter( status='active')
    privacy_items = Privacypolicy.objects.filter( status='active')
    terms_items = Terms.objects.filter( status='active')

    tracking_status = []
    #print ("AAAAAAAAAAAAAAAAA")
    if order_id:
        #print ("BBBBBBBBBBBBBBBB")
        order_id = order_id[0]
        tracking_status = TrackingStatus.objects.filter(order_id=order_id)
        #print ("GGGGGGGGGGG",tracking_status)
    return render(request, "hoitymoppet/tracker.html", {'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 
    'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg(), 'order': order_id, 'tracking_status': tracking_status})


# def hoitymoppetlookbook(request):
#     lookbooks = Lookbook.objects.all()
#     lookbookcategories = Lookbookcategories.objects.all()
#     context = {'lookbooks':lookbooks, 'lookbookcategories':lookbookcategories, 'child_categ': get_categ_and_subcateg()}
#     return render(request, "hoitymoppet/hoitymoppet-look-book.html", context)


def hoitymoppetlookbook(request):
    lookbooks = Lookbookcategories.objects.filter(status='active')
    lookbookcategories = Lookbookcategories.objects.all()

    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter(status='active')
    privacy_items = Privacypolicy.objects.filter(status='active')
    terms_items = Terms.objects.filter(status='active')

    context = {'company_info':company_info, 'lookbooks':lookbooks, 'lookbookcategories':lookbookcategories, 'child_categ': get_categ_and_subcateg(), 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items}
    return render(request, "hoitymoppet/hoitymoppet-look-book.html", context)


def hoitymoppetlookbookdetails(request, id):
    lookbook_cat = get_object_or_404(Lookbookcategories, id=id)
    #print("lookbook_cat ......................", lookbook_cat)

    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter( status='active')
    testimonials_items = Testimonials.objects.filter( status='active')
    disclaimer_items = Disclaimer.objects.filter( status='active')
    privacy_items = Privacypolicy.objects.filter( status='active')
    terms_items = Terms.objects.filter( status='active')

    lookbookdetails = Product.objects.filter(lookbook_category=id, status='active')
    return render(request, "hoitymoppet/hoitymoppet-look-book-details.html", context={'company_info':company_info, 'lookbook_cat':lookbook_cat, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'lookbookdetails': lookbookdetails, 'child_categ': get_categ_and_subcateg()})


@login_required()
def add_to_wishlist_by_lookbook(request, id):
    product = get_object_or_404(Product, id=id)
    wished_item, created = UserWishList.objects.get_or_create(product_id_id=product.id, user=request.user)
    if created:
        messages.info(request, 'The item is added to your wishlist.')
    else:
        messages.info(request, 'The item is already in your wishlist.')
    # return redirect('hoitymoppetlookbookdetails', id=2)
    return redirect(request.META.get('HTTP_REFERER'))


def get_expected_delivery_days(cart_items):
    max_days = None
    date_list = []
    if cart_items:
        for item in cart_items:
            if item.product_id.expected_delivery_date:
                date_list.append(item.product_id.expected_delivery_date)
        if len(date_list) > 1:
            max_days = max(date_list)
        elif len(date_list) == 1:
            max_days = date_list[0]
        else:
            max_days = None
    return max_days


def categorydetails(request, id):
    categorydetails = Product.objects.filter(category=id, status='active')
    return render(request, "hoitymoppet/category-wise-products.html", context={'categorydetails': categorydetails, 'child_categ': get_categ_and_subcateg()})


def ordercompleted(request):
    user = request.user
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter(status='active')
    privacy_items = Privacypolicy.objects.filter(status='active')
    terms_items = Terms.objects.filter(status='active')

    order_detail_list = []
    coupon_discount_amt = 0.0
    product_price = 0.0

    # get address
    address = ''
    generated_order_detail_list = []
    if request.GET and request.GET.get('addr'):
        delivery_address = Address.objects.filter(user=request.user, id=request.GET.get('addr'))
        if delivery_address:
            address = delivery_address[0]

    # create order
    if request.method == 'POST':
        cart_items = UserCart.objects.filter(user=request.user)
        # Piyush: code for expected deliver days om 28-10-2020
        maximum_days = get_expected_delivery_days(cart_items)
        # Piyush: code for expected deliver days om 28-10-2020 ends here
        if cart_items:
            #Jatin:code for shipping charges
            total_discount_price1 = cart_items_discount_price_total(cart_items)
            subtotal1 = cart_items_discount_price_total(cart_items) or 0.0
            ####abhishek start 28-10-2020 count expected delivery days from cart items
            expected_delivery_days = cart_items_expected_delivery_days(cart_items) or 0
            ####abhishek end 28-10-2020 count expected delivery days from cart items
            if request.GET:
                if request.GET.get('cpn'):
                    coupon = request.GET.get('cpn')
                    coupon_id = int(coupon)
                    coupon_code_rec = Coupon.objects.filter(id=coupon_id)
                    if coupon_code_rec:
                        coupon_code = coupon_code_rec[0].code or ''

                        if coupon_code_rec[0].discount_type == 'Fixed':
                            coupon_dicount_amt = round(coupon_code_rec[0].discount)
                        elif coupon_code_rec[0].discount_type == 'Percentage':
                            coupon_dicount_amt = round((total_discount_price1 * coupon_code_rec[0].discount) / 100)
                        subtotal1 = total_discount_price1 - coupon_dicount_amt

            ship_charges=0.0
            shipping_charges = cart_items_shipping_charges(request, cart_items, subtotal1, request.GET.get('addr')) or 0.0
            #print('shipping_charges', shipping_charges)
            if shipping_charges:
                ship_charges = shipping_charges['shipping']
            #Jatin end: code for shipping charges
            #Create Order start
            order_no = str(1).rjust(3, '0')
            prev_created_orders = Order.objects.filter()
            if prev_created_orders:
                order_no = str((len(prev_created_orders) + 1)).rjust(3, '0')
            # ref_code = 'ArkeOrderNo' + str(order_no)
            ref_code = 'HM-' + str(order_no)
            generated_order = Order.objects.create(
                user=user,
                ref_code=ref_code,
                address_id=address,
                status_name='ordered',
                maximum_days=maximum_days,
                expected_delivery_days=expected_delivery_days,
            )
            # Order created
            # if address and generated_order:
            #     address.editable = "false"
            #     address.save()

            # code for creating coupon history if applicable
            if request.GET:
                if request.GET.get('cpn'):
                    coupon_code_rec = Coupon.objects.filter(id=int(request.GET.get('cpn')))
                    if coupon_code_rec:
                        coupon_history = CouponHistory.objects.create(
                            user=user,
                            order_id=generated_order,
                            coupon_id=coupon_code_rec[0],
                        )
            # code for creating coupon history if applicable ends here

            # create order detail
            if generated_order:
                # Create Order Detail and Delete Cart Item one by one after order placed - start
                for cart in cart_items:

                    # check for coupon applicable or not
                    if request.GET and request.GET.get('cpn'):
                        coupon_code_rec = Coupon.objects.filter(id=int(request.GET.get('cpn')))
                        if coupon_code_rec:
                            """
                            Means coupon is applied. Now this coupon value will be subtracted from product price.
                            After that coupon price will be subtacted from total price.
                            """
                            price = cart.product_id.discount_price or cart.product_id.price
                            get_no_of_items = len(cart_items)
                            if coupon_code_rec[0].discount_type == 'Fixed':
                                coupon_discount_amt = round(coupon_code_rec[0].discount)
                            elif coupon_code_rec[0].discount_type == 'Percentage':
                                coupon_discount_amt = round(float(price) * (coupon_code_rec[0].discount / 100))
                            product_price = price - coupon_discount_amt
                    else:
                        product_price = cart.product_id.discount_price or cart.product_id.price
                    # coupon function ends here

                    # create order detail lines here
                    create_order_detail = OrderDetail.objects.create(
                        user=user,
                        order_id=generated_order,
                        product_id=cart.product_id,
                        quantity=cart.quantity,
                        price=product_price,
                        total_price=cart.quantity * product_price,
                        product_age=cart.product_age,
                        user_custom_size_master=cart.user_custom_size_master,
                        prod_color=cart.prod_color,
                    )
                    generated_order_detail_list.append(create_order_detail)
                    cart.delete()
                # Create Order Detail and Delete Cart Item one by one after order placed - end
                #Jatin added code for added shipping charges
                ship_chr=Order.objects.filter(id=generated_order.id)
                for ship in ship_chr:
                    ship.shipping_charges=ship_charges
                    ship.save()

                # Create Tracking Status as Ordered - start
                tracking_status = TrackingStatus.objects.create(
                    user=user,
                    order_id=generated_order,
                    status_name='ordered',
                    description='Order Placed'
                )
                # Piyush: code for making description dynamic on 28-10-2020
                description = EmailDescription.objects.filter(subject='order_received').first()
                subject = "Your order has been Received. " + generated_order.ref_code
                # Piyush: code for making description dynamic on 28-10-2020 ends here passed in message
                # Create Tracking Status as Ordered - end
                current_site = get_current_site(request)

                # get default name and number 28-10-2020
                req_username = request.user.email.split("@")[0]
                name = ''
                if request.user.first_name and request.user.last_name:
                    name = request.user.first_name + " " + request.user.last_name
                elif request.user.first_name:
                    name = request.user.first_name
                else:
                    name = req_username
                placed_on = generated_order.ordered_date.date()
                # Piyush: code for getting shipping charges on 19dec
                price_total = 0.0
                if generated_order:
                    order_details = OrderDetail.objects.filter(order_id=generated_order.id)
                    if order_details:
                        for detail in order_details:
                            price_total += detail.total_price
                        if ship_charges:
                            price_total += ship_charges
                # Piyush: code for getting shipping charges on 19dec ends here
                message = {
                    'user': user,
                    'placed_on': placed_on,
                    'name': name,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'generated_order': generated_order,
                    'generated_order_detail_list': generated_order_detail_list,
                    'BASE_URL': settings.BASE_URL,
                    'order_detail_list': order_detail_list,
                    'address': address,
                    'description': description,
                    'subject': subject,
                    'ship_charges': ship_charges,
                    # 'token': account_activation_token.make_token(user),
                    'price_total': price_total,
                }
                config = DynamicEmailConfiguration.get_solo()
                # current_user = User.objects.get(id=request.user.id)
                # email from company 17-11-2020
                current_company = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
                company_email = config.from_email
                if current_company and current_company[0].email:
                    company_email = current_company[0].email
                to_email = user.email
                email = EmailMessage('etemplate/acc_activate_email.tpl', message, "Do not reply <{}>".format(config.from_email), bcc=[company_email],
                                     to=[to_email])
                email.send()

                return render(request, "hoitymoppet/order-completed.html",
                              context={'subtotal1': format(subtotal1, '.2f'), 'company_info':company_info, 'generated_order': generated_order, 'address': address, 'from_cod': 'from_cod',
                                       'generated_order_detail_list': generated_order_detail_list, 'faq_items': faq_items, 'testimonials_items': testimonials_items,
                                       'disclaimer_items': disclaimer_items, 'privacy_items': privacy_items, 'terms_items': terms_items, 'price_total': price_total,
                                       'child_categ': get_categ_and_subcateg()})
        else:
            return HttpResponse("No Item in your Cart !")


#####abhishek start 29-5-2020
def change_status(request, id):
    order_id = Order.objects.get(id=id)
    current_status = order_id and order_id.status_name or ''
    return render(request, "hoitymoppet/change_status.html",
                  context={'order_id': order_id, 'current_status': current_status})


def change_status_done(request, id):
    if request.method == 'POST':
        status_to_change = request.POST.get('status_to_change', '')
        description = request.POST.get('description', '')
        order_id = Order.objects.get(id=id)
        if order_id:
            Order.objects.filter(id=order_id.id).update(status_name=status_to_change)

            tracking_status = TrackingStatus.objects.create(
                user=request.user,
                order_id=order_id,
                status_name=status_to_change,
                description=description,
            )


    # return render(request, "hoitymoppet/change_status.html", context={'order_id': order_id, 'current_status': current_status})
    #####abhishek start 27-6-2020 calling order admin panel tree view from Chenge Status Btn from Order Tree View
    # url = '/admin/hoitymoppet/order/' + str(order_id.id) + '/change/'
    url = '/admin/enquiry_order/order/'
    #####abhishek end 27-6-2020 calling order admin panel tree view from Chenge Status Btn from Order Tree View
    return redirect(url)


#####abhishek end 29-5-2020


def hoitymoppetblog(request):
    return render(request, "hoitymoppet/hoitymoppet-blog.html")


def hoitymoppetblogdetails(request):
    return render(request, "hoitymoppet/hoitymoppet-blog-details.html")


def contactus(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname','')
        contactno = request.POST.get('contactno','')
        email = request.POST.get('email','')
        message = request.POST.get('message','')
        enquiry = Enquiry(fullname=fullname, contactno=contactno, email=email, message=message)
        enquiry.save()
        return render(request, "hoitymoppet/success.html", {'child_categ': get_categ_and_subcateg()})
    return render(request, "hoitymoppet/contact-us.html", {'child_categ': get_categ_and_subcateg()})


def careinstructions(request):
    cares = Careinstructions.objects.all()
    context = {'cares': cares}
    return render(request, "hoitymoppet/care-instructions.html", context, {'child_categ': get_categ_and_subcateg()})


# @login_required
# @csrf_exempt
# def add_user_custom_size(request):
#     if request.is_ajax and request.method == "POST":
#         size = request.POST.get('size_val')
#         size_id = Age.objects.filter(age=size)[0]
#         measure_id = Measurements.objects.filter(age=size_id.id)[0]

#         id = request.POST.get('id')
#         user_custom_size_name = request.POST.get('user_custom_size_name')
#         shoulder_to_apex = request.POST.get('shoulder_to_apex')
#         cap_sleeve_length = request.POST.get('cap_sleeve_length')
#         short_sleeve_length = request.POST.get('short_sleeve_length')
#         three_fourth_to_apex = request.POST.get('three_fourth_to_apex')
#         full_sleeve_length = request.POST.get('full_sleeve_length')
#         knee_round = request.POST.get('knee_round')
#         calf = request.POST.get('calf')
#         ankle_round = request.POST.get('ankle_round')
#         waist_length = request.POST.get('waist_length')
#         neck_round = request.POST.get('neck_round')
#         front_neck_depth = request.POST.get('front_neck_depth')
#         cross_front = request.POST.get('cross_front')
#         bust = request.POST.get('bust')
#         under_bust = request.POST.get('under_bust')
#         waist = request.POST.get('waist')
#         lower_waist = request.POST.get('lower_waist')
#         wrist = request.POST.get('wrist')
#         thigh_round = request.POST.get('thigh_round')
#         lower_thigh = request.POST.get('lower_thigh')
#         arm_hole = request.POST.get('arm_hole')
#         knee_length = request.POST.get('knee_length')
#         full_length = request.POST.get('full_length')
#         shoulder = request.POST.get('shoulder')
#         back_neck_depth = request.POST.get('back_neck_depth')
#         biceps = request.POST.get('biceps')
#         elbow_round = request.POST.get('elbow_round')
#         hips = request.POST.get('hips')
#         bottom_length = request.POST.get('bottom_length')

#         # if not id:
#         if shoulder_to_apex:
#             ucs = {
#                 'user':request.user,
#                 'age':size_id,
#                 'measurements':measure_id,
#                 'user_custom_size_name':user_custom_size_name,
#                 'shoulder_to_apex': shoulder_to_apex,
#                 'cap_sleeve_length':cap_sleeve_length,
#                 'short_sleeve_length':short_sleeve_length,
#                 'three_fourth_to_apex':three_fourth_to_apex,
#                 'full_sleeve_length':full_sleeve_length,
#                 'knee_round':knee_round,
#                 'calf':calf,
#                 'ankle_round':ankle_round,
#                 'waist_length':waist_length,
#                 'neck_round':neck_round,
#                 'front_neck_depth':front_neck_depth,
#                 'cross_front':cross_front,
#                 'bust':bust,
#                 'under_bust':under_bust,
#                 'waist':waist,
#                 'lower_waist':lower_waist,
#                 'wrist':wrist,
#                 'thigh_round':thigh_round,
#                 'lower_thigh':lower_thigh,
#                 'arm_hole':arm_hole,
#                 'knee_length':knee_length,
#                 'full_length':full_length,
#                 'shoulder':shoulder,
#                 'back_neck_depth':back_neck_depth,
#                 'biceps':biceps,
#                 'elbow_round':elbow_round,
#                 'hips':hips,
#                 'bottom_length':bottom_length,
#             }
#             ucsize = UserCustomSize(**ucs)
#             ucsize.save()
#             objs = UserCustomSize.objects.filter(user=request.user)
#             return JsonResponse({'status' : 'success'})

# return render(request, 'hoitymoppet/product-details.html', context={'pusercustomsizes':objs, 'child_categ': get_categ_and_subcateg()})
# return redirect(request.META.get('HTTP_REFERER'), context={'pusercustomsizes':objs, 'child_categ': get_categ_and_subcateg()})

# else:
#     ucsaddr = get_object_or_404(UserCustomSize, id=id)
#     ucsaddr.user_custom_size_name = user_custom_size_name
#     ucsaddr.shoulder_to_apex = shoulder_to_apex
#     ucsaddr.cap_sleeve_length = cap_sleeve_length
#     ucsaddr.short_sleeve_length = short_sleeve_length
#     ucsaddr.three_fourth_to_apex = three_fourth_to_apex
#     ucsaddr.full_sleeve_length = full_sleeve_length
#     ucsaddr.knee_round = knee_round
#     ucsaddr.calf = calf
#     ucsaddr.ankle_round = ankle_round
#     ucsaddr.waist_length = waist_length
#     ucsaddr.neck_round = neck_round
#     ucsaddr.front_neck_depth = front_neck_depth
#     ucsaddr.cross_front = cross_front
#     ucsaddr.bust = bust
#     ucsaddr.under_bust = under_bust
#     ucsaddr.waist = waist
#     ucsaddr.lower_waist = lower_waist
#     ucsaddr.wrist = wrist
#     ucsaddr.thigh_round = thigh_round
#     ucsaddr.lower_thigh = lower_thigh
#     ucsaddr.arm_hole = arm_hole
#     ucsaddr.knee_length = knee_length
#     ucsaddr.full_length = full_length
#     ucsaddr.shoulder = shoulder
#     ucsaddr.back_neck_depth = back_neck_depth
#     ucsaddr.biceps = biceps
#     ucsaddr.elbow_round = elbow_round
#     ucsaddr.hips = hips
#     ucsaddr.bottom_length = bottom_length
#     ucsaddr.save()
#     objs = UserCustomSize.objects.filter(user=request.user)

#     # return render(request, 'hoitymoppet/product-details.html', context={'pusercustomsizes': objs, 'child_categ': get_categ_and_subcateg()})
#     return redirect(request.META.get('HTTP_REFERER'), context={'pusercustomsizes':objs, 'child_categ': get_categ_and_subcateg()})

# objs = UserCustomSize.objects.filter(user=request.user)

# return render(request, 'hoitymoppet/product-details.html', context={'pusercustomsizes': objs, 'child_categ': get_categ_and_subcateg()})
# return redirect(request.META.get('HTTP_REFERER'), context={'pusercustomsizes':objs, 'child_categ': get_categ_and_subcateg()})


def custom(request):
    return render(request, "hoitymoppet/custom-size.html")


@csrf_exempt
def get_country_state(request):
    if request.is_ajax and request.method == "GET":
        c_id = request.GET.get('country_id')
        state_items = HoityState.objects.filter(country_id_id = c_id)
        serialized_data = json.loads(serialize('json', state_items))
    return JsonResponse({'data': serialized_data})


@csrf_exempt
@login_required
def checkout(request):
    # get default name and number 28-10-2020
    name = ''
    if request.user.first_name and request.user.last_name:
        name = request.user.first_name + " " + request.user.last_name
    elif request.user.first_name:
        name = request.user.first_name
    user_name = name
    contact_number = request.user.profile.user_contact_number

    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter(status='active')
    privacy_items = Privacypolicy.objects.filter(status='active')
    terms_items = Terms.objects.filter(status='active')

    #state_items = HoityState.objects.all()
    country_items = HoityCountry.objects.all()
    state_items = HoityState.objects.filter(country_id_id = 103)

    # user_address = Product.objects.all()
    # #print("user_addressssssssssssssssssssssssssssssss", user_address)
    # #print("This is chekoutpage ........................................")

    #####abhishek 13-5-2020 Used to calculate sum of discount price
    total_discount_price = 0.0

    #####abhishek 13-6-2020 Adding coupon functionality
    coupon = ''
    coupon_code = ''
    coupon_dicount_amt = 0.0
    subtotal = 0.0
    #####abhishek 13-6-2020 Adding coupon functionality
    card_records = UserCart.objects.filter(user=request.user)
    if card_records:
        total_discount_price = cart_items_discount_price_total(card_records)
        subtotal = cart_items_discount_price_total(card_records) or 0.0
    #####abhishek 13-5-2020 Used to calculate sum of discount price

    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        mobile_no = request.POST.get('mobile_no')
        pincode = request.POST.get('pincode')
        locality = request.POST.get('locality')
        address = request.POST.get('address')
        state = request.POST.get('state')
        country = request.POST.get('country')
        city = request.POST.get('city')
        landmark = request.POST.get('landmark')
        alternate_no = request.POST.get('alternate_no')
        default = request.POST.get('default', False)

        ustate = HoityState.objects.filter(name__iexact=state)
        ucountry = HoityCountry.objects.filter(name__iexact=country)
        # print("ustateeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", ustate, ucountry)

        if not id:
            if name and mobile_no:
                addres = {
                    'user': request.user,
                    'name': name,
                    'mobile_no': mobile_no,
                    'pincode': pincode,
                    'locality': locality,
                    'address': address,
                    'user_state': ustate[0],
                    'user_country': ucountry[0],
                    'city': city,
                    'landmark': landmark,
                    'alternate_no': alternate_no,
                    'default': default
                }
                address = Address(**addres)
                # print("addressssssssssssssssssssssssssssssssssssssssssssssssss",address)
                address.save()
                objs = Address.objects.filter(user=request.user)

                # return render(request, 'hoitymoppet/checkout.html', context={'company_info':company_info, 'addresses':objs, 'total_discount_price': total_discount_price, 
                #     'faq_items':faq_items, 'state_items':state_items, 'country_items':country_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 
                #     'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()})

                return redirect(request.META.get('HTTP_REFERER'))

        else:
            addr = get_object_or_404(Address, id=id)
            addr.name = name
            addr.mobile_no = mobile_no
            addr.pincode = pincode
            addr.locality = locality
            addr.address = address
            addr.user_state = ustate[0]
            addr.user_country = ucountry[0]
            addr.city = city
            addr.landmark = landmark
            addr.alternate_no = alternate_no
            addr.default = default
            addr.save()
            objs = Address.objects.filter(user=request.user)

            # return render(request, 'hoitymoppet/checkout.html', context={'company_info':company_info, 'addresses': objs, 'total_discount_price': total_discount_price, 'faq_items':faq_items, 
            #     'testimonials_items':testimonials_items, 'state_items':state_items, 'country_items':country_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 
            #     'child_categ': get_categ_and_subcateg()})

            return redirect(request.META.get('HTTP_REFERER'))

    objs = Address.objects.filter(user=request.user)
    adress = []
    for obj in objs:
        addrs = obj.id
        adress.append(addrs)
    # print("objsssssssssssssssssssssssssssssssssssssssssss", objs)
    addr_id = 0

    #####abhishek start 13-6-2020 get coupon code from url sent from addtocart page Apply Button
    if request.GET:
        if request.GET.get('cpn'):
            coupon = request.GET.get('cpn')
            coupon_id = int(coupon)
            coupon_code_rec = Coupon.objects.filter(id=coupon_id)
            if coupon_code_rec:
                coupon_code = coupon_code_rec[0].code or ''

                if coupon_code_rec[0].discount_type == 'Fixed':
                    coupon_dicount_amt = round(coupon_code_rec[0].discount)
                elif coupon_code_rec[0].discount_type == 'Percentage':
                    coupon_dicount_amt = round((total_discount_price * coupon_code_rec[0].discount) / 100)
                subtotal = total_discount_price - coupon_dicount_amt
        # Jatin added code for address check
        if request.GET.get('addr'):
            # print("hello")
            addr_id = request.GET.get('addr')
            # print("addr_id",addr_id)
        # jatin end

    #####abhishek end 13-6-2020 get coupon code from url sent from addtocart page Apply Button
    # Jatin added code for shipping charges and added values in return dict
    ship_charges = 0.0
    u_pay = 0.0
    if card_records:
        shipping_charges = cart_items_shipping_charges(request, card_records, subtotal,addr_id) or 0.0
        #print('shipping_charges', shipping_charges)
        if shipping_charges:
            ship_charges=shipping_charges['shipping']
        u_pay = subtotal + ship_charges
        disp_cont=shipping_charges['disp_cont']
        if ship_charges==0.0:
            ship_charges ="Free Shipping"
    return render(request, "hoitymoppet/checkout.html", {'user_name': user_name, 'contact_number': contact_number, 'company_info':company_info, 'addresses': objs,'adress':adress,'coupon': coupon, 'coupon_code': coupon_code,
        'faq_items':faq_items, 'state_items':state_items, 'country_items':country_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items,
        'terms_items':terms_items, 'coupon_dicount_amt': format(coupon_dicount_amt,'.2f'), 'subtotal': format(subtotal,'.2f'), 'total_discount_price': format(total_discount_price,'.2f'),
        'shipping_charges':ship_charges,'u_pay':format(u_pay,'.2f'),'addr_id':addr_id,'disp_cont':disp_cont,'child_categ': get_categ_and_subcateg()})
# end jatin

@login_required
def deliverymethod(request):

    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter(status='active')
    privacy_items = Privacypolicy.objects.filter(status='active')
    terms_items = Terms.objects.filter(status='active')

    #####abhishek 13-5-2020 send address and Cart Items on delivery method page
    address = []
    items = []

    #####abhishek 13-6-2020 Adding coupon functionality
    coupon = ''
    coupon_code = ''
    coupon_dicount_amt = 0.0
    subtotal = 0.0
    #####abhishek 13-6-2020 Adding coupon functionality

    if request.GET and request.GET.get('addr'):
        delivery_address = Address.objects.filter(user=request.user, id=request.GET.get('addr'))
        if delivery_address:
            address = delivery_address[0]
    items = UserCart.objects.filter(user=request.user)
    total_discount_price = cart_items_discount_price_total(items) or 0.0
    subtotal = cart_items_discount_price_total(items) or 0.0
    #####abhishek 13-5-2020 send address and Cart Items on delivery method page

    #####abhishek start 13-6-2020 get coupon code from url sent from addtocart page Apply Button
    if request.GET:
        if request.GET.get('cpn'):
            coupon = request.GET.get('cpn')
            coupon_id = int(coupon)
            coupon_code_rec = Coupon.objects.filter(id=coupon_id)
            if coupon_code_rec:
                coupon_code = coupon_code_rec[0].code or ''

                if coupon_code_rec[0].discount_type == 'Fixed':
                    coupon_dicount_amt = round(coupon_code_rec[0].discount)
                elif coupon_code_rec[0].discount_type == 'Percentage':
                    coupon_dicount_amt = round((total_discount_price * coupon_code_rec[0].discount) / 100)
                subtotal = total_discount_price - coupon_dicount_amt
    #####abhishek end 13-6-2020 get coupon code from url sent from addtocart page Apply Button
    # jatin added code for shipping charges and a field in dictionary

    shipping_charges = cart_items_shipping_charges(request, items, subtotal,request.GET.get('addr')) or 0.0
    #print('shipping_charges', shipping_charges)
    ship_charges=0.0
    if shipping_charges:
        ship_charges=shipping_charges['shipping']
    u_pay = subtotal + ship_charges
    return render(request, "hoitymoppet/delivery-method.html", {'company_info':company_info, 'address': address, 'items': items,
        'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items,
        'privacy_items':privacy_items, 'terms_items':terms_items, 'coupon': coupon, 'coupon_code': coupon_code,
        'coupon_dicount_amt': coupon_dicount_amt, 'subtotal': subtotal, 'total_discount_price': total_discount_price,
        'u_pay':format(u_pay,'.2f'),'child_categ': get_categ_and_subcateg()})
    #end Jatin


@login_required
def paymentmethod(request):

    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter(status='active')
    privacy_items = Privacypolicy.objects.filter(status='active')
    terms_items = Terms.objects.filter(status='active')

    display_items = UiConfiguration.objects.filter(status='active')
    #print("display_itemssssssssssssssssssssssssssssssssssssssssss", display_items)

    #####abhishek 21-5-2020 send address on payment method page
    address = []

    #####abhishek 13-6-2020 Adding coupon functionality
    coupon = ''
    coupon_code = ''
    coupon_dicount_amt = 0.0
    subtotal = 0.0
    #####abhishek 13-6-2020 Adding coupon functionality

    if request.GET and request.GET.get('addr'):
        delivery_address = Address.objects.filter(user=request.user, id=request.GET.get('addr'))
        if delivery_address:
            address = delivery_address[0]

    #####abhishek start 13-6-2020 get coupon code from url sent from addtocart page Apply Button
    if request.GET:
        if request.GET.get('cpn'):
            coupon = request.GET.get('cpn')
            coupon_id = int(coupon)
            coupon_code_rec = Coupon.objects.filter(id=coupon_id)
            if coupon_code_rec:
                coupon_code = coupon_code_rec[0].code or ''
    #####abhishek end 13-6-2020 get coupon code from url sent from addtocart page Apply Button

    return render(request, "hoitymoppet/payment-method.html", {'company_info':company_info, 'address': address, 'coupon': coupon, 'coupon_code': coupon_code,
        'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items,
        'terms_items':terms_items, 'display_items':display_items, 'child_categ': get_categ_and_subcateg()})


def singleorderconfirmation(request):
    context = {'child_categ': get_categ_and_subcateg()}
    return render(request, "etemplate/single-order-confirmation.html", context)

def multiorderconfirmation(request):
    context = {'child_categ': get_categ_and_subcateg()}
    return render(request, "etemplate/multi-order-confirmation.html", context)

def userconfirmation(request):
    context = {'child_categ': get_categ_and_subcateg()}
    return render(request, "etemplate/user-confirmation.html", context)


# Piyush: code for sending email based on cart items
def cart_mail_view(request):
    all_cart_items = UserCart.objects.all()
    for number in all_cart_items:

        # Admin input from the cart menu
        # no_of_times = number.no_of_times
        # no_of_days = number.no_of_days
        no_of_times = 3  # default for now
        no_of_days = 7  # default for now

        while no_of_times > 0:

            user_cart = UserCart.objects.all()
            user_list = []
            req_user = []
            req_email = []
            times = 1

            # got user whose items have been a req time of creation
            for usr in user_cart:
                req_date = usr.create_date + timedelta(days=no_of_days * times)

                if req_date.date == datetime.now().date():
                    # for testing
                    # if req_date.date:
                    user_list.append(usr.user)
                else:
                    # pass
                    return HttpResponse("No items to send mail today!")

            # cart items for users obtained
            if user_list:

                # remove duplicate user from the users list
                for usr in user_list:
                    if usr not in req_user:
                        req_user.append(usr)

            if req_user:
                # for all the products related to particular user
                # for user_id in req_user:
                # user_item = UserCart.objects.filter(user=user_id)

                # for the particular product, required to send details about

                for user_id in req_user:
                    cr_date = datetime.now().date() - timedelta(days=no_of_days * times)
                    user_item = UserCart.objects.filter(user=user_id, create_date=cr_date)
                    # for testing
                    # user_item = UserCart.objects.filter(user=user_id)

                    if user_item:
                        req_email.append(user_id.email)
                        # for testing
                        # req_email = 'piyushpandey164@gmail.com'

                        message = {'items': user_item, 'BASE_URL': settings.BASE_URL,}

                        email = EmailMessage('etemplate/status-change-mail.tpl', message, settings.EMAIL_HOST_USER,
                                             [req_email])
                        email.send()
                        times += 1
                        no_of_times -= 1

    # code ends here

# @csrf_exempt
# def getcustomsize(request):
#     if request.is_ajax and request.method == "POST":
#         size = request.POST.get('size_val', None)
#         #print("sizeeeeeeeeeeeeeeeeeeeeeeeeeee in post", size)
#         custom_size = Age.objects.filter(age = size)
#         if custom_size:
#             age = custom_size[0].id
#             #print("the value in the cusotm size is", custom_size)
#             #print(age)
#             data = Measurements.objects.filter(age = age)
#             serialized_data = json.loads(serialize('json', data))
#             return JsonResponse({'data': serialized_data})


@csrf_exempt
def getcustomsize(request):
    if request.is_ajax and request.method == "POST":
        size = request.POST.get('size_val', None)
        custom_size = Age.objects.filter(age=size)
        if custom_size:
            age = custom_size[0].id
            data = Measures.objects.filter(age=age, status='active').values()
            val_list = []
            # print("The value in  the data is",data)
            for values in data:
                for key, value in values.items():
                    master = values['mesure_name_id']
                    master_name = Measurement_Master.objects.get(id=master).name
                val_list.append({'master_name': master_name, 'stand_value': values['value']})
            # print("The vlue in hte list is",val_list)
            # serialized_data = json.loads(serialize('json', data))
            # print("ddddddddddddddddddddddddddddddddddd", json.dumps(val_list))
            return JsonResponse(json.dumps(val_list), safe=False)
        else:
            return JsonResponse({'data': 'No Data Found'})


# Piyush: code for checking unique name of the custom size for every particular customer on 03-11-2020
@csrf_exempt
def unique_custom_name(request):
    """
    this method will check for the unique name of the custom size for every particular user.
    :param request: custom size name will be send in the request and that will be validated from the database as per
           customer.
    :return: this will return a boolean response that name exist or not.
    """
    if request.is_ajax and request.method == "POST":
        custom_name = request.POST.get('custom_size_name', None)
        obtained_age = request.POST.get('age', None)
        age = Age.objects.filter(age=obtained_age)[0]
        if custom_name and age:
            cx_measures_master = UserCustomMeasuresMaster.objects.filter(user_custom_size_name=custom_name,
                                                                         user=request.user).filter(age=age)
            if cx_measures_master and len(cx_measures_master) >= 1:
                return JsonResponse({'data': True})
            else:
                return JsonResponse({'data': False})
        return JsonResponse({'data': 'NOK'})
# Piyush: code for checking unique name of the custom size for every perticular customer on 03-11-2020 ends here


# Trilok Added this function 08-10-2020
@csrf_exempt
def getselectedcustomsize(request):
    """
    if user select the already defined custom size and press the customize button in product details page then
    this function will fetch the value of selected custom size from the usercustom measures table and return an
    json response to the javascript function.
    """
    if request.is_ajax and request.POST:
        size = request.POST.get('size_val', None)
        custom_master = request.POST.get('selected_cust_size', None)
        custom_size = Age.objects.filter(age=size)
        cust_master = UserCustomMeasuresMaster.objects.filter(user_custom_size_name=custom_master, user=request.user, age=custom_size[0].id)
        if custom_size and cust_master:
            age = custom_size[0].id
            cust_id = cust_master[0].id
            data = UserCustomMeasures.objects.filter(age=age, custom_measures_master=cust_id).values()
            val_list = []
            for values in data:
                for key, value in values.items():
                    master = values['measures_id']
                    measure_id = Measures.objects.get(id=master)
                val_list.append({'master_name': measure_id.mesure_name.name, 'stand_value': values['standard_value'], 'custom_value': values['custom_value']})
            return JsonResponse(json.dumps(val_list), safe=False)
    return JsonResponse({'data': 'Method is not allowed'})


@csrf_exempt
def GetUserCustomSize(request):
    if request.is_ajax and request.method == "POST":
        size = request.POST.get('size_val', None)
        age = Age.objects.filter(age = size)[0]
        user = request.user
        custom_size = UserCustomMeasuresMaster.objects.filter(user=user, age=age)
        if custom_size:
            serialized_data = json.loads(serialize('json', custom_size))
            return JsonResponse({'data': serialized_data})


# Trilok Added this function to check custom size have active order or not. 09-10-2020
def check_custom_size_active_orders(obj, user):
    """
    This function will return a boolean value on the basis of condition if the obj is linked with order
    and order is not completed yet then it will return false.
    on the basis of boolean value user will edit the selected user custom size.
    """
    result = False
    orders = Order.objects.filter(custom_size_master=obj, user=user)
    if orders:
        for order in orders:
            if order.status_name != 'delivered':
                result = True
                break
    return result


# Piyush: code for creating post view for sending data to pflo of user custom measure on 19-02-2020
def after_save_custom_measure(migration, obj):
    if migration:
        for instance in migration:
            try:
                # P: preparing req dict of data to be send
                req_dict = {
                    "user_custom_size_name": instance.user_custom_size_name or '',
                    "customer": instance.user.reference_id or False,
                    "age": instance.age.reference_id or False,
                    "measures_id": instance.measures.reference_id or False,
                    "standard_value": instance.standard_value or False,
                    "custom_value": instance.custom_value or False,
                    "custom_measures_master": instance.custom_measures_master.reference_id or obj.reference_id or False,
                    "status": instance.status or False,
                    "migrate_data": True,
                    "reference_id": instance.id or False,
                }
                prepare_and_connect(instance=instance, req_model='custom.measures', req_dict=req_dict,
                                    model=UserCustomMeasures,
                                    from_find='id', to_find=instance.reference_id)
            except Exception as e:
                pass
# Piyush: code for creating post view for sending data to pflo of user custom measure on 20-10-2020


# Piyush: code for custom user measure master post view for sending data to pflo
def after_save_cx_measures_master(instance, **kwargs):
    try:
        # P: preparing req dict of data to be send
        req_dict = {
            "user_custom_size_name": instance.user_custom_size_name,
            "customer_id": instance.user.reference_id or 1,
            "age_id": instance.age.reference_id or 1,
            "status": instance.status or 'active',
            "migrate_data": True,
            "reference_id": instance.id
        }
        prepare_and_connect(instance=instance, req_model='user.custom.measures.master', req_dict=req_dict,
                            model=UserCustomMeasuresMaster, from_find='id', to_find=instance.reference_id)
    except Exception as e:
        pass
# P: code ends here


# Trilok Implement the create and write logic of user data 9-10-2020
@login_required
@csrf_exempt
def add_user_custom_size(request):
    """
    This function accept the dictionary from a javascript function then loop over it and create or update the record in the
    database on the basis of condition.
    --->if user select the already defined custom size then this function will edit the values.
    ---->if size is newly created then it will create the record with the values that we are getting in the dict.
    """
    if request.is_ajax and request.method == "POST":
        data_dict = json.loads(request.POST.get('final_values'))
        # print("the value in the data dict, data_dict", data_dict)
        custom_list = []
        measures_list = []
        for item in data_dict:
            asize = item.get('size')
            size_id = Age.objects.filter(age=asize)[0]
            master = item.get('master_name')
            master_id = Measurement_Master.objects.filter(name=master)[0]
            measure_id = Measures.objects.filter(age=size_id).filter(mesure_name=master_id)[0]

            user_custom_size_name = item.get('custom_size_name')
            standard_value = item.get('stand_value')
            custom_value = item.get('cust_value') if item.get('cust_value') != 0 else item.get('stand_value')

            obj, created = UserCustomMeasuresMaster.objects.get_or_create(user_custom_size_name=user_custom_size_name,
                                                                          user=request.user, age=size_id)
            obj.save()
            # Piyush: added code for migrating this to pflo lite on 20-10-2020
            if obj:
                after_save_cx_measures_master(obj)
            isactive = check_custom_size_active_orders(obj, request.user)
            if isactive:
                return JsonResponse({'code': 'NOK',
                                     'msg': "You have already placed order with this size you can not edit it until the order completion."})
            custom_data = UserCustomMeasures.objects.filter(custom_measures_master=obj)
            if custom_data:
                for row in custom_data:
                    if row.measures.id == measure_id.id:
                        row.custom_value = custom_value
                        row.save()
                        measures_list.append(row)

            else:
                vals = {
                    'user': request.user,
                    'age': size_id,
                    'measures': measure_id,
                    'user_custom_size_name': user_custom_size_name,
                    'standard_value': standard_value,
                    'custom_value': custom_value,
                    'custom_measures_master': obj,
                }
                custom_list.append(UserCustomMeasures(**vals))

        migration = []
        for line in custom_list:
            line.save()
            migration.append(line)
        if migration:
            after_save_custom_measure(migration=migration, obj=obj)
        if measures_list:
            after_save_custom_measure(migration=measures_list, obj=obj)

        if user_custom_size_name:
            return JsonResponse({'code': 'OK', 'msg': 'insertion/updation is successful'})


# Post request for user creations
@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':

        data = request.data

        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            user_id = list(User.objects.filter(
                first_name=serializer.data['first_name']).values('id'))
            reference_id = user_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_user(request, pk):
    try:
        req_user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":

        serializer = UserSerializer(instance=req_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# P: code for creating user ends here

from rest_framework.response import Response


# Post request for company creations
@api_view(['GET'])
def company_record(request):
    company_qs = Associated_Company.objects.all()
    serializer = CompanySerializer(company_qs, many=True)
    # return JsonResponse(serializer.data, safe=False)
    return Response(serializer.data)


@api_view(['POST'])
def create_company(request):
    if request.method == 'POST':
        data = request.data

        serializer = CompanySerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            company_id = list(Associated_Company.objects.filter(
                associated_company_name=serializer.data['associated_company_name']).values('id'))
            reference_id = company_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_company(request, pk):
    try:
        req_company = Associated_Company.objects.get(id=pk)
    except Associated_Company.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = CompanySerializer(instance=req_company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# P: code ends for company creation


# P: code for product category creation
@api_view(['GET'])
def category_record(request):
    company_qs = Categories.objects.all()
    serializer = CategoriesSerializer(company_qs, many=True)
    # return JsonResponse(serializer.data, safe=False)
    return Response(serializer.data)


@api_view(['POST'])
def create_category(request):
    if request.method == 'POST':

        data = request.data

        serializer = CategoriesSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            category_id = list(Categories.objects.filter(
                category=serializer.data['category']).values('id'))
            reference_id = category_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_category(request, pk):
    try:
        req_category = Categories.objects.get(id=pk)
    except Categories.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":

        serializer = CategoriesSerializer(instance=req_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# P: code ends for company creation


# Piyush: code for creating product
@api_view(['POST'])
def create_product(request):
    if request.method == 'POST':
        data = request.data
        serializer = ProductSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            product_id = list(Product.objects.filter(
                product_name=serializer.data['product_name']).values('id'))
            reference_id = product_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_product(request, pk):
    try:
        req_product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":

        serializer = ProductSerializer(instance=req_product, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_product(request, pk):
    req_product = Product.objects.get(id=pk)
    req_product.delete()
    return JsonResponse("Deleted", status=status.HTTP_204_NO_CONTENT)
# Piyush: code for creating product ends here


# Piyush: put and post request for creating care instruction
@api_view(['POST'])
def create_care_instruction(request):
    if request.method == 'POST':
        data = request.data
        serializer = CareinstructionsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            care_id = list(Careinstructions.objects.filter(
                cares_name=serializer.data['cares_name']).values('id'))
            reference_id = care_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_care_instruction(request, pk):
    try:
        req_instruction = Careinstructions.objects.get(id=pk)
    except Careinstructions.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":

        serializer = CareinstructionsSerializer(instance=req_instruction, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Piyush: put and post request for creating fabric
@api_view(['POST'])
def create_fabric(request):
    if request.method == 'POST':
        data = request.data
        serializer = FabricSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            fabric_id = list(Fabric.objects.filter(
                fabric=serializer.data['fabric']).values('id'))
            reference_id = fabric_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_fabric(request, pk):
    try:
        req_fabric = Fabric.objects.get(id=pk)
    except Fabric.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":

        serializer = FabricSerializer(instance=req_fabric, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# P: code for fabric ends here


# Piyush: put and post request for creating color
@api_view(['POST'])
def create_color(request):
    if request.method == 'POST':
        data = request.data
        serializer = ColorSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            color_id = list(Color.objects.filter(
                color_name=serializer.data['color_name']).values('id'))
            reference_id = color_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_color(request, pk):
    try:
        req_color = Color.objects.get(id=pk)
    except Color.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":

        serializer = ColorSerializer(instance=req_color, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# P: code for fabric ends here


# Piyush: put and post request for creating age
@api_view(['POST'])
def create_age(request):
    if request.method == 'POST':
        data = request.data
        serializer = AgeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            age_id = list(Age.objects.filter(
                age=serializer.data['age']).values('id'))
            reference_id = age_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_age(request, pk):
    try:
        req_age = Age.objects.get(id=pk)
    except Age.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = AgeSerializer(instance=req_age, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_age(request, pk):
    req_item = Product.objects.get(id=pk)
    req_item.delete()
    return JsonResponse(1, status=status.HTTP_201_CREATED)
# P: code for age ends here


# Piyush: put and post request for creating photo
@api_view(['POST'])
def create_images(request):
    if request.method == 'POST':
        data = request.data
        serializer = PhotoSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            image_id = list(Photo.objects.filter(
                product=serializer.data['product']).values('id'))
            reference_id = image_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Piyush: put and post request for creating photo ends here


# Piyush: code for updating status change of a sale order from pflo lite on 13-09-2020
@api_view(['PUT'])
def update_order(request, pk):
    try:
        req_order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        user = User.objects.filter(id=req_order.user.id).first()
        change_state_to = ''
        required_state = request.data.get('state', '') or request.data.get('state_new', '') or False

        if required_state:
            if required_state == 'sale':
                change_state_to = 'confirmed'

                if req_order.status_name != 'confirmed':

                    if req_order:
                        Order.objects.filter(id=req_order.id).update(status_name=change_state_to)

                        user_req = req_order.user

                        tracking_status = TrackingStatus.objects.create(
                            user=user_req,
                            order_id=req_order,
                            status_name=change_state_to,
                        )

                        # Piyush: code for sending mail on change of order status on 06-08-2020
                        generated_order = Order.objects.filter(id=pk).first()
                        generated_order_detail_list = OrderDetail.objects.filter(order_id=generated_order)
                        description = EmailDescription.objects.filter(subject='order_confirmed').first()
                        subject = "Your order has been Confirmed. " + generated_order.ref_code

                        req_username = user.email.split("@")[0]
                        if user.first_name and user.last_name:
                            name = user.first_name + " " + user.last_name
                        elif user.first_name:
                            name = user.first_name
                        else:
                            name = req_username
                        placed_on = generated_order.ordered_date.date()
                        current_site = get_current_site(request)
                        address = Address.objects.filter(id=generated_order.address_id.id).first()
                        # Piyush: code for getting shipping charges on 19dec
                        ship_charges = 0.0
                        if generated_order.shipping_charges:
                            ship_charges = generated_order.shipping_charges
                        price_total = 0.0
                        if generated_order:
                            order_details = OrderDetail.objects.filter(order_id=generated_order.id)
                            if order_details:
                                for detail in order_details:
                                    price_total += detail.total_price
                                if ship_charges:
                                    price_total += ship_charges
                        # Piyush: code for getting shipping charges on 19dec ends here
                        message = {
                            'user': user,
                            'placed_on': placed_on,
                            'name': name,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'generated_order': generated_order,
                            'generated_order_detail_list': generated_order_detail_list,
                            'address': address,
                            'description': description,
                            'subject': subject,
                            'BASE_URL': settings.BASE_URL,
                            'ship_charges': ship_charges,
                            'price_total': price_total,
                        }
                        config = DynamicEmailConfiguration.get_solo()
                        to_email = user.email
                        email = EmailMessage('etemplate/acc_activate_email.tpl', message,
                                             "Do not reply <{}>".format(config.from_email), to=[to_email])
                        email.send()

            elif required_state == 'draft':
                change_state_to = 'ordered'

                if req_order.status_name != 'ordered':
                    if req_order:
                        Order.objects.filter(id=req_order.id).update(status_name=change_state_to)

                        user_req = req_order.user

                        tracking_status = TrackingStatus.objects.create(
                            user=user_req,
                            order_id=req_order,
                            status_name=change_state_to,
                        )

                        # # Piyush: code for sending mail on change of order status on 06-08-2020
                        # # getting required order
                        # order = Order.objects.get(id=req_order.id)
                        # details = OrderDetail.objects.filter(order_id=order)
                        # message = {'order': order, 'details': details}
                        # # getting user email id for sending mail
                        # req_email = order.user.email
                        # # for testing
                        # # req_email = 'piyushpandey164@gmail.com'
                        # email = EmailMessage('etemplate/status-change-mail.tpl', message, settings.EMAIL_HOST_USER,
                        #                      [req_email])
                        # email.send()

            # elif required_state == 'done':
            # elif required_state == 'done':
            #     change_state_to = 'delivered'
            #
            #     if req_order.status_name != 'delivered':
            #         if req_order:
            #             Order.objects.filter(id=req_order.id).update(status_name=change_state_to)
            #
            #             user_req = req_order.user
            #
            #             tracking_status = TrackingStatus.objects.create(
            #                 user=user_req,
            #                 order_id=req_order,
            #                 status_name=change_state_to,
            #             )
            #             # Piyush: code for sending mail on change of order status on 06-08-2020
            #             generated_order = Order.objects.filter(id=pk).first()
            #             generated_order_detail_list = OrderDetail.objects.filter(order_id=generated_order)
            #             description = EmailDescription.objects.filter(subject='order_delivered').first()
            #             subject = "Your order has been Delivered. " + generated_order.ref_code
            #             req_username = request.user.email.split("@")[0]
            #             if request.user.first_name and request.user.last_name:
            #                 name = request.user.first_name + " " + request.user.last_name
            #             elif request.user.first_name:
            #                 name = request.user.first_name
            #             else:
            #                 name = req_username
            #             placed_on = generated_order.ordered_date.date()
            #             current_site = get_current_site(request)
            #             address = Address.objects.filter(id=generated_order.address_id.id).first()
            #
            #             message = {
            #                 'user': request.user,
            #                 'placed_on': placed_on,
            #                 'name': name,
            #                 'domain': current_site.domain,
            #                 'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
            #                 'generated_order': generated_order,
            #                 'generated_order_detail_list': generated_order_detail_list,
            #                 'address': address,
            #                 'description': description,
            #                 'subject': subject,
            #             }
            #             config = DynamicEmailConfiguration.get_solo()
            #             current_user = User.objects.get(id=request.user.id)
            #             to_email = user.email
            #             email = EmailMessage('etemplate/acc_activate_email.tpl', message,
            #                                  "Do not reply <{}>".format(config.from_email), to=[to_email])
            #             email.send()

            # elif required_state == 'Shipped':
            elif required_state == 'done':
                change_state_to = 'dispatched'

                if req_order.status_name != 'dispatched':
                    if req_order:
                        Order.objects.filter(id=req_order.id).update(status_name=change_state_to)

                        user_req = req_order.user

                        tracking_status = TrackingStatus.objects.create(
                            user=user_req,
                            order_id=req_order,
                            status_name=change_state_to,
                        )

                        # Piyush: code for sending mail on change of order status on 06-08-2020
                        generated_order = Order.objects.filter(id=pk).first()
                        generated_order_detail_list = OrderDetail.objects.filter(order_id=generated_order)
                        description = EmailDescription.objects.filter(subject='order_dispatched').first()
                        subject = "Your order has been Dispatched. " + generated_order.ref_code
                        req_username = user.email.split("@")[0]
                        if user.first_name and user.last_name:
                            name = user.first_name + " " + user.last_name
                        elif user.first_name:
                            name = user.first_name
                        else:
                            name = req_username
                        placed_on = generated_order.ordered_date.date()
                        current_site = get_current_site(request)
                        address = Address.objects.filter(id=generated_order.address_id.id).first()
                        # Piyush: code for getting shipping charges and total price on 19dec
                        ship_charges = 0.0
                        if generated_order.shipping_charges:
                            ship_charges = generated_order.shipping_charges
                        price_total = 0.0
                        if generated_order:
                            order_details = OrderDetail.objects.filter(order_id=generated_order.id)
                            if order_details:
                                for detail in order_details:
                                    price_total += detail.total_price
                                if ship_charges:
                                    price_total += ship_charges
                        # Piyush: code for getting shipping charges on 19dec ends here
                        message = {
                            'user': request.user,
                            'placed_on': placed_on,
                            'name': name,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'generated_order': generated_order,
                            'generated_order_detail_list': generated_order_detail_list,
                            'address': address,
                            'description': description,
                            'subject': subject,
                            'BASE_URL': settings.BASE_URL,
                            'ship_charges': ship_charges,
                            'price_total': price_total,
                        }
                        config = DynamicEmailConfiguration.get_solo()
                        # current_user = User.objects.get(id=request.user.id)
                        to_email = user.email
                        email = EmailMessage('etemplate/acc_activate_email.tpl', message,
                                             "Do not reply <{}>".format(config.from_email), to=[to_email])
                        email.send()

            # code ends here


# Piyush: code for updating status change of a sale order from pflo lite on 13-09-2020 ends here
# Piyush: main function for connection and creating and sending data
def prepare_and_connect(instance=None, req_dict=None, req_model=None, model=None, from_find=None, to_find=None):
    # P: establishing connection
    url = settings.URL_PATH
    db = settings.DATABASE
    username = settings.USERNAME
    password = settings.PASSWORD

    # P: code for authenticating user data
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
    uid = common.authenticate(db, username, password, {})

    # P: searching for user if already exist in pflo
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
    id_found = models.execute_kw(db, uid, password, req_model, 'search',
                                 [[[from_find, '=', to_find]]])

    if id_found:
        search_id = id_found[0]
        models.execute_kw(db, uid, password, req_model, 'write', [[search_id], req_dict])
    else:
        created_id = models.execute_kw(db, uid, password, req_model, 'create', [req_dict])  # id
        created_instance = model.objects.get(id=instance.id)
        created_instance.reference_id = created_id  # change field
        created_instance.migrate_data = True  # migrate True
        created_instance.save()  # this will update reference id in hoity with id of item created in pflo


# connection and prepare function ends here


# Piyush: code for creating post view for sending data to pflo
@receiver(post_save, sender=User)
def after_save_user(sender, instance, **kwargs):
    if not instance.is_staff and not instance.is_superuser:
        # P: preparing req dict of data to be send 28-10-2020
        if instance.first_name and instance.last_name:
            name = instance.first_name + " " + instance.last_name + " " + instance.username
        elif instance.first_name:
            name = instance.first_name + " " + instance.username
        else:
            name = instance.username
        req_dict = {
            "name": name,
            "company_type": "person" or "company",
            "email": instance.email or '',
            "migrate_data": True,
            "reference_id": instance.id or '',
            "created_from_hm": True,
        }

        # P: establishing connection
        url = settings.URL_PATH
        db = settings.DATABASE
        username = settings.USERNAME
        password = settings.PASSWORD

        # P: code for authenticating user data
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)

        # P: searching for user if already exist in pflo based on email or based on id
        id_found = models.execute_kw(db, uid, password, 'res.partner', 'search',
                                     [[['email', '=', instance.email.strip()],
                                       ['parent_id', '=', False]]])

        if not id_found:
            id_found = models.execute_kw(db, uid, password, 'res.partner', 'search',
                                         [[['reference_id', '=', instance.id],
                                           ['parent_id', '=', False]]])

        if id_found:
            search_id = id_found[0]
            id_returned = models.execute_kw(db, uid, password, 'res.partner', 'write', [[search_id], req_dict])
            if id_returned:
                found_instance = User.objects.get(id=instance.id)
                if not found_instance.reference_id:
                    found_instance.reference_id = id_found[0]  # change field
                    found_instance.migrate_data = True  # migrate True
                    found_instance.save()

        else:
            created_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [req_dict])  # id
            created_instance = User.objects.get(id=instance.id)
            created_instance.reference_id = created_id  # change field
            created_instance.migrate_data = True  # migrate True
            created_instance.save()  # this will update reference id in hoity with id of item created in pflo
            if instance and not instance.reference_id:
                global REFERENCE_ID, MIGRATE_DATA, CREATED_INSTANCE
                REFERENCE_ID = created_id
                MIGRATE_DATA = True
                CREATED_INSTANCE = instance.id
# P: code ends here


# Piyush: code for creating post view for sending data to pflo
@receiver(post_save, sender=Child)
def after_save_child(sender, instance, **kwargs):
    try:
        m = instance.child_birth_date.date()
        date_of_birth = datetime.strptime(str(m), '%Y-%d-%m').date()

        # P: preparing req dict of data to be send
        req_dict = {
            "customer_id": instance.user.reference_id or False,
            "name": instance.child_name,
            "child_birth_date": str(date_of_birth),
            "migrate_data": True,
            "reference_id": instance.id
        }

        prepare_and_connect(instance=instance, req_model='customer.children', req_dict=req_dict, model=sender,
                            from_find='id', to_find=instance.reference_id)
    except Exception as e:
        pass
# P: code ends here


# Piyush: code for creating post view for sending data to pflo
@receiver(post_save, sender=Profile)
def after_save_profile(sender, instance, **kwargs):
    if instance.user_contact_number:
        # P: preparing req dict of data to be send
        req_dict = {
            "mobile": instance.user_contact_number,
        }
        try:
            prepare_and_connect(instance=instance, req_model='res.partner', req_dict=req_dict, model=sender,
                                to_find=instance.user.reference_id, from_find='id')
        except Exception as e:
            print('Exception in profile creation is : ', e)
# P: code ends here


# Piyush: code for creating post view for sending data to pflo
@receiver(post_save, sender=Address)
def after_save_address(sender, instance, **kwargs):
    # P: establishing connection
    url = settings.URL_PATH
    db = settings.DATABASE
    username = settings.USERNAME
    password = settings.PASSWORD

    # P: code for authenticating user data
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
    uid = common.authenticate(db, username, password, {})

    # check_state = instance.user_state.reference_id if instance.user_state.reference_id else 587
    # check_country = instance.user_country.reference_id if instance.user_country.reference_id else 1
    check_state = None
    if instance.user_state and instance.user_state.reference_id:
        check_state = instance.user_state.reference_id

    check_country = None
    if instance.user_country and instance.user_country.reference_id:
        check_country = instance.user_country.reference_id

    # P: preparing req dict of data to be send
    req_dict = {
        'name': instance.name,
        'mobile': instance.mobile_no,
        'email': instance.user.email or '',
        'zip': instance.pincode or False,
        'display_name': instance.name,
        'street': instance.locality or False,
        'street2': instance.address or False,
        'city': instance.city or False,
        'state_id': check_state,
        'country_id': check_country,
        'type': 'delivery',
        'migrate_data': True,
        'reference_id': instance.id,
        'from_hm': True,
    }

    # P: searching for user if already exist in pflo
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
    user_found = models.execute_kw(db, uid, password, 'res.partner', 'search',
                                   [[['id', '=', instance.user.reference_id]]])

    if user_found:

        # search for address on the basis of reference_id
        address_found = models.execute_kw(db, uid, password, 'res.partner', 'search',
                                          [[['reference_id', '=', instance.id],
                                            ['parent_id', '!=', False]]])
        if address_found:
            # print('address_found', address_found)
            # try:
                # P: preparing req dict of data to be send
            req_dict["display_name"] = instance.user.first_name + ' ' + instance.name or instance.name
            req_dict["parent_id"] = instance.user.reference_id
            models.execute_kw(db, uid, password, 'res.partner', 'write', [[address_found], req_dict])  # id

            # except Exception as e:
            # pass

        else:
            try:
                req_dict["display_name"] = instance.name
                req_dict["parent_id"] = instance.user.reference_id
                created_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [req_dict])  # id
                created_instance = Address.objects.get(id=instance.id)

            except Exception as e:
                pass

    else:
        req_dict["display_name"] = instance.name
        req_dict["parent_id"] = instance.user.reference_id
        created_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [req_dict])  # id
        created_instance = Address.objects.get(id=instance.id)
        # created_instance.reference_id = created_id  # change field
        # created_instance.save()  # this will update reference id in hoity with id of item created in pflo
# P: code ends here


# Piyush: code for creating post view for sending data to pflo
@receiver(post_save, sender=Order)
def after_save_order(sender, instance, **kwargs):
    # address_to_send = Address.objects.filter(id=instance.address_id.id).first().id
    # print("address_to_send", instance.address_id.id)

    # P: preparing req dict of data to be send
    # jatin added shipping charges in req_dict
    req_dict = {
        "partner_id": instance.user.reference_id or 1,
        "client_order_ref": instance.ref_code,
        "from_ecom": True,
        "migrate_data": True,
        "reference_id": instance.id,
        "data_from_hoitymoppet": True,
        "address_id": instance.address_id.id,
        "maximum_days": instance.maximum_days,
    }

    # P: establishing connection
    url = settings.URL_PATH
    db = settings.DATABASE
    username = settings.USERNAME
    password = settings.PASSWORD

    # P: code for authenticating user data
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
    uid = common.authenticate(db, username, password, {})

    # P: searching for user if already exist in pflo
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
    id_found = models.execute_kw(db, uid, password, 'sale.order', 'search',
                                 [[['id', '=', instance.reference_id]]])

    if id_found:
        search_id = id_found[0]
        models.execute_kw(db, uid, password, 'sale.order', 'write', [[search_id], req_dict])
        if instance.shipping_charges:
            shipping = ShippingProduct.objects.all().first()
            requ_dict= {"shipping_charges": instance.shipping_charges, "shipping_id": shipping.reference_id}
            models.execute_kw(db, uid, password, 'sale.order', 'write', [[search_id], requ_dict])

    else:
        try:
            created_id = models.execute_kw(db, uid, password, 'sale.order', 'create', [req_dict])  # id
            created_instance = Order.objects.get(id=instance.id)
            created_instance.reference_id = created_id  # change field
            search_order = models.execute_kw(db, uid, password, 'sale.order', 'read', [created_id], {'fields': ['name']})
            order_name = [data_dict['name'] for data_dict in search_order][0]
            created_instance.sale_order_name = order_name
            created_instance.save()  # this will update reference id in hoity with id of item created in pflo
        except Exception as e:
            print("Exception in Order placement is : ", e)
# P: code ends here


# Piyush: code for creating post view for sending data to pflo
@receiver(post_save, sender=OrderDetail)
def after_save_detail(sender, instance, **kwargs):
    item = Order.objects.get(id=instance.order_id.id)

    # get the product color and age
    age_need = None
    if instance.product_age:
        req_age = Age.objects.filter(id=instance.product_age.id).first()
        if req_age and req_age.reference_id:
            age_need = req_age.reference_id

    color_need = None
    if instance.prod_color:
        req_color = Color.objects.filter(id=instance.prod_color.id).first()
        if req_color and req_color.reference_id:
            color_need = req_color.reference_id

    measure_master = None
    if instance.user_custom_size_master:
        for_ref = UserCustomMeasuresMaster.objects.filter(id=instance.user_custom_size_master.id).first()
        if for_ref:
            measure_master = for_ref.reference_id or None
    unit = None
    if instance.product_id.product_uom:
        unit = instance.product_id.product_uom.reference_id or 1

    # P: preparing req dict of data to be send
    req_dict = {

        "order_id": item.reference_id or False,
        "name": instance.product_id.product_name or '',
        "product_id": instance.product_id.reference_id or 1,
        "product_uom_qty": instance.quantity or 1.0,
        "price_unit": float(instance.price) or float(instance.discount_price),
        "product_uom": unit or 1,
        "order_detail": True,
        "age_id": age_need or False,
        "color_id": color_need or False,
        "migrate_data": True,
        "reference_id": instance.id,
        "custom_measure_master_id": measure_master or False,
    }

    try:
        prepare_and_connect(instance=instance, req_model='sale.order.line', req_dict=req_dict, model=sender,
                            to_find=instance.reference_id, from_find='id')
    except Exception as e:
        print("Exception in sale order line is : ", e)
# P: code ends here


# Piyush: code for creating post view for sending data to pflo of cx cart on 15-02-2020
@receiver(post_save, sender=UserCart)
def after_save_cart(sender, instance, **kwargs):
    if instance.quantity > 0:
        try:
            cx_master = None
            if instance.user_custom_size_master:
                cx_master = instance.user_custom_size_master.reference_id
            cx_color = None
            if instance.prod_color:
                cx_color = instance.prod_color.reference_id
            total_price = 0.0
            if instance.quantity and instance.product_id:
                total_price = (instance.product_id.discount_price or instance.product_id.price) * instance.quantity

            # P: preparing req dict of data to be send
            req_dict = {
                "customer_id": instance.user.reference_id or False,
                "product_id": instance.product_id.reference_id or False,
                "product_age": instance.product_age.reference_id or False,
                "user_custom_size_master": cx_master or False,
                "color_id": cx_color or False,
                "quantity": instance.quantity or 0,
                "total_price": float(total_price) or 0,
                "ordered": instance.ordered or False,
                "migrate_data": True,
                "reference_id": instance.id or False,
            }

            prepare_and_connect(instance=instance, req_model='customer.cart', req_dict=req_dict, model=sender,
                                from_find='id', to_find=instance.reference_id)

        except Exception as e:
            pass
# Piyush: code for creating post view for sending data to pflo of cx cart on 15-02-2020 ends here


# Piyush: code for creating post view for sending data to pflo of cx wishlist on 15-02-2020
@receiver(post_save, sender=UserWishList)
def after_save_wishlist(sender, instance, **kwargs):
    try:
        # P: preparing req dict of data to be send
        req_dict = {
            "customer_id": instance.user.reference_id or False,
            "product_id": instance.product_id.reference_id or False,
            "migrate_data": True,
            "reference_id": instance.id or False,
        }

        prepare_and_connect(instance=instance, req_model='customer.wishlist', req_dict=req_dict, model=sender,
                            from_find='id', to_find=instance.reference_id)

    except Exception as e:
        pass
# Piyush: code for creating post view for sending data to pflo of cx wishlist on 15-02-2020 ends here


# Piyush: common function for deleting items revoked after post delete on 15-09-2020
def delete_items(instance=None, req_model=None):
    # P: establishing connection
    url = settings.URL_PATH
    db = settings.DATABASE
    username = settings.USERNAME
    password = settings.PASSWORD

    # P: code for authenticating user data
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
    uid = common.authenticate(db, username, password, {})

    id_to_delete = instance.reference_id
    # API for deleting record in pflo lite
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
    item_deleted = models.execute_kw(db, uid, password, req_model, 'unlink', [[id_to_delete]])

# Piyush: common function for deleting items revoked after post delete on 15-09-2020 ends here


# Piyush: code for deleting items after delete of item from cart on 15-09-2020
@receiver(post_delete, sender=UserCart)
def delete_cart_item(sender, instance, **kwargs):
    # function for deleting items
    delete_items(instance=instance, req_model='customer.cart')
# code ends here


# Piyush: code for deleting items after delete of item from wishlist on 15-09-2020
@receiver(post_delete, sender=UserWishList)
def delete_wishlist_item(sender, instance, **kwargs):
    # function for deleting items
    delete_items(instance=instance, req_model='customer.wishlist')
# code ends here


# Piyush: code for deleting items after delete of item from child on 15-09-2020
@receiver(post_delete, sender=Child)
def delete_children(sender, instance, **kwargs):
    # function for deleting items
    delete_items(instance=instance, req_model='customer.children')
# code ends here


# Post request for measurement master creations
@api_view(['POST'])
def create_measurement_master(request):
    if request.method == 'POST':
        data = request.data
        serializer = MeasurementSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            master_id = list(Measurement_Master.objects.filter(
                name=serializer.data['name']).values('id'))
            reference_id = master_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_measurement_master(request, pk):
    try:
        req_master = Measurement_Master.objects.get(id=pk)
    except Measurement_Master.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":

        serializer = MeasurementSerializer(instance=req_master, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# P: code for creating measurement master ends here


# Post request for measures creations
@api_view(['POST'])
def create_measures(request):
    if request.method == 'POST':
        data = request.data
        serializer = MeasuresSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            measures_id = list(Measures.objects.filter(
                reference_id=serializer.data['reference_id']).values('id'))
            reference_id = measures_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_measures(request, pk):
    try:
        req_measures = Measures.objects.get(id=pk)
    except Measures.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":

        serializer = MeasuresSerializer(instance=req_measures, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# P: code for creating user ends here


# P: code for creating user ends here


# Piyush: code for create_currency post view on 07-10-2020
@api_view(['POST'])
def create_currency(request):
    if request.method == 'POST':
        data = request.data
        serializer = ResCurrencySerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            currency_id = list(HoityCurrency.objects.filter(
                name=serializer.data['name']).values('id'))
            reference_id = currency_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Piyush: code for create_currency post view on 07-10-2020 ends here


# Piyush: code for create_currency_rate post view on 07-10-2020
@api_view(['POST'])
def create_currency_rate(request):
    if request.method == 'POST':
        data = request.data
        serializer = ResCurrencyRateSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            currency_rate_id = list(HoityCurrencyRate.objects.filter(
                name=serializer.data['name']).values('id'))
            reference_id = currency_rate_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Piyush: code for create_currency_rate post view on 07-10-2020 ends here


# Piyush: code for create_country post view on 07-10-2020
@api_view(['POST'])
def create_country(request):
    if request.method == 'POST':
        data = request.data
        serializer = ResCountrySerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            country_id = list(HoityCountry.objects.filter(
                name=serializer.data['name']).values('id'))
            reference_id = country_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Piyush: code for create_country post view on 07-10-2020 ends here


# Piyush: code for create_state post view on 07-10-2020
@api_view(['POST'])
def create_state(request):
    if request.method == 'POST':
        data = request.data
        serializer = ResStateSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            state_id = list(HoityState.objects.filter(
                name=serializer.data['name']).values('id'))
            reference_id = state_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Piyush: code for create_state post view on 07-10-2020 ends here


# Post request for coupons creations
@api_view(['POST'])
def create_coupon(request):
    if request.method == 'POST':
        data = request.data
        serializer = AvailableCouponsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            coupon_id = list(Coupon.objects.filter(
                code=serializer.data['code']).values('id'))
            reference_id = coupon_id[0]
            ##print("reference_id", reference_id)

            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_coupon(request, pk):
    try:
        req_coupon = Coupon.objects.get(id=pk)
    except Coupon.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":

        serializer = AvailableCouponsSerializer(instance=req_coupon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# P: code for creating user ends here


# P: code for creating user ends here


# Piyush: code for getting currency as per the country location of the user
def get_user_currency(request):
    """
    This method will return the user currency and currency rate as per the location of user.
    if country is other than India then its currency and rate will be retuned with its position.
    """
    user_location = ipapi.location(output='country_name')
    currency_by_location = ipapi.location(output='currency')
    # print("user_location and currency ---------------------", user_location, currency_by_location)
    try:
        country_obj = ResCountry.objects.filter(name=user_location).first()
    except ResCountry.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    try:
        currency_rate = None
        currency_obj = ResCurrency.objects.filter(name=currency_by_location).first()
        if currency_obj and currency_obj.name != "INR":
            country_rate = ResCurrencyRate.objects.filter(currency_id=currency_obj.id) or False
            usd_rate = ResCurrencyRate.objects.filter(name="USD").first()
            currency_rate = country_rate if country_rate else usd_rate
        elif currency_obj and currency_obj.name == "INR":
            currency_rate = "default"
        else:
            currency_rate = ResCurrencyRate.objects.filter(name="USD").first()

    except ResCurrency.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    context = {
        'country_obj': country_obj,
        'currency_obj': currency_obj,
        'currency_rate': currency_rate,
    }
    return context


# Piyush: code for getting currency as per the country location of the user code ends here


# Piyush: code for updating coupon in sale order
@receiver(post_save, sender=CouponHistory)
def after_save_history(sender, instance, **kwargs):
    # P: establishing connection
    url = settings.URL_PATH
    db = settings.DATABASE
    username = settings.USERNAME
    password = settings.PASSWORD

    # P: code for authenticating user data
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
    uid = common.authenticate(db, username, password, {})

    # P: searching for user if already exist in pflo
    sale_order = Order.objects.get(id=instance.order_id_id)
    reference_id_so = 0
    if sale_order:
        reference_id_so = sale_order.reference_id
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
    id_found = models.execute_kw(db, uid, password, 'sale.order', 'search',
                                 [[['id', '=', reference_id_so]]])
    # print(id_found)
    coupon_reference = Coupon.objects.get(id=instance.coupon_id_id)
    coup_obj = 0
    if coupon_reference:
        coup_obj = coupon_reference.reference_id

    if id_found:
        req_dict = {"coupon_id": coup_obj, "coupon_applied": True}
        search_id = id_found[0]
        models.execute_kw(db, uid, password, 'sale.order', 'write', [[search_id], req_dict])


# Piyush: code for updating coupon in sale order ends here


# Post request for product uom creations
@api_view(['POST'])
def create_product_uom(request):
    if request.method == 'POST':
        data = request.data
        serializer = ProductUomSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            instance_id = list(ProductUom.objects.filter(
                name=serializer.data['name']).values('id'))
            reference_id = instance_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_product_uom(request, pk):
    try:
        req_instance = ProductUom.objects.get(id=pk)
    except ProductUom.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":

        serializer = ProductUomSerializer(instance=req_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# P: code for creating measurement master ends here


# Jatin Added this function for calculating shipping charges
def cart_items_shipping_charges(request, items, subtotal, addr=None):
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com').first()
    shipping_charges = list(
        ShippingCharges.objects.filter(associated_company=company_info.id).values('free_order_value',
                                                                                   'charge_type',
                                                                                   'specific_charge',
                                                                                   'max_charge'))
    # print('shipping_charges',shipping_charges)
    disp_cont = False
    # free_order_value=shipping_charges[0]['free_order_value']
    # charge_type=shipping_charges[0]['charge_type']
    shipping = 0.0
    ship_list = []
    if addr:
        delivery_address = Address.objects.filter(user=request.user, id=request.GET.get('addr'))
        # print("delivery_address",delivery_address)
        for addrs in delivery_address:
            country = addrs.user_country
        # print("country",country)

        if country:
            if country.name == 'India':
                disp_cont = True
                # print("ohk")
            else:
                # print("outside")
                messages.info(request, 'Sorry currently not delivering outside india ')
        else:
            disp_cont = True
            # messages.info(request, 'No country selected')

    if items:
        for item in items:
            if item.product_id.shipping_charges:
                ship = item.product_id.shipping_charges
                # print('ship', ship)
                ship = ship * item.quantity
                ship_list.append(ship)

    # print('ship_list',ship_list)
    if shipping_charges:
        # free_order_value=5000.00
        if subtotal > shipping_charges[0]['free_order_value']:
            shipping = 0.0
        else:
            if shipping_charges[0]['charge_type'] == 'specific_amount':
                shipping = shipping_charges[0]['specific_charge']
            elif shipping_charges[0]['charge_type'] == 'prod_based_charge':

                if shipping_charges[0]['max_charge'] == 'max_value':
                    if ship_list:
                        max_ship = max(ship_list)
                        # print('max_ship', max_ship)
                        shipping = max_ship
                elif shipping_charges[0]['max_charge'] == 'sum_value':
                    if ship_list:
                        sum_ship = sum(ship_list)
                        # print('sum_ship', sum_ship)
                        shipping = sum_ship

    context = {
        'shipping': shipping,
        'disp_cont': disp_cont
    }

    return context
# Jatin: code ended


@csrf_exempt
def delete_images(request, pk):
    try:
        req_image = Photo.objects.get(reference_id=pk)
    except Photo.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)
    req_image.delete()
    return JsonResponse({"Deleted": "Deleted"}, safe=False)
# Piyush: code for creating product ends here


# Piyush: code for creating post view for sending data to pflo of reference payment details on 25-11-2020
@receiver(post_save, sender=PaymentReference)
def after_save_payment_details(sender, instance, **kwargs):
    # P: preparing req dict of data to be send
    get_user = None
    if instance.username:
        user = User.objects.filter(email=instance.username)
        get_user = user[0].reference_id or None

    req_order = ''
    if instance.order_no:
        order = Order.objects.filter(ref_code=instance.order_no).first()
        if order:
            req_order = order.ref_code

    req_dict = {
        "payment_type": "inbound",
        "payment_method_id": 1,
        "partner_type": "customer",
        "partner_id": get_user,
        "communication": req_order or 'HMOrder',
        "amount": instance.amount or 0.0,
        "journal_id": 10,  # sending int value directly for picking up bank IRN option
    }

    # P: establishing connection
    url = settings.URL_PATH
    db = settings.DATABASE
    username = settings.USERNAME
    password = settings.PASSWORD

    # P: code for authenticating user data
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
    uid = common.authenticate(db, username, password, {})

    # P: searching for user if already exist in pflo
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)

    try:
        created_id = models.execute_kw(db, uid, password, 'account.payment', 'create', [req_dict])  # id
        created_instance = PaymentReference.objects.get(id=instance.id)
        created_instance.reference_id = created_id  # change field
        created_instance.save()  # this will update reference id in hoity with id of item created in pflo
    except Exception as e:
        print("Exception in Adding Payment reference is : ", e)
# code ends here


# Piyush: code for creating shipping charges on 15dec
@api_view(['POST'])
def create_shipping_charge(request):
    if request.method == 'POST':
        data = request.data
        serializer = ShippingChargesSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            instance_id = list(ShippingCharges.objects.filter(
                reference_id=serializer.data['reference_id']).values('id'))
            reference_id = instance_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_shipping_charge(request, pk):
    try:
        req_instance = ShippingCharges.objects.get(id=pk)
    except ShippingCharges.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":

        serializer = ShippingChargesSerializer(instance=req_instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Piyush: code for creating shipping charges on 15dec ends here


# Piyush: code for creating shipping charges on 16dec
@api_view(['POST'])
def create_shipping_product(request):
    if request.method == 'POST':
        data = request.data
        serializer = ShippingProductSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            instance_id = list(ShippingProduct.objects.filter(
                reference_id=serializer.data['reference_id']).values('id'))
            reference_id = instance_id[0]
            return JsonResponse(reference_id, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_shipping_product(request, pk):
    try:
        req_instance = ShippingProduct.objects.get(id=pk)
    except ShippingProduct.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == "PUT":
        serializer = ShippingProductSerializer(instance=req_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Piyush: code for creating shipping charges on 15dec ends here
