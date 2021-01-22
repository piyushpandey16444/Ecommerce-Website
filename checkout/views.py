from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from paywix.payu import Payu
from des.models import DynamicEmailConfiguration

payu_config = settings.PAYU_CONFIG
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')

payu = Payu(merchant_key, merchant_salt, surl, furl, mode)

from mail_templated import EmailMessage
from django.contrib.auth.models import User
from accounts.models import *
from generic_links.models import *
from hoitymoppet.models import *
from hoitymoppet.views import *
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
import secrets
# Create your views here.

def get_categ_and_subcateg():
    categories = Categories.objects.filter(parent_category=None, status='active', invisible=False)
    categ_dict = {}
    for categ in categories:
        c_list = Categories.objects.filter(parent_category=categ, status='active').values()
        categ_dict[categ] = c_list
    return categ_dict


def category_wise_products(request, id):
    product_cat = get_object_or_404(Categories, id=id)
    print("product_cat ................", product_cat)

    # allprods = Product.objects.all()
    # allprods = get_object_or_404(Product, id=id)
    # print("allprodssssssssssssssssssssssssssssssss", allprods)

    products = Product.objects.filter(categories=id, status=1).order_by('-id')

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
        #####abhishek start 7-5-2020
        if request.user.id:
            wishlist_product_user_wise = UserWishList.objects.filter(product_id=product.id, user=request.user)
            if wishlist_product_user_wise:
                wishlist_product_user_wise_list.append(product.id)
        #####abhishek end7-5-2020
    categories = Categories.objects.filter(parent_category=None)
    categ_dict = {}
    for categ in categories:
        c_list = Categories.objects.filter(parent_category=categ, status='active')
        categ_dict[categ]= c_list
    context = {'product_cat': product_cat, 'products': products, 'categories':categories, 'photos': photos, 'prod_photos_all':prod_photos_all, 'child_categ':categ_dict, 'disable_attr': wishlist_product_user_wise_list}
    return render(request, "hoitymoppet/category-wise-products.html", context)


def home(request):
    return render(request, 'checkout/home.html')


@csrf_exempt
@login_required
def payu_demo(request):
    coupon = ''
    coupon_code = ''
    coupon_dicount_amt = 0.0
    user = str(request.user.id)
    # data.update({"udf3": user})
    address_id = []
    if request.GET and request.GET.get('addr'):
        address_id = request.GET.get('addr')
    # data.update({"udf4": address_id})

    total_discount_price = 0.0
    card_records = UserCart.objects.filter(user=request.user)
    if card_records:
        total_discount_price = cart_items_discount_price_total(card_records)
        subtotal = cart_items_discount_price_total(card_records) or 0.0
        
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
            # data.update({"udf5": coupon})
    shipping_charges = cart_items_shipping_charges(request, card_records, subtotal, request.GET.get('addr')) or 0.0
    #print('shipping_charges', shipping_charges)
    ship_charges = shipping_charges['shipping']
    total_amount =  subtotal + ship_charges
    #Jatin end: code for shipping charges
    
    user_fname = request.user.first_name
    user_lname = request.user.last_name
    user_email = request.user.email
    user_phone = request.user.phone

    if address_id:
        delivery_address = Address.objects.filter(user=user, id=address_id)
        if delivery_address:
            address = delivery_address[0]
    if not user_fname:
        user_fname=address.name
    if not user_phone:
        user_phone=address.mobile_no

    req_date = datetime.strftime(date.today(), '%d-%m-%Y')
    second_tax_id = str(user_email + '-' + req_date)
    tax_id = secrets.token_hex(16)
    
    data = { 'amount': total_amount,
        'firstname': user_fname, 
        'email': user_email,
        'phone': user_phone, 'productinfo': 'Dress',
        'lastname': user_lname, 'address1': address.address,
        'address2': 'test', 'city': address.city,
        'state': address.user_state, 'country': address.user_country,
        'zipcode': address.pincode, 'udf1': '',
        'udf2': second_tax_id, 'udf3': user, 'udf4': address_id, 'udf5': coupon
    }

    
    # No Transactio ID's, Create new with paywix, it's not mandatory
    # Create your own transaction Id with payu and verify with table it's not existed
    # txnid = "Create your transaction id"
    data.update({"txnid": tax_id})
    
    payu_data = payu.transaction(**data)
    return render(request, 'checkout/payu_checkout.html', {"posted": payu_data})


# Jatin Added this function for calculating shipping charges
def cart_items_shipping_charges(request, items, subtotal, addr=None):
    shipping_charges = list(
        ShippingCharges.objects.filter(associated_company=request.user.default_company).values('free_order_value',
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



# Payu success return page
@csrf_exempt
def payu_success(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    amount = data.get('amount', 0.0)
    get_user_id = data.get('udf3')
    if get_user_id:
        get_user_id = int(get_user_id)
    address_id = data.get('udf4')
    response = payu.verify_transaction(data)
    # #print ("RRRRRRRRRRRResponse",response)
    # return JsonResponse(response)

    # user = request.user
    user = User.objects.get(id=get_user_id)

    #####abhishek 21-5-2020 Work on 'Place Your Order' button functionality
    # Get Address
    address = []
    # address = Address.objects.filter(user=user, id=1)
    # address = address[0]
    generated_order_detail_list = []
    generated_order = ''
    # if request.GET and request.GET.get('addr'):
    #     # delivery_address = Address.objects.filter(user=request.user, id=request.GET.get('addr'))
    #     # delivery_address = Address.objects.filter(user=user, id=request.GET.get('addr'))
    #     delivery_address = Address.objects.filter(user=user, id=request.GET.get('addr'))
    #     if delivery_address:
    #         address = delivery_address[0]
    if address_id:
        delivery_address = Address.objects.filter(user=user, id=address_id)
        if delivery_address:
            address = delivery_address[0]
        
    ####### SUB TOTAL #########

    order_id = []
    order_detail_list = []
    total_price = 0.0
    product_price = 0.0
    coupon_dicount_amt = 0.0
    coupon_discount_amt = 0.0
    subtotal = 0.0
    order = Order.objects.filter(user=user, id=request.GET.get('on'))
    if order:
        order_id = order[0]
        order_detail_list = OrderDetail.objects.filter(user=user, order_id=order_id)
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
                        coupon_dicount_amt = round(coupon_id.discount)
                    elif coupon_id.discount_type == 'Percentage':
                        coupon_dicount_amt = round((total_discount_price * coupon_id.discount) / 100)
                    subtotal = total_price - coupon_dicount_amt
    ####### SUB TOTAL #########
    if request.method == 'POST':
        cart_items = UserCart.objects.filter(user=user)
        if cart_items:
        
            # Create Order start
            ####abhishek start 28-10-2020 count expected delivery days from cart items
            expected_delivery_days = cart_items_expected_delivery_days(cart_items) or 0
            ####abhishek end 28-10-2020 count expected delivery days from cart items
            
            # prev_created_orders = Order.objects.filter()
            # order_no = 1
            # if prev_created_orders:
            #     order_no = len(prev_created_orders) + 10
            # ref_code = 'ArkeOrderNo' + str(order_no)

            ship_charges=0.0
            # shipping_charges = cart_items_shipping_charges(request, cart_items, subtotal1, request.GET.get('addr')) or 0.0
            # print('shipping_charges', shipping_charges)
            # if shipping_charges:
            #     ship_charges = shipping_charges['shipping']
            #Jatin end: code for shipping charges

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
                #####abhishek start 29-5-2020
                status_name='Confirm',
                #####abhishek end 29-5-2020
                expected_delivery_days=expected_delivery_days,
            )
            # Create Order end

            # if generated_order and address:
            #     address.editable = "false"
            #     address.save()

            if generated_order:
                # Create Order Detail and Delete Cart Item one by one after order placed - start
                for cart in cart_items:

                    # check for coupon applicable or not
                    # if request.GET and request.GET.get('cpn'):
                    if data and data.get('udf5'):
                        coupon_code_rec = Coupon.objects.filter(id=int(data.get('udf5')))
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
                        total_price=round(cart.quantity * product_price),
                        product_age=cart.product_age,
                        user_custom_size_master=cart.user_custom_size_master,
                        prod_color=cart.prod_color,
                    )
                    generated_order_detail_list.append(create_order_detail)
                    cart.delete()

                    # create_order_detail = OrderDetail.objects.create(
                    #     user=user,
                    #     order_id=generated_order,
                    #     product_id=cart.product_id,
                    #     quantity=cart.quantity,
                    #     price=(cart.product_id.discount_price or cart.product_id.price),
                    #     total_price=cart.quantity * (cart.product_id.discount_price or cart.product_id.price),
                    #     product_age=cart.product_age,
                    #     user_custom_size_master=cart.user_custom_size_master,
                    #     prod_color=cart.prod_color,
                    # )
                    # generated_order_detail_list.append(create_order_detail)
                    # cart.delete()
                # Create Order Detail and Delete Cart Item one by one after order placed - end
            
                # Create Tracking Status as Confirm - start
                tracking_status = TrackingStatus.objects.create(
                    user=user,
                    order_id=generated_order,
                    status_name='Confirm',
                    description='Order Confirm'
                )

                # Piyush: code for making description dynamic on 28-10-2020
                description = EmailDescription.objects.filter(subject='order_received').first()
                subject = "Your order has been Received. " + generated_order.ref_code
                # Piyush: code for making description dynamic on 28-10-2020 ends here passed in message
                # Create Tracking Status as Ordered - end
                current_site = get_current_site(request)

                # get default name and number 28-10-2020
                req_username = user.email.split("@")[0]
                name = ''
                if user.first_name and user.last_name:
                    name = user.first_name + " " + user.last_name
                elif user.first_name:
                    name = user.first_name
                else:
                    name = req_username
                placed_on = generated_order.ordered_date.date()

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
                    # 'token': account_activation_token.make_token(user),
                }
                config = DynamicEmailConfiguration.get_solo()
                # current_user = User.objects.get(id=request.user.id)
                # email from company 17-11-2020
                current_company = Associated_Company.objects.filter(
                    associated_company_url__contains='www.hoitymoppet.com')
                company_email = config.from_email
                if current_company and current_company[0].email:
                    company_email = current_company[0].email
                to_email = user.email
                email = EmailMessage('etemplate/acc_activate_email.tpl', message,
                                     "Do not reply <{}>".format(config.from_email), bcc=[company_email],
                                     to=[to_email])
                email.send()
                #####abhishek start 13-6-2020 get coupon code from url sent from addtocart page Apply Button
                coupon = data.get('udf5')
                # if request.GET:
                #     if request.GET.get('cpn'):
                if coupon:
                    coupon_id = int(coupon)
                    coupon_code_rec = Coupon.objects.filter(id=coupon_id)
                    if coupon_code_rec:
                        coupon_history = CouponHistory.objects.create(
                            user=user,
                            order_id=generated_order,
                            coupon_id=coupon_code_rec[0],
                        )
                        coupon_code_rec[0].customer.remove(user)
                #####abhishek end 13-6-2020 get coupon code from url sent from addtocart page Apply Button

                response.update({"generated_order": generated_order})
                response.update({"address": address})
                response.update({"generated_order_detail_list": generated_order_detail_list})
                response.update({"child_categ": get_categ_and_subcateg()})
                response.update({'amount': amount})
                response['from_payu'] = 'from_payu'

                #####abhishek start 30-09-2020
                payment_date = datetime.now()
                payment_date = datetime.strftime(payment_date, '%d-%m-%Y')
                payment_reference = PaymentReference.objects.create(
                    username=user,
                    order_no=generated_order,
                    amount=str(amount),
                    address=address,
                    payment_date=payment_date,
                    payment_mode='payumoney',
                )
                #####abhishek end 30-09-2020
                
                return render(request, "hoitymoppet/order-completed.html",
                              context=response)
        else:
            return HttpResponse("No Item in your Cart !")



# Payu failure return page
@csrf_exempt
def payu_failure(request):
    company_info = Associated_Company.objects.filter(associated_company_url__contains='www.hoitymoppet.com')
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    context= {'company_info':company_info, 'child_categ': get_categ_and_subcateg()}
    return render(request, "hoitymoppet/order-failure.html", context)
    # return JsonResponse(response)