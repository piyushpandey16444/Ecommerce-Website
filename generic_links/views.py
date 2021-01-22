from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Company, AboutUs, Homevideo, Companyphoto, Privacypolicy, Disclaimer, Terms, Enquiry, Faq, Testimonials
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from django.contrib.auth.models import User, Associated_Company

from hoitymoppet.models import Categories, Product, Country, BackgroundImage


def get_categ_and_subcateg():
    categories = Categories.objects.filter(parent_category=None, invisible=False)
    categ_dict = {}
    for categ in categories:
        c_list = Categories.objects.filter(parent_category=categ, status='active').values()
        categ_dict[categ] = c_list
    return categ_dict


def category_wise_products(request, id):
    product_cat = get_object_or_404(Categories, id=id)

    # allprods = Product.objects.all()
    # allprods = get_object_or_404(Product, id=id)

    products = Product.objects.filter(categories=id, status=1).order_by('-id')

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
        photos.append({product:Photo.objects.filter(product=product)})
        #####abhishek start 7-5-2020
        if request.user.id:
            wishlist_product_user_wise = UserWishList.objects.filter(product_id=product.id, user=request.user)
            if wishlist_product_user_wise:
                wishlist_product_user_wise_list.append(product.id)
        #####abhishek end7-5-2020
    categories = Categories.objects.filter(parent_category=None, invisible=False)
    categ_dict = {}
    for categ in categories:
        c_list = Categories.objects.filter(parent_category=categ, status='active')
        categ_dict[categ]= c_list
    context = {'product_cat': product_cat, 'products': products, 'categories':categories, 'photos': photos, 'prod_photos_all':prod_photos_all, 'child_categ':categ_dict, 'disable_attr': wishlist_product_user_wise_list}
    return render(request, "hoitymoppet/category-wise-products.html", context)


def slidersdetails(request, id):
    slidedetails = Product.objects.filter(sliders_category=id, status=1)
    return render(request, "hoitymoppet/category-wise-products.html", context={'slidedetails': slidedetails, 'child_categ': get_categ_and_subcateg()})


def homevideo(request, id):
    homepagevideo = Homevideo.objects.filter(video_category=id, status=1)
    return render(request, "hoitymoppet/category-wise-products.html", context={'homepagevideo': homepagevideo, 'child_categ': get_categ_and_subcateg()})


def advertisedetails(request, id):
    advertisedetails = Product.objects.filter(ads_category=id, status=1)
    return render(request, "hoitymoppet/category-wise-products.html", context={'advertisedetails': advertisedetails, 'child_categ': get_categ_and_subcateg()})


def company(request):
    companies = AboutUs.objects.filter(status='active')
    comp_photos = Companyphoto.objects.filter()

    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter(status='active')
    privacy_items = Privacypolicy.objects.filter(status='active')
    terms_items = Terms.objects.filter(status='active')

    context= {'company_info':company_info, 'companies':companies, 'photos': comp_photos, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()}
    return render(request, "generic_links/company.html", context)


def contactus(request):

    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter(status='active')
    privacy_items = Privacypolicy.objects.filter(status='active')
    terms_items = Terms.objects.filter(status='active')

    if request.method == 'POST':
        fullname = request.POST.get('fullname','')
        contactno = request.POST.get('contactno','')
        email = request.POST.get('email','')
        message = request.POST.get('message','')
        enquiry = Enquiry(fullname=fullname, contactno=contactno, email=email, message=message)
        enquiry.save()
        
        return render(request, "generic_links/success.html", {'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()})
    return render(request, "generic_links/contact-us.html", {'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()})


def privacypolicy(request):
    privacypolicies = Privacypolicy.objects.filter(status='active')
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter(status='active')
    privacy_items = Privacypolicy.objects.filter(status='active')
    terms_items = Terms.objects.filter(status='active')

    context= {'company_info':company_info, 'privacypolicies':privacypolicies, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()}
    return render(request, "generic_links/privacy-policy.html", context)


def disclaimer(request):
    disclaimers = Disclaimer.objects.filter(status='active')
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter(status='active')
    privacy_items = Privacypolicy.objects.filter(status='active')
    terms_items = Terms.objects.filter( status='active')

    context= {'company_info':company_info, 'disclaimers':disclaimers, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()}
    return render(request, "generic_links/disclaimer.html", context)


def termsconditions(request):
    terms = Terms.objects.filter(status='active')
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter(status='active')
    privacy_items = Privacypolicy.objects.filter(status='active')
    terms_items = Terms.objects.filter( status='active')

    context= {'company_info':company_info, 'terms':terms, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()}
    return render(request, "generic_links/terms-conditions.html", context)


def faq(request):
    faqs = Faq.objects.filter(status='active')
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter( status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter(status='active')
    privacy_items = Privacypolicy.objects.filter(status='active')
    terms_items = Terms.objects.filter( status='active')

    bgimg = BackgroundImage.objects.filter(item='faqimage', status='active')

    context= {'company_info':company_info, 'bgimg':bgimg, 'faqs':faqs, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()}
    return render(request, "generic_links/faq.html", context)


def testimonials(request):
    alltestimonials = Testimonials.objects.filter(status='active')
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.filter(status='active')
    testimonials_items = Testimonials.objects.filter(status='active')
    disclaimer_items = Disclaimer.objects.filter(status='active')
    privacy_items = Privacypolicy.objects.filter(status='active')
    terms_items = Terms.objects.filter(status='active')

    bgimg = BackgroundImage.objects.filter(item='testimonialsimage', status='active')

    context= {'company_info':company_info, 'bgimg':bgimg, 'alltestimonials':alltestimonials, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()}
    return render(request, "generic_links/testimonials.html", context)