from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, AddressForm
from django.contrib.auth.models import User, Associated_Company
from accounts.models import *
import datetime
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from hoitymoppet.views import get_categ_and_subcateg
##### Adding Order - start
from hoitymoppet.models import *
from generic_links.models import *
from enquiry_order.models import *
##### Adding Order - end
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.http import HttpResponse
# from django.core.mail import EmailMessage
from mail_templated import EmailMessage
from django.contrib.auth.views import LoginView
from des.models import DynamicEmailConfiguration


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return render(request, 'accounts/user-activation.html',)
    else:
        return HttpResponse('Activation link is invalid or This link is already activated.')    

def signup(request):
    login_img = BackgroundImage.objects.filter(item='loginimage', status='active')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # user.is_active= False
            # Piyush: code for making description dynamic on 28-10-2020
            description = EmailDescription.objects.filter(subject='registration').first()
            # Piyush: code for making description dynamic on 28-10-2020 ends here passed in message
            current_site = get_current_site(request)
            subject = "Activate your account"
            mail_subject = 'Activate your account'
            message = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'description': description,
                'subject': subject,
                'BASE_URL': settings.BASE_URL
            }
            # TODO: Add more useful commands here.
            to_email = form.cleaned_data.get('email')
            config = DynamicEmailConfiguration.get_solo()
            email = EmailMessage('accounts/acc_activate_email.tpl', message, "Do not reply <{}>".format(config.from_email), to=[to_email])

            email.send()
            # login(request, user)
            # return redirect('login')
            # messages.success(request, 'User registration successfully done. Please confirm your email address to complete the registration.')
            # return HttpResponse('Please confirm your email address to complete the registration')
            return render(request, 'accounts/success-registration.html', {'form': form, 'login_img':login_img, 'child_categ': get_categ_and_subcateg()})
    else:
        form = SignUpForm()
    return render(request, './accounts/signup.html', {'form': form, 'login_img':login_img, 'child_categ': get_categ_and_subcateg()})

@login_required
def change_password(request):
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.all()
    testimonials_items = Testimonials.objects.all()
    disclaimer_items = Disclaimer.objects.all()
    privacy_items = Privacypolicy.objects.all()
    terms_items = Terms.objects.all()

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('logout')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form, 'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()
    })


@login_required
def profile(request):
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.all()
    testimonials_items = Testimonials.objects.all()
    disclaimer_items = Disclaimer.objects.all()
    privacy_items = Privacypolicy.objects.all()
    terms_items = Terms.objects.all()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_contact_number = request.POST.get('user_contact_number',0)
        user_sex = request.POST.get('user_sex',False)
        email = request.POST.get('email')
        current_user = User.objects.get(id=request.user.id)
        if current_user:
            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.email = email
            current_user.save()
        profile = Profile.objects.get(user=current_user)
        profile.user_sex = user_sex
        profile.user_contact_number = user_contact_number
        profile.save()
        return redirect('profile')
        # return render(request, './accounts/profile.html', {'company_info':company_info, 'child_categ': get_categ_and_subcateg()})
    return render(request, './accounts/profile.html', {'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()})


# def login(request, user):
#     return render(request, './accounts/login.html', {'child_categ': get_categ_and_subcateg()})


@login_required
def orderhistory(request):
    return render(request, './accounts/order-history.html', {'child_categ': get_categ_and_subcateg()})


@login_required
def changepassword(request):
    return render(request, './accounts/change_password.html', {'child_categ': get_categ_and_subcateg()})


def resetpassword(request):
    return render(request, './accounts/password_reset.html', {'child_categ': get_categ_and_subcateg()})


@login_required
def myorders(request):
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.all()
    testimonials_items = Testimonials.objects.all()
    disclaimer_items = Disclaimer.objects.all()
    privacy_items = Privacypolicy.objects.all()
    terms_items = Terms.objects.all()
    #####abhishek - start - 23-5-2020 Adding Order List
    user_orders = []
    user_orders = Order.objects.filter(user=request.user).order_by('-id')
    #####abhishek - end - 23-5-2020 Adding Order List
    return render(request, './accounts/my-orders.html', {'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'user_orders': user_orders, 'child_categ': get_categ_and_subcateg()})

@login_required
def myorderdetails(request):
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.all()
    testimonials_items = Testimonials.objects.all()
    disclaimer_items = Disclaimer.objects.all()
    privacy_items = Privacypolicy.objects.all()
    terms_items = Terms.objects.all()
    #####abhishek start - 23-5-2020 Send Order Detail to Detail page from Order History page
    ##### abhishek 26-5-2020 adding total_price
    order_id = []
    # coupon_dicount_amt = 0.0
    order_detail_list = []
    total_price = 0.0
    order = Order.objects.filter(user=request.user, id=request.GET.get('on'))
    if order:
        order_id = order[0]
        order_detail_list = OrderDetail.objects.filter(user=request.user, order_id=order_id)

        if order_detail_list:
            for ord_detail in order_detail_list:
                total_price += ord_detail.total_price

        for orders in order:
            shipping_charges = orders.shipping_charges
            if shipping_charges:
                all_total_price = total_price + shipping_charges
            else:
                all_total_price = total_price
    #####abhishek end - 23-5-2020 Send Order Detail to Detail page from Order History page
    return render(request, './accounts/my-order-details.html', {'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'all_total_price': format(all_total_price, '.2f'),'shipping_charges': format(shipping_charges, '.2f') if shipping_charges else shipping_charges,'order': order, 'order_detail_list': order_detail_list, 'total_price':format(total_price, '.2f'), 'child_categ': get_categ_and_subcateg()})


@login_required
def mywishlist(request):
    return render(request, './accounts/my-wishlist.html', {'child_categ': get_categ_and_subcateg()})


@login_required
def manageaddress(request):

    # get default name and number 28-10-2020
    name = ''
    if request.user.first_name and request.user.last_name:
        name = request.user.first_name + " " + request.user.last_name
    elif request.user.first_name:
        name = request.user.first_name
    user_name = name
    contact_number = request.user.profile.user_contact_number

    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.all()
    testimonials_items = Testimonials.objects.all()
    disclaimer_items = Disclaimer.objects.all()
    privacy_items = Privacypolicy.objects.all()
    terms_items = Terms.objects.all()

    country_items = HoityCountry.objects.all()
    state_items = HoityState.objects.filter(country_id_id = 103)

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

        ustate = HoityState.objects.filter(name__iexact = state).first()
        ucountry = HoityCountry.objects.filter(name__iexact = country).first()

        if not id:
            if name and mobile_no:
                addres = {
                    'user':request.user,
                    'name': name,
                    'mobile_no':mobile_no,
                    'pincode':pincode,
                    'locality':locality,
                    'address':address,
                    'user_state':ustate,
                    'user_country':ucountry,
                    'city':city,
                    'landmark':landmark,
                    'alternate_no':alternate_no,
                    'default':default,
                }

                if default:
                    Address.objects.filter(user = request.user, default=True).update(default=False)
                    
                address = Address(**addres)
                address.save()
                objs = Address.objects.filter(user=request.user)
                return render(request, './accounts/manage-address.html', context={'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items,'addresses':objs, 'state_items':state_items, 'country_items':country_items, 'child_categ': get_categ_and_subcateg()})
        else:
            instance_address = Address.objects.filter(id=id)
            if not ustate:
                ustate = instance_address.user_state
            if not ucountry:
                ucountry = instance_address.user_country
            address_dict = {
                'id': id,
                'user': request.user,
                'name': name,
                'mobile_no': mobile_no,
                'pincode': pincode,
                'locality': locality,
                'address': address,
                'user_state': ustate,
                'user_country': ucountry,
                'city': city,
                'landmark': landmark,
                'alternate_no': alternate_no,
                'default': default,
            }

            instance_address = Address.objects.filter(id=id).first()
            instance_address.user = request.user
            instance_address.name = name
            instance_address.mobile_no = mobile_no
            instance_address.pincode = pincode
            instance_address.locality = locality
            instance_address.address = address
            instance_address.user_state = ustate
            instance_address.user_country = ucountry
            instance_address.city = city
            instance_address.landmark = landmark
            instance_address.alternate_no = alternate_no
            instance_address.default = default
            instance_address.save()
            objs = Address.objects.filter(user=request.user)
            return render(request, './accounts/manage-address.html', context={'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'addresses': objs, 'state_items':state_items, 'country_items':country_items, 'child_categ': get_categ_and_subcateg()})
    objs = Address.objects.filter(user=request.user)


    user_orders = Order.objects.filter(user=request.user)
    #print("user_addresssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss", user_orders)

    user_address = Address.objects.filter(user=request.user)
    #print("user_addresssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss", user_address)


    return render(request, './accounts/manage-address.html', context={'user_name': user_name, 'contact_number': contact_number, 'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'user_orders':user_orders, 'user_address':user_address, 'addresses': objs, 'state_items':state_items, 'country_items':country_items, 'child_categ': get_categ_and_subcateg()})


@login_required
def childinformation(request):
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.all()
    testimonials_items = Testimonials.objects.all()
    disclaimer_items = Disclaimer.objects.all()
    privacy_items = Privacypolicy.objects.all()
    terms_items = Terms.objects.all()

    if request.method == 'POST':
        id = request.POST.get('id')
        child_name = request.POST.get('child_name')
        child_birth_date = request.POST.get('child_birth_date')
        if not id:
            if child_name and child_birth_date:
                chil = {
                    'user': request.user,
                    'child_name': child_name,
                    # 'child_birth_date': datetime.datetime.strptime(child_birth_date,'%m/%d/%Y'),
                    'child_birth_date': datetime.strptime(child_birth_date, '%m/%d/%Y'),
                }
                childinformation = Child(**chil)
                childinformation.save()
                objc = Child.objects.filter(user=request.user)
                return render(request, './accounts/child-information.html', context={'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'childinformations': objc, 'child_categ': get_categ_and_subcateg()})
        else:
            chill = get_object_or_404(Child, id=id)
            chill.child_name = child_name
            # Piyush: changed datetime.datetime to datetime on 12-09-2020
            chill.child_birth_date = datetime.strptime(child_birth_date, '%m/%d/%Y')
            chill.save()
            objc = Child.objects.filter(user=request.user)
            return render(request, './accounts/child-information.html', context={'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'childinformations': objc, 'child_categ': get_categ_and_subcateg()})
    objc = Child.objects.filter(user=request.user)
    return render(request, './accounts/child-information.html', context={'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'childinformations': objc, 'child_categ': get_categ_and_subcateg()})


@login_required
def address_delete(request, id):
    obj = get_object_or_404(Address, id=id)
    # obj.delete()
    # return redirect('manageaddress')
    try:
        obj.delete()
        return redirect('manageaddress')
    except models.ProtectedError:
        messages.error(request, 'You can`t delete this address. because you already used this address in case of orders.')
        return redirect('manageaddress')


@login_required
def childs_delete(request, id):
    obj = get_object_or_404(Child, id=id)
    obj.delete()
    return redirect('childinformation')


# @login_required
# def usercustomsizes(request):
#     if request.method == 'POST':
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

#         if not id:
#             if user_custom_size_name and shoulder_to_apex:
#                 ucs = {
#                     'user':request.user,
#                     'user_custom_size_name':user_custom_size_name,
#                     'shoulder_to_apex': shoulder_to_apex,
#                     'cap_sleeve_length':cap_sleeve_length,
#                     'short_sleeve_length':short_sleeve_length,
#                     'three_fourth_to_apex':three_fourth_to_apex,
#                     'full_sleeve_length':full_sleeve_length,
#                     'knee_round':knee_round,
#                     'calf':calf,
#                     'ankle_round':ankle_round,
#                     'waist_length':waist_length,
#                     'neck_round':neck_round,
#                     'front_neck_depth':front_neck_depth,
#                     'cross_front':cross_front,
#                     'bust':bust,
#                     'under_bust':under_bust,
#                     'waist':waist,
#                     'lower_waist':lower_waist,
#                     'wrist':wrist,
#                     'thigh_round':thigh_round,
#                     'lower_thigh':lower_thigh,
#                     'arm_hole':arm_hole,
#                     'knee_length':knee_length,
#                     'full_length':full_length,
#                     'shoulder':shoulder,
#                     'back_neck_depth':back_neck_depth,
#                     'biceps':biceps,
#                     'elbow_round':elbow_round,
#                     'hips':hips,
#                     'bottom_length':bottom_length,
#                 }
#                 ucsize = UserCustomSize(**ucs)
#                 ucsize.save()
#                 objs = UserCustomSize.objects.filter(user=request.user)
#                 return render(request, './accounts/user-custom-sizes.html', context={'pusercustomsizes':objs, 'child_categ': get_categ_and_subcateg()})
#         else:
#             ucsaddr = get_object_or_404(UserCustomSize, id=id)
#             ucsaddr.user_custom_size_name = user_custom_size_name
#             ucsaddr.shoulder_to_apex = shoulder_to_apex
#             ucsaddr.cap_sleeve_length = cap_sleeve_length
#             ucsaddr.short_sleeve_length = short_sleeve_length
#             ucsaddr.three_fourth_to_apex = three_fourth_to_apex
#             ucsaddr.full_sleeve_length = full_sleeve_length
#             ucsaddr.knee_round = knee_round
#             ucsaddr.calf = calf
#             ucsaddr.ankle_round = ankle_round
#             ucsaddr.waist_length = waist_length
#             ucsaddr.neck_round = neck_round
#             ucsaddr.front_neck_depth = front_neck_depth
#             ucsaddr.cross_front = cross_front
#             ucsaddr.bust = bust
#             ucsaddr.under_bust = under_bust
#             ucsaddr.waist = waist
#             ucsaddr.lower_waist = lower_waist
#             ucsaddr.wrist = wrist
#             ucsaddr.thigh_round = thigh_round
#             ucsaddr.lower_thigh = lower_thigh
#             ucsaddr.arm_hole = arm_hole
#             ucsaddr.knee_length = knee_length
#             ucsaddr.full_length = full_length
#             ucsaddr.shoulder = shoulder
#             ucsaddr.back_neck_depth = back_neck_depth
#             ucsaddr.biceps = biceps
#             ucsaddr.elbow_round = elbow_round
#             ucsaddr.hips = hips
#             ucsaddr.bottom_length = bottom_length
#             ucsaddr.save()
#             objs = UserCustomSize.objects.filter(user=request.user)
#             return render(request, './accounts/user-custom-sizes.html', context={'pusercustomsizes': objs, 'child_categ': get_categ_and_subcateg()})
#     objs = UserCustomSize.objects.filter(user=request.user).order_by('-id')
#     return render(request, './accounts/user-custom-sizes.html', context={'pusercustomsizes': objs, 'child_categ': get_categ_and_subcateg()})



@login_required
def usercustomsizes(request):

    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.all()
    testimonials_items = Testimonials.objects.all()
    disclaimer_items = Disclaimer.objects.all()
    privacy_items = Privacypolicy.objects.all()
    terms_items = Terms.objects.all()
    
    # if request.method == 'POST':
    #     id = request.POST.get('id')
    #     user_custom_size_name = request.POST.get('user_custom_size_name')
    #     shoulder_to_apex = request.POST.get('shoulder_to_apex')

    #     if not id:
    #         if user_custom_size_name and shoulder_to_apex:
    #             ucs = {
    #                 'user':request.user,
    #                 'user_custom_size_name':user_custom_size_name,
    #                 'shoulder_to_apex': shoulder_to_apex,
    #             }
    #             ucsize = UserCustomSize(**ucs)
    #             ucsize.save()
    #             objs = UserCustomSize.objects.filter(user=request.user)
    #             return render(request, './accounts/user-custom-sizes.html', context={'pusercustomsizes':objs, 'child_categ': get_categ_and_subcateg()})
    #     else:
    #         ucsaddr = get_object_or_404(UserCustomSize, id=id)
    #         ucsaddr.user_custom_size_name = user_custom_size_name
    #         ucsaddr.shoulder_to_apex = shoulder_to_apex

    #         ucsaddr.save()
    #         objs = UserCustomSize.objects.filter(user=request.user)
    #         return render(request, './accounts/user-custom-sizes.html', context={'pusercustomsizes': objs, 'child_categ': get_categ_and_subcateg()})
    

    objs = UserCustomMeasures.objects.filter(user=request.user).order_by('-id')
    pusercustomsizes = {}
    if objs:
        for size in objs:
            if size.user_custom_size_name not in pusercustomsizes:
                pusercustomsizes[size.user_custom_size_name] = [{'id':size.id, 'age':size.age,'measures':size.measures, 'standard_value':size.standard_value, 'custom_value':size.custom_value}]
                # pusercustomsizes['age'] = size.age
            elif size.user_custom_size_name in pusercustomsizes:
                pusercustomsizes[size.user_custom_size_name].append({'id':size.id, 'age':size.age,'measures':size.measures, 'standard_value':size.standard_value, 'custom_value':size.custom_value})
    return render(request, './accounts/user-custom-sizes.html', context={'pusercustomsizes': pusercustomsizes, 'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()})


@login_required
def editsize(request, id):
    try:
        size = get_object_or_404(id=id)
        if request.method == 'POST':
            custom = request.POST.get('custom_value')
            size.custom_value = custom
            size.save()
            return render
    except:
        pass


@login_required
def usercustomsizes_delete(request, id):
    obj = get_object_or_404(UserCustomSize, id=id)
    obj.delete()
    return redirect('usercustomsizes')


@login_required
def pancardinformation(request):
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.all()
    testimonials_items = Testimonials.objects.all()
    disclaimer_items = Disclaimer.objects.all()
    privacy_items = Privacypolicy.objects.all()
    terms_items = Terms.objects.all()

    if request.method == 'POST':
        pancard_name = request.POST.get('pancard_name')
        pancard_number = request.POST.get('pancard_number')
        current_user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=current_user)
        profile.pancard_name = pancard_name
        profile.pancard_number = pancard_number
        profile.save()
        return render(request, './accounts/pan-card-information.html', {'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()})
    return render(request, './accounts/pan-card-information.html', {'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()})


@login_required
def aadharcardinformation(request):
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.all()
    testimonials_items = Testimonials.objects.all()
    disclaimer_items = Disclaimer.objects.all()
    privacy_items = Privacypolicy.objects.all()
    terms_items = Terms.objects.all()

    if request.method == 'POST':
        aadharcard_name = request.POST.get('aadharcard_name')
        aadharcard_number = request.POST.get('aadharcard_number')
        current_user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=current_user)
        profile.aadharcard_name = aadharcard_name
        profile.aadharcard_number = aadharcard_number
        profile.save()
        return render(request, './accounts/aadhar-card-information.html', {'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()})
    return render(request, './accounts/aadhar-card-information.html', {'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'child_categ': get_categ_and_subcateg()})


@login_required
def customersupport(request):
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.all()
    testimonials_items = Testimonials.objects.all()
    disclaimer_items = Disclaimer.objects.all()
    privacy_items = Privacypolicy.objects.all()
    terms_items = Terms.objects.all()

    return render(request, './accounts/customersupport.html', {'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items,'child_categ': get_categ_and_subcateg()})


@login_required
def myuserqueries(request):
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    faq_items = Faq.objects.all()
    testimonials_items = Testimonials.objects.all()
    disclaimer_items = Disclaimer.objects.all()
    privacy_items = Privacypolicy.objects.all()
    terms_items = Terms.objects.all()

    if request.method == 'POST':
        id = request.POST.get('id')
        order_id = request.POST.get('order_id')
        query_summary = request.POST.get('query_summary')
        query_details = request.POST.get('query_details')
        if not id:
            if order_id and query_summary:
                uqs = {
                    'user': request.user,
                    'order_id': order_id,
                    'query_summary': query_summary,
                    'query_details': query_details,
                }
                muquery = UserQueries(**uqs)
                muquery.save()

                # Email send when user send query | 19 Nov 2020
                subject = query_summary
                current_site = get_current_site(request)

                req_username = request.user.email.split("@")[0]
                name = ''
                if request.user.first_name and request.user.last_name:
                    name = request.user.first_name + " " + request.user.last_name
                elif request.user.first_name:
                    name = request.user.first_name
                else:
                    name = req_username

                user_email = request.user.email
                if request.user and request.user.email:
                    user_email = request.user.email
                current_company = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
                to_email = 'hello@hoitymoppet.com'
                if current_company and current_company[0].email:
                    to_email = current_company[0].email

                message = {
                    'user': request.user,
                    'user_email': request.user.email,
                    'order_id': order_id,
                    'query_summary': query_summary,
                    'query_details': query_details,
                    'subject': subject,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
                    'BASE_URL': settings.BASE_URL,
                }
                config = DynamicEmailConfiguration.get_solo()
                email = EmailMessage('etemplate/user_query_email.tpl', message, "Do not reply <{}>".format(config.from_email), to=[to_email])
                email.send()
                objc = UserQueries.objects.filter(user=request.user)
                return render(request, './accounts/userqueries.html', context={'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'alluserqueries': objc, 'child_categ': get_categ_and_subcateg()})
        else:
            uqss = get_object_or_404(UserQueries, id=id)
            uqss.order_id = order_id
            uqss.query_summary = query_summary
            uqss.query_details = query_details
            uqss.save()
            objc = UserQueries.objects.filter(user=request.user)
            return render(request, './accounts/userqueries.html', context={'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'alluserqueries': objc, 'child_categ': get_categ_and_subcateg()})
    objc = UserQueries.objects.filter(user=request.user).order_by('-id')
    return render(request, './accounts/userqueries.html', context={'company_info':company_info, 'faq_items':faq_items, 'testimonials_items':testimonials_items, 'disclaimer_items':disclaimer_items, 'privacy_items':privacy_items, 'terms_items':terms_items, 'alluserqueries': objc, 'child_categ': get_categ_and_subcateg()})


# we have override get_context_data funtion of MyLoginView for dynamic background image/we have changed url also.   
class MyLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image = BackgroundImage.objects.filter(item='loginimage', status='active')
        context['image'] = image
        return context