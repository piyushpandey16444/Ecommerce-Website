from django.contrib.auth.models import User, Group, Associated_Company

from hoitymoppet.models import (Color, Fabric, Styles, Categories, Stockdetails, Product, Age, 
Lookbookcategories, Lookbook, Slider, Photo, Companyphoto, Company, Careinstructions, Privacypolicy, 
Disclaimer, Terms, UserCart, UserCustomSize, Coupon, Order, OrderDetail, Country, OrderUpdate, DeliveryPlaces, 
Advertise, UserWishList, Faq, Testimonials, Statusoption, UserQueries)


def count_users():
    return User.objects.count()

def count_groups():
    return Group.objects.count()

def count_products():

    # ddc = self.request.user.default_company
    # print("ddcccccccccccccccccccccccccccccccccccccccccccccccccc", self.request.user.default_company)

    # context = super().get_context_data(**kwargs)
    # if 'company' not in self.request.session:
    #     print("list_viewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
    #     self.request.session['company'] = self.request.user.default_company.associated_company_name
    # return context

    # if 'company' in request.session:
    #     print("The value of the company isssssssssssssssssszzzzzzzzzzzzzz", request.session['company'])
    #     company_id = Associated_Company.objects.filter(associated_company_name = request.session['company'])
    #     list_view = Product.objects.filter(associated_company_id=company_id[0].id)
    #     print("list_viewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww", list_view)
    # return list_view
    # return Product.objects.filter(associated_company_id=company_id[0].id).count()

    # return Product.objects.filter(associated_company_id=1).count()
    return Product.objects.filter(status="active").count()


def count_orders():
    return Order.objects.count()

def count_orders_confirm():
    return Order.objects.filter(status_name="ordered").count()

def count_orders_dispatch():
    return Order.objects.filter(status_name="confirmed").count()

def count_orders_shiped():
    return Order.objects.filter(status_name="dispatched").count()

def count_orders_delivered():
    return Order.objects.filter(status_name="delivered").count()

def count_categories():
    return Categories.objects.count()

def count_enquiries():
    return UserQueries.objects.count()