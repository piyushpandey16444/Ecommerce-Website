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

# Piyush: code for import statements for sending mails
from datetime import datetime, timedelta

import json
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# def gen_links():
#     faq_items = Faq.objects.filter(country=1, status='active')
#     testimonials_items = Testimonials.objects.filter(country=1, status='active')
#     disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
#     privacy_items = Privacypolicy.objects.filter(country=1, status='active')
#     terms_items = Terms.objects.filter(country=1, status='active')

#     context = {'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items}
#     return context


def get_categ_and_subcateg():
    categories = Categories.objects.filter(country=1, parent_category=None)
    categ_dict = {}
    for categ in categories:
        c_list = Categories.objects.filter(parent_category=categ, country=1, status='active').values()
        categ_dict[categ] = c_list
    return categ_dict


def index(request):
    sliders = HomePageSlider.objects.filter(country=1, status='active').order_by('-id')
    # advertise = HomePageAdvertise.objects.filter(country=1, status='active')[:1]
    advertise = HomePageAdvertise.objects.filter(country=1, status='active').order_by('-id')
    categories = Categories.objects.filter(country=1, status='active')[:3]
    videos = Homevideo.objects.filter(country=1, status='active')[:1]

    faq_items = Faq.objects.filter(country=1, status='active')
    testimonials_items = Testimonials.objects.filter(country=1, status='active')
    disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
    privacy_items = Privacypolicy.objects.filter(country=1, status='active')
    terms_items = Terms.objects.filter(country=1, status='active')

    context = {'videos': videos, 'sliders': sliders, 'advertise':advertise, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'categories':categories, 'child_categ': get_categ_and_subcateg()}
    return render(request, "hoitymoppet/master.html", context)


def category_wise_products(request, id):
    product_cat = get_object_or_404(Categories, id=id)
    print("product_cat ................", product_cat)

    # allprods = Product.objects.all()
    # allprods = get_object_or_404(Product, id=id)
    # print("allprodssssssssssssssssssssssssssssssss", allprods)

    products = Product.objects.filter(categories=id, country=1, status=1).order_by('-id')

    faq_items = Faq.objects.filter(country=1, status='active')
    testimonials_items = Testimonials.objects.filter(country=1, status='active')
    disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
    privacy_items = Privacypolicy.objects.filter(country=1, status='active')
    terms_items = Terms.objects.filter(country=1, status='active')

    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    
    # Code for on mouse over image on category page 27/04/2020
    prod_photos_all = Photo.objects.filter(product=id)
    print("prod_photos_alllllllllllllllllllllllllllllllllllllllll", prod_photos_all)
    # End


    photos = []
    #####abhishek start 7-5-2020
    wishlist_product_user_wise_list = []
    #####abhishek end7-5-2020
    
    for product in products:
        photos.append({product:Photo.objects.filter(product=product)})

        # prod_photos = Photo.objects.filter(product=product)

        #####abhishek start 7-5-2020
        if request.user.id:
            wishlist_product_user_wise = UserWishList.objects.filter(product_id=product.id, user=request.user)
            if wishlist_product_user_wise:
                wishlist_product_user_wise_list.append(product.id)
        #####abhishek end7-5-2020
    categories = Categories.objects.filter(country=1, parent_category=None)
    categ_dict = {}
    for categ in categories:
        c_list = Categories.objects.filter(parent_category=categ, country=1, status='active')
        categ_dict[categ]= c_list
    context = {'product_cat': product_cat, 'products': products, 'categories':categories, 'photos': photos, 'prod_photos_all':prod_photos_all, 'child_categ':categ_dict, 'disable_attr': wishlist_product_user_wise_list, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items}
    # print("productttttttttttttttttttttttddddddd", context.get('products')[0].slug)
    return render(request, "hoitymoppet/category-wise-products.html", context)


def price_wise_products_low(request, id):
    product_cat = get_object_or_404(Categories, id=id)
    products = Product.objects.filter(categories=id, status=1).order_by('discount_price')

    faq_items = Faq.objects.filter(country=1, status='active')
    testimonials_items = Testimonials.objects.filter(country=1, status='active')
    disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
    privacy_items = Privacypolicy.objects.filter(country=1, status='active')
    terms_items = Terms.objects.filter(country=1, status='active')
 
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
 
    photos = []
    for product in products:
        photos.append({product: Photo.objects.filter(product=product)})
    categories = Categories.objects.filter(country=1, parent_category=None)
    categ_dict = {}
    for categ in categories:
        c_list = Categories.objects.filter(parent_category=categ)
        categ_dict[categ] = c_list
    context = {'product_cat': product_cat, 'products': products, 'categories': categories, 'photos': photos,
               'child_categ': categ_dict, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 
               'privacy_items':privacy_items, 'terms_items':terms_items}
    return render(request, "hoitymoppet/category-wise-products.html", context)


def price_wise_products_high(request, id):
    product_cat = get_object_or_404(Categories, id=id)
    products = Product.objects.filter(categories=id, status=1).order_by('-discount_price')

    faq_items = Faq.objects.filter(country=1, status='active')
    testimonials_items = Testimonials.objects.filter(country=1, status='active')
    disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
    privacy_items = Privacypolicy.objects.filter(country=1, status='active')
    terms_items = Terms.objects.filter(country=1, status='active')
 
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
 
    photos = []
    for product in products:
        photos.append({product: Photo.objects.filter(product=product)})
    categories = Categories.objects.filter(country=1, parent_category=None)
    categ_dict = {}
    for categ in categories:
        c_list = Categories.objects.filter(parent_category=categ)
        categ_dict[categ] = c_list
    context = {'product_cat': product_cat, 'products': products, 'categories': categories, 'photos': photos,
               'child_categ': categ_dict, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 
               'privacy_items':privacy_items, 'terms_items':terms_items}
    return render(request, "hoitymoppet/category-wise-products.html", context)


def price_wise_products_low_twofive(request, id):
    product_cat = get_object_or_404(Categories, id=id)
    products = Product.objects.filter(categories=id, status=1)

    faq_items = Faq.objects.filter(country=1, status='active')
    testimonials_items = Testimonials.objects.filter(country=1, status='active')
    disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
    privacy_items = Privacypolicy.objects.filter(country=1, status='active')
    terms_items = Terms.objects.filter(country=1, status='active')
 
    paginator = Paginator(products, 25)
    page = request.GET.get('page')
    products = paginator.get_page(page)
 
    photos = []
    for product in products:
        photos.append({product: Photo.objects.filter(product=product)})
    categories = Categories.objects.filter(country=1, parent_category=None)
    categ_dict = {}
    for categ in categories:
        c_list = Categories.objects.filter(parent_category=categ)
        categ_dict[categ] = c_list
    context = {'product_cat': product_cat, 'products': products, 'categories': categories, 'photos': photos,
               'child_categ': categ_dict, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 
               'privacy_items':privacy_items, 'terms_items':terms_items}
    return render(request, "hoitymoppet/category-wise-products.html", context)


def price_wise_products_low_fivezero(request, id):
    product_cat = get_object_or_404(Categories, id=id)
    products = Product.objects.filter(categories=id, status=1)

    faq_items = Faq.objects.filter(country=1, status='active')
    testimonials_items = Testimonials.objects.filter(country=1, status='active')
    disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
    privacy_items = Privacypolicy.objects.filter(country=1, status='active')
    terms_items = Terms.objects.filter(country=1, status='active')
 
    paginator = Paginator(products, 50)
    page = request.GET.get('page')
    products = paginator.get_page(page)
 
    photos = []
    for product in products:
        photos.append({product: Photo.objects.filter(product=product)})
    categories = Categories.objects.filter(country=1, parent_category=None)
    categ_dict = {}
    for categ in categories:
        c_list = Categories.objects.filter(parent_category=categ)
        categ_dict[categ] = c_list
    context = {'product_cat': product_cat, 'products': products, 'categories': categories, 'photos': photos,
               'child_categ': categ_dict, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 
               'privacy_items':privacy_items, 'terms_items':terms_items}
    return render(request, "hoitymoppet/category-wise-products.html", context)


@require_http_methods(['GET'])
def productsearch(request):

    faq_items = Faq.objects.filter(country=1, status='active')
    testimonials_items = Testimonials.objects.filter(country=1, status='active')
    disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
    privacy_items = Privacypolicy.objects.filter(country=1, status='active')
    terms_items = Terms.objects.filter(country=1, status='active')

    q = request.GET.get('q')
    if q:
        products = Product.objects.filter(product_name__icontains=q, country=1, status=1)
        return render(request, 'hoitymoppet/search-results.html', {'products': products, 'query': q, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 
               'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()})
    return render(request, "hoitymoppet/search-results.html" ,{'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 
               'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()})


#####abhishek 13-5-2020 Used to calculate sum of discount price
def cart_items_discount_price_total(cart_items):
    total_discount_price = 0.0
    if cart_items:
        for cart in cart_items:
            # print ("SSSSSSS",cart.get_total_discount_item_price())
            total_discount_price = total_discount_price + cart.get_total_discount_item_price()
            # print ("PPPPPPPPPPPPPQQQQ",cart.product_id.discount_price, cart.quantity )

    return total_discount_price
#####abhishek 13-5-2020 Used to calculate sum of discount price


#####abhishek start 12-6-2020
def coupon_apply(request):
    coupon_id = ''
    if request.POST:
        coupon_code = request.POST.get('couponcode')
        print ("GGGGGGGGGGGGGGGGGGGGG",coupon_code)
        coupon_id_get = Coupon.objects.filter(code=coupon_code)
        print ("HHHHHHHHHH",coupon_id_get)
        if coupon_id_get:
            coupon_id = str(coupon_id_get[0].id)
    # now = timezone.now()
    # print("ddddddddddddddddddddddddddddddddddddddddd...........4,request.POST",request.POST)
    # form = CouponApplyForm(request.POST)
    # if form.is_valid():
    #     code = form.cleaned_data['code']
    #     try:
    #         coupon =  Coupon.objects.get(code__iexact=code, valid_form__lte=now, valid_to__gte=now, active=True)
    #         request.session['coupon_id'] = coupon.id
    #     except:
    #         request.session['coupon_id'] = None
    url = '/hoitymoppet/addtocart/' + '?cpn=' + coupon_id
    return redirect(url)
#####abhishek end 12-6-2020


#####Devashish 04-06-2020 Used to calculate sum of discount price after apply coupon/promo code
# @require_POST
# def coupon_apply(request):
#     now = timezone.now()
#     print("ddddddddddddddddddddddddddddddddddddddddd...........4")
#     form = CouponApplyForm(request.POST)
#     if form.is_valid():
#         code = form.cleaned_data['code']
#         try:
#             coupon =  Coupon.objects.get(code__iexact=code, valid_form__lte=now, valid_to__gte=now, active=True)
#             request.session['coupon_id'] = coupon.id
#         except:
#             request.session['coupon_id'] = None
#     return redirect("addtocart")
#####Devashish 04-06-2020 Used to calculate sum of discount price after apply coupon/promo code


@login_required
def add_to_cart(request):

    faq_items = Faq.objects.filter(country=1, status='active')
    testimonials_items = Testimonials.objects.filter(country=1, status='active')
    disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
    privacy_items = Privacypolicy.objects.filter(country=1, status='active')
    terms_items = Terms.objects.filter(country=1, status='active')

    #####abhishek start 12-6-2020 get coupon code from url sent from addtocart page Apply Button
    coupon = ''
    coupon_code = ''
    msg = ''
    coupon_dicount_amt = 0.0
    
    #####abhishek start 12-6-2020 get coupon code from url sent from addtocart page Apply Button
    items = UserCart.objects.filter(user=request.user)
    # for item in items:
    #     if item.product_size == 'custom-size':
    #         print("the custom size of item is", item.user_custom_size)
    #         user_custom = item.user_custom_size.split('(')[0].strip()
    #         print("the final custom size is", user_custom)
            

    #####abhishek 13-5-2020 Used to calculate sum of discount price
    total_discount_price = cart_items_discount_price_total(items) or 0.0
    subtotal = cart_items_discount_price_total(items) or 0.0
    #####abhishek 13-5-2020 Used to calculate sum of discount price

    #####abhishek start 12-6-2020 get coupon code from url sent from addtocart page Apply Button
    print ("FFFFFFFFF",request.GET)
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
                    if local_dt >= valid_from and local_dt <= valid_to:
                        if coupon_code_rec[0].discount_type == 'Fixed':
                            coupon_dicount_amt = coupon_code_rec[0].discount
                        elif coupon_code_rec[0].discount_type == 'Percentage':
                            coupon_dicount_amt = (total_discount_price * coupon_code_rec[0].discount) / 100
                        subtotal = total_discount_price - coupon_dicount_amt
                    else:
                        msg = 'Coupon is not between the Valid Date !'
                else:
                    msg = 'Your coupon is not active !'
            else:
                msg = 'Invalid Coupon !'
        else:
            msg = 'Invalid Coupon !'
    messages.info(request, msg)

    return render(request, "hoitymoppet/shopping-cart.html", {'items': items, 'coupon_code': coupon_code, 'coupon': coupon, 
        'coupon_dicount_amt': coupon_dicount_amt, 'total_discount_price': total_discount_price, 'subtotal': subtotal, 
        'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 
        'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()})


# Cart Functionalities
@login_required
def add_product_to_cart(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product_size = request.POST.get('size', '')
        print("the value in the product size isssssssssssssssssss", product_size)
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


@login_required
def add_product_to_cart_wishlist(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product_size = request.POST.get('size', '')
        user_custom_size = request.POST.get('usercustomsizes', '')
        product_color = request.POST.get('product_color', '')

        print("the value in the product size istttttttttttttttt", product_size)
        print("user_custom_sizeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", user_custom_size)
        print("product_colorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr", product_color)

        item_in_cart = UserCart.objects.get_or_create(
            user=user,
            product_id=product,
            product_size=product_size,
            user_custom_size=user_custom_size,
            product_color=product_color,
            ordered=False
        )
        item_in_cart[0].quantity += 1
        item_in_cart[0].save()
        messages.info(request, "Item added/updated into Cart")
        return redirect(request.META.get('HTTP_REFERER'), product.id)


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


@login_required
def productdetails(request, slug):
    
    # print("the value in the slug is", slug)
    product_details = get_object_or_404(Product, slug=slug)
    id = Product.objects.filter(slug = slug)[0].id
    
    faq_items = Faq.objects.filter(country=1, status='active')
    testimonials_items = Testimonials.objects.filter(country=1, status='active')
    disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
    privacy_items = Privacypolicy.objects.filter(country=1, status='active')
    terms_items = Terms.objects.filter(country=1, status='active')

    # For user custom size
    if request.user.is_authenticated:
        items = UserCustomSize.objects.filter(user=request.user)
    else:
        print("items....................")
    # End

    prod_cat = Categories.objects.all()
    print("prod_cat ........................", prod_cat)

    # For related products
    relatedprodsall = Producttype.objects.filter(product=id)
    print("relatedprodsall ............................", relatedprodsall)
    
    relatedprods = Product.objects.filter(product_type=relatedprodsall[0]).order_by('-id')
    print("relatedprods ............................", relatedprods)
    # End

    # For recently viewed products
    current_date = datetime.now()
    previous_date = current_date + relativedelta(months=-4)
    user = request.user
    product = get_object_or_404(Product, id=id)
    if not Recenltyviewedproducts.objects.filter(user=user, product_id=product).exists():
        recently_viewed_products = Recenltyviewedproducts(user=user, product_id=product)
        recently_viewed_products.save()

    if request.user.is_authenticated:    
        # recentlyviewed = Recenltyviewedproducts.objects.filter(user=request.user).order_by('-id')
        # print("recentlyviewed ............................", recentlyviewed)
        # recentlyviewed = Recenltyviewedproducts.objects.filter(Q(user = request.user) | Q(view_date__gte =previous_date, view_date__lte=current_date)).order_by('-id')
        recentlyviewed = Recenltyviewedproducts.objects.filter(Q(user= request.user) & Q(view_date__range=[previous_date, current_date])).order_by('-id')
    else:
        print("items....................")
    # End

    prod_photos = Photo.objects.filter(product=id)
    categories = Categories.objects.filter(country=1, parent_category=None)
    # print("categories ........................", categories)
    return render(request, "hoitymoppet/product-details.html", context={'product_details': product_details, 'relatedprods':relatedprods, 'recentlyviewed': recentlyviewed, 'child_categ': get_categ_and_subcateg(), 'photos':prod_photos, 'items': items, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items})


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

    faq_items = Faq.objects.filter(country=1, status='active')
    testimonials_items = Testimonials.objects.filter(country=1, status='active')
    disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
    privacy_items = Privacypolicy.objects.filter(country=1, status='active')
    terms_items = Terms.objects.filter(country=1, status='active')

    count = items.count()
    return render(request, "hoitymoppet/product-wishlist.html",{'child_categ': get_categ_and_subcateg(), 'items': items, 
        'usercustomsizes':usercustomsizes, 'count': count, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 
        'privacy_items':privacy_items, 'terms_items':terms_items})


@login_required
def addWishList(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    id = Product.objects.filter(slug = slug)[0].id
    
    if not UserWishList.objects.filter(product_id=product).exists():
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
    return redirect(request.META.get('HTTP_REFERER'))


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
    tracking_status = []
    print ("AAAAAAAAAAAAAAAAA")
    if order_id:
        print ("BBBBBBBBBBBBBBBB")
        order_id = order_id[0]
        tracking_status = TrackingStatus.objects.filter(order_id=order_id)
        print ("GGGGGGGGGGG",tracking_status)
    return render(request, "hoitymoppet/tracker.html", {'child_categ': get_categ_and_subcateg(), 'order': order_id, 'tracking_status': tracking_status})


# def hoitymoppetlookbook(request):
#     lookbooks = Lookbook.objects.all()
#     lookbookcategories = Lookbookcategories.objects.all()
#     context = {'lookbooks':lookbooks, 'lookbookcategories':lookbookcategories, 'child_categ': get_categ_and_subcateg()}
#     return render(request, "hoitymoppet/hoitymoppet-look-book.html", context)


def hoitymoppetlookbook(request):
    lookbooks = Lookbookcategories.objects.filter(country=1, status='active')
    lookbookcategories = Lookbookcategories.objects.all()

    faq_items = Faq.objects.filter(country=1, status='active')
    testimonials_items = Testimonials.objects.filter(country=1, status='active')
    disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
    privacy_items = Privacypolicy.objects.filter(country=1, status='active')
    terms_items = Terms.objects.filter(country=1, status='active')

    context = {'lookbooks':lookbooks, 'lookbookcategories':lookbookcategories, 'child_categ': get_categ_and_subcateg(), 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items}
    return render(request, "hoitymoppet/hoitymoppet-look-book.html", context)


# def hoitymoppetlookbookdetails(request, id):
#     lookbookdetails = Lookbook.objects.get(id=id)
#     categories = Categories.objects.filter(country=1, parent_category=None)
#     return render(request, "hoitymoppet/hoitymoppet-look-book-details.html", context={'lookbookdetails': lookbookdetails, 'categories':categories})


def hoitymoppetlookbookdetails(request, id):
    
    lookbook_cat = get_object_or_404(Lookbookcategories, id=id)
    print("lookbook_cat ......................", lookbook_cat)

    faq_items = Faq.objects.filter(country=1, status='active')
    testimonials_items = Testimonials.objects.filter(country=1, status='active')
    disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
    privacy_items = Privacypolicy.objects.filter(country=1, status='active')
    terms_items = Terms.objects.filter(country=1, status='active')

    lookbookdetails = Product.objects.filter(lookbook_category=id, status=1)
    return render(request, "hoitymoppet/hoitymoppet-look-book-details.html", context={'lookbook_cat':lookbook_cat, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'lookbookdetails': lookbookdetails, 'child_categ': get_categ_and_subcateg()})


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


def categorydetails(request, id):
    categorydetails = Product.objects.filter(category=id, status=1)
    return render(request, "hoitymoppet/category-wise-products.html", context={'categorydetails': categorydetails, 'child_categ': get_categ_and_subcateg()})


# def ordercompleted(request):

#     faq_items = Faq.objects.filter(country=1, status='active')
#     testimonials_items = Testimonials.objects.filter(country=1, status='active')
#     disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
#     privacy_items = Privacypolicy.objects.filter(country=1, status='active')
#     terms_items = Terms.objects.filter(country=1, status='active')

#     user = request.user
#     #####abhishek 21-5-2020 Work on 'Place Your Order' button functionality
#     print ("AAAAAAAAAAAAAAA",request.method, request.GET)
#     #Get Address
#     address = []
#     generated_order_detail_list = []
#     generated_order = ''
#     if request.GET and request.GET.get('addr'):
#         print ("FFFFFFFFF",UserCart.objects.filter(user=request.user))
#         delivery_address = Address.objects.filter(user=request.user, id=request.GET.get('addr'))
#         if delivery_address:
#             address = delivery_address[0]
#     if request.method == 'POST':
#         cart_items = UserCart.objects.filter(user=request.user)
#         if cart_items:
            
#             #Create Order start
#             order_no = 1
#             prev_created_orders = Order.objects.filter()
#             if prev_created_orders:
#                 order_no = len(prev_created_orders) + 10
#             ref_code = 'ArkeOrderNo'+ str(order_no)
#             print("generateeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", ref_code)
#             generated_order = Order.objects.create(
#                 user=user,
#                 ref_code=ref_code,
#                 address_id=address,
#                 #####abhishek start 29-5-2020
#                 status_name='Confirm',
#                 #####abhishek end 29-5-2020
#             )
#             # Create Order end

#             if generated_order:
#                 # Create Order Detail and Delete Cart Item one by one after order placed - start
#                 for cart in cart_items:
#                     create_order_detail = OrderDetail.objects.create(
#                         user=user,
#                         order_id= generated_order,
#                         product_id=cart.product_id,
#                         quantity=cart.quantity,
#                         price=cart.product_id.discount_price,
#                         total_price=cart.quantity * cart.product_id.discount_price,
#                         product_size=cart.product_size,
#                         user_custom_size=cart.user_custom_size,
#                         product_color=cart.product_color,
#                     )
#                     generated_order_detail_list.append(create_order_detail)

#                     cart.delete()
#                 # Create Order Detail and Delete Cart Item one by one after order placed - end

#                 # Create Tracking Status as Confirm - start
#                 tracking_status = TrackingStatus.objects.create(
#                     user=user,
#                     order_id=generated_order,
#                     status_name='Confirm',
#                     description='Order Confirm'
#                     )
#                 # Create Tracking Status as Confirm - end
#                 current_site = get_current_site(request)
#                 print(current_site)
#                 # mail_subject = 'Activate your account'
#                 message = {
#                     'user': user,
#                     'domain': current_site.domain,
#                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                     # 'token': account_activation_token.make_token(user),   
#                 }
            
#                 # TODO: Add more useful commands here.
                
#                 print(message)
#                 current_user = User.objects.get(id=request.user.id)
                
#                 to_email =  current_user.email
#                 print(to_email)
#                 email = EmailMessage('etemplate/acc_activate_email.tpl',message,'nautiyalakshat11@gmail.com',to=[to_email])
                

#                 print(email)
#                 email.send()
#                 #####abhishek start 13-6-2020 get coupon code from url sent from addtocart page Apply Button
#                 if request.GET:
#                     if request.GET.get('cpn'):
#                         coupon = request.GET.get('cpn')
#                         coupon_id = int(coupon)
#                         coupon_code_rec = Coupon.objects.filter(id=coupon_id)
#                         if coupon_code_rec:
#                             coupon_history = CouponHistory.objects.create(
#                                 user=user,
#                                 order_id=generated_order,
#                                 coupon_id=coupon_code_rec[0],
#                             )
#                             print ("CCCCCCCCCCCCCCCCCC",coupon_code_rec[0].customer.all())
#                             coupon_code_rec[0].customer.remove(user)
#                             print("DDDDDDDDDDDDDDDDDDD", coupon_code_rec[0].customer.all())
#                 #####abhishek end 13-6-2020 get coupon code from url sent from addtocart page Apply Button
                
#                 return render(request, "hoitymoppet/order-completed.html", context={'generated_order': generated_order, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 
#                     'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 
#                     'address': address, 'generated_order_detail_list': generated_order_detail_list, 
#                     'child_categ': get_categ_and_subcateg()})
#         else:
#             return HttpResponse("No Item in your Cart !")


def ordercompleted(request):
    user = request.user
    
    #####abhishek 21-5-2020 Work on 'Place Your Order' button functionality
    print ("AAAAAAAAAAAAAAA",request.method, request.GET)
    #Get Address
    address = []
    generated_order_detail_list = []
    generated_order = ''
    if request.GET and request.GET.get('addr'):
        print ("FFFFFFFFF",UserCart.objects.filter(user=request.user))
        delivery_address = Address.objects.filter(user=request.user, id=request.GET.get('addr'))
        if delivery_address:
            address = delivery_address[0]
    ####### SUB TOTAL #########
    
    order_id = []
    order_detail_list = []
    total_price = 0.0
    coupon_dicount_amt = 0.0
    subtotal = 0.0
    order = Order.objects.filter(user=request.user, id=request.GET.get('on'))
    if order:
        order_id = order[0]
        order_detail_list = OrderDetail.objects.filter(user=request.user, order_id=order_id)
        if order_detail_list:
            for ord_detail in order_detail_list:
                total_price += ord_detail.total_price
        #####abhishek start 19-6-2020 getting Coupon Discount Amount
        subtotal = total_price
        coupon_history = CouponHistory.objects.filter(order_id=order_id)
        if coupon_history:
            coupon_id = coupon_history[0].coupon_id
            if coupon_id:
                if coupon_id:
                    coupon_code = coupon_id.code or ''
        
                    if coupon_id.discount_type == 'Fixed':
                        coupon_dicount_amt = coupon_id.discount
                    elif coupon_id.discount_type == 'Percentage':
                        coupon_dicount_amt = (total_discount_price * coupon_id.discount) / 100
                    subtotal = total_price - coupon_dicount_amt
    ####### SUB TOTAL #########        
    if request.method == 'POST':
        cart_items = UserCart.objects.filter(user=request.user)
        if cart_items:
            
            #Create Order start
            order_no = 1
            prev_created_orders = Order.objects.filter()
            if prev_created_orders:
                order_no = len(prev_created_orders) + 10
            ref_code = 'ArkeOrderNo'+ str(order_no)
            generated_order = Order.objects.create(
                user=user,
                ref_code=ref_code,
                address_id=address,
                #####abhishek start 29-5-2020
                status_name='Confirm',
                #####abhishek end 29-5-2020
            )
            # Create Order end

            if generated_order:
                # Create Order Detail and Delete Cart Item one by one after order placed - start
                for cart in cart_items:
                    create_order_detail = OrderDetail.objects.create(
                        user=user,
                        order_id= generated_order,
                        product_id=cart.product_id,
                        quantity=cart.quantity,
                        price=cart.product_id.discount_price,
                        total_price=cart.quantity * (cart.product_id.discount_price or cart.product_id.price),
                        product_size=cart.product_size,
                        user_custom_size=cart.user_custom_size,
                        product_color=cart.product_color,
                    )
                    generated_order_detail_list.append(create_order_detail)

                    cart.delete()
                # Create Order Detail and Delete Cart Item one by one after order placed - end

                # Create Tracking Status as Confirm - start
                tracking_status = TrackingStatus.objects.create(
                    user=user,
                    order_id=generated_order,
                    status_name='Confirm',
                    description='Order Confirm'
                    )
                # Create Tracking Status as Confirm - end
                current_site = get_current_site(request)
                print(current_site)
                # mail_subject = 'Activate your account'
                message = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'generated_order': generated_order,
                    'generated_order_detail_list': generated_order_detail_list,
                    
                    'order_detail_list':order_detail_list,
                     
                    
                    'address': address,
                    # 'token': account_activation_token.make_token(user),   
                }
            
                # TODO: Add more useful commands here.
                
                print(message)
                current_user = User.objects.get(id=request.user.id)
                
                to_email =  current_user.email
                print(to_email)
                email = EmailMessage('etemplate/acc_activate_email.tpl',message,'assistwebtech@gmail.com',to=[to_email])
                

                print(email)
                email.send()
                #####abhishek start 13-6-2020 get coupon code from url sent from addtocart page Apply Button
                if request.GET:
                    if request.GET.get('cpn'):
                        coupon = request.GET.get('cpn')
                        coupon_id = int(coupon)
                        coupon_code_rec = Coupon.objects.filter(id=coupon_id)
                        if coupon_code_rec:
                            coupon_history = CouponHistory.objects.create(
                                user=user,
                                order_id=generated_order,
                                coupon_id=coupon_code_rec[0],
                            )
                            print ("CCCCCCCCCCCCCCCCCC",coupon_code_rec[0].customer.all())
                            coupon_code_rec[0].customer.remove(user)
                            print("DDDDDDDDDDDDDDDDDDD", coupon_code_rec[0].customer.all())
                #####abhishek end 13-6-2020 get coupon code from url sent from addtocart page Apply Button
                
                return render(request, "hoitymoppet/order-completed.html", context={'generated_order': generated_order, 'address': address, 'generated_order_detail_list': generated_order_detail_list, 'child_categ': get_categ_and_subcateg()})
        else:
            return HttpResponse("No Item in your Cart !")


#####abhishek start 29-5-2020
def change_status(request, id):
    order_id = Order.objects.get(id=id)
    current_status = order_id and order_id.status_name or ''
    return render(request, "hoitymoppet/change_status.html", context={'order_id': order_id, 'current_status': current_status})

def change_status_done(request, id):
    if request.method == 'POST':
        status_to_change = request.POST.get('status_to_change','')
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


            # Piyush: code for sending mail on change of order status on 06-08-2020

            # getting required order
            order = Order.objects.get(id=id)
            details = OrderDetail.objects.get(order_id=order)

            message = {'order': order, 'details': details}

            # getting user email id for sending mail
            req_user = User.objects.get(username=order.user)
            req_email = req_user.email
            if req_email:
                email = EmailMessage('etemplate/status-change-mail.tpl', message, settings.EMAIL_HOST_USER,
                                     [req_email])
                email.send()

            # code ends here

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
    context= {'cares':cares}
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


@login_required
def checkout(request):

    faq_items = Faq.objects.filter(country=1, status='active')
    testimonials_items = Testimonials.objects.filter(country=1, status='active')
    disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
    privacy_items = Privacypolicy.objects.filter(country=1, status='active')
    terms_items = Terms.objects.filter(country=1, status='active')

    # user_address = Product.objects.all()
    # print("user_addressssssssssssssssssssssssssssssss", user_address)
    # print("This is chekoutpage ........................................")

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
        city = request.POST.get('city')
        landmark = request.POST.get('landmark')
        alternate_no = request.POST.get('alternate_no')
        if not id:
            if name and mobile_no:
                addres = {
                    'user':request.user,
                    'name': name,
                    'mobile_no':mobile_no,
                    'pincode':pincode,
                    'locality':locality,
                    'address':address,
                    'state':state,
                    'city':city,
                    'landmark':landmark,
                    'alternate_no':alternate_no,
                }
                address = Address(**addres)
                address.save()
                objs = Address.objects.filter(user=request.user)
                return render(request, 'hoitymoppet/checkout.html', context={'addresses':objs, 'total_discount_price': total_discount_price, 
                    'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 
                    'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()})
        else:
            addr = get_object_or_404(Address, id=id)
            addr.name = name
            addr.mobile_no = mobile_no
            addr.pincode = pincode
            addr.locality = locality
            addr.address = address
            addr.state = state
            addr.city = city
            addr.landmark = landmark
            addr.alternate_no = alternate_no
            addr.save()
            objs = Address.objects.filter(user=request.user)
            return render(request, 'hoitymoppet/checkout.html', context={'addresses': objs, 'total_discount_price': total_discount_price, 'faq_items':faq_items, 
                'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 
                'child_categ': get_categ_and_subcateg()})
    objs = Address.objects.filter(user=request.user)
    print("objsssssssssssssssssssssssssssssssssssssssssss", objs)

    #####abhishek start 13-6-2020 get coupon code from url sent from addtocart page Apply Button
    if request.GET:
        if request.GET.get('cpn'):
            coupon = request.GET.get('cpn')
            coupon_id = int(coupon)
            coupon_code_rec = Coupon.objects.filter(id=coupon_id)
            if coupon_code_rec:
                coupon_code = coupon_code_rec[0].code or ''
    
                if coupon_code_rec[0].discount_type == 'Fixed':
                    coupon_dicount_amt = coupon_code_rec[0].discount
                elif coupon_code_rec[0].discount_type == 'Percentage':
                    coupon_dicount_amt = (total_discount_price * coupon_code_rec[0].discount) / 100
                subtotal = total_discount_price - coupon_dicount_amt
    #####abhishek end 13-6-2020 get coupon code from url sent from addtocart page Apply Button
    
    return render(request, "hoitymoppet/checkout.html", {'addresses': objs, 'coupon': coupon, 'coupon_code': coupon_code, 
        'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 
        'terms_items':terms_items, 'coupon_dicount_amt': coupon_dicount_amt, 'subtotal': subtotal, 'total_discount_price': total_discount_price, 
        'child_categ': get_categ_and_subcateg()})


@login_required
def deliverymethod(request):

    faq_items = Faq.objects.filter(country=1, status='active')
    testimonials_items = Testimonials.objects.filter(country=1, status='active')
    disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
    privacy_items = Privacypolicy.objects.filter(country=1, status='active')
    terms_items = Terms.objects.filter(country=1, status='active')

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
                    coupon_dicount_amt = coupon_code_rec[0].discount
                elif coupon_code_rec[0].discount_type == 'Percentage':
                    coupon_dicount_amt = (total_discount_price * coupon_code_rec[0].discount) / 100
                subtotal = total_discount_price - coupon_dicount_amt
    #####abhishek end 13-6-2020 get coupon code from url sent from addtocart page Apply Button
    
    return render(request, "hoitymoppet/delivery-method.html", {'address': address, 'items': items, 
        'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 
        'privacy_items':privacy_items, 'terms_items':terms_items, 'coupon': coupon, 'coupon_code': coupon_code, 
        'coupon_dicount_amt': coupon_dicount_amt, 'subtotal': subtotal, 'total_discount_price': total_discount_price, 
        'child_categ': get_categ_and_subcateg()})


@login_required
def paymentmethod(request):

    faq_items = Faq.objects.filter(country=1, status='active')
    testimonials_items = Testimonials.objects.filter(country=1, status='active')
    disclaimer_items = Disclaimer.objects.filter(country=1, status='active')
    privacy_items = Privacypolicy.objects.filter(country=1, status='active')
    terms_items = Terms.objects.filter(country=1, status='active')

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
    
    return render(request, "hoitymoppet/payment-method.html", {'address': address, 'coupon': coupon, 'coupon_code': coupon_code, 
        'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 
        'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()})


def singleorderconfirmation(request):
    context= {'child_categ': get_categ_and_subcateg()}
    return render(request, "etemplate/single-order-confirmation.html", context)

def multiorderconfirmation(request):
    context= {'child_categ': get_categ_and_subcateg()}
    return render(request, "etemplate/multi-order-confirmation.html", context)

def userconfirmation(request):
    context= {'child_categ': get_categ_and_subcateg()}
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

                        message = {'items': user_item}

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
#         print("sizeeeeeeeeeeeeeeeeeeeeeeeeeee in post", size)
#         custom_size = Age.objects.filter(age = size)
#         if custom_size:
#             age = custom_size[0].id
#             print("the value in the cusotm size is", custom_size)
#             print(age)
#             data = Measurements.objects.filter(age = age)
#             serialized_data = json.loads(serialize('json', data))
#             return JsonResponse({'data': serialized_data})

@csrf_exempt
def getcustomsize(request):
    if request.is_ajax and request.method == "POST":
        size = request.POST.get('size_val', None)
        custom_size = Age.objects.filter(age = size)
        if custom_size:
            age = custom_size[0].id
            data = Measures.objects.filter(age = age).values()
            val_list =[]
            print("The value in  the data is",data)
            for values in data:
                for key,value in values.items():
                    master = values['mesure_name_id']
                    master_name = Measurement_Master.objects.get(id=master).name
                val_list.append({'master_name':master_name,'stand_value':values['value']})
            print("The vlue in hte list is",val_list)
            # serialized_data = json.loads(serialize('json', data))
            print("ddddddddddddddddddddddddddddddddddd", json.dumps(val_list))
            return JsonResponse(json.dumps(val_list), safe = False)
        else:
            return JsonResponse({'data':'No Data Found'})



@csrf_exempt
def GetUserCustomSize(request):
    if request.is_ajax and request.method == "POST":
        size = request.POST.get('size_val', None)
        # print("sizeeeeeeeeeeee zzzzzzzzzzzz eeeeeeeeeeeeee in post", size)
        age = Age.objects.filter(age = size)[0]
        # print("ageeeeeeeeeeeee 5555555555 eeeeeeeeeeeeee in post", age)
        user = request.user
        # print("userrrrrrrrrrrrrrrrr 5555555555 eeeeeeeeeeeeee in post", user)
        # custom_size = UserCustomSize.objects.filter(user=user)
        custom_size = UserCustomMeasures.objects.filter(user=user)
        # print("custom_sizeeeeeeeeeeee 5555555555 eeeeeeeeeeeeee in post", custom_size)
        if custom_size:
            serialized_data = json.loads(serialize('json', custom_size))
            return JsonResponse({'data': serialized_data})



@login_required
@csrf_exempt
def add_user_custom_size(request):
    if request.is_ajax and request.method == "POST":
        data_dict = json.loads(request.POST.get('final_values'))

        custom_list = []

        for item in data_dict:
            asize = item.get('size')
            size_id = Age.objects.filter(age=asize)[0]
            # print("the value in hte size id", size_id)
            master = item.get('master_name')
            master_id = Measurement_Master.objects.filter(name=master)[0]
            # print("the value of maste is",master_id)
            measure_id = Measures.objects.filter(age=size_id).filter(mesure_name=master_id)[0]
            # print("dataaaaaaaaaaaaaaaaaaaaaaa", measure_id)
            
            user_custom_size_name = item.get('custom_size_name')
            standard_value = item.get('stand_value')
            custom_value = item.get('cust_value')
            
            vals = {
            'user':request.user,
            'age':size_id,
            'measures':measure_id,
            'user_custom_size_name':user_custom_size_name,
            'standard_value':standard_value,
            'custom_value':custom_value,
            }

            custom_list.append(UserCustomMeasures(**vals))

        obj = UserCustomMeasures.objects.bulk_create(custom_list)
        return JsonResponse({'success':'insertion successful'})