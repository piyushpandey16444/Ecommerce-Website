from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<int:id>", views.category_wise_products, name="category-wise-products"),

    path("subcategory/<int:id>", views.sub_category, name="subcategory"),

    path("category_low/<int:id>", views.price_wise_products_low, name="price-asc-rank"),
    path("category_high/<int:id>", views.price_wise_products_high, name="price-desc-rank"),
    path("category_item/<int:id>", views.price_wise_products_low_twofive, name="price-asc-rank"),
    path("category_item_new/<int:id>", views.price_wise_products_low_fivezero, name="price-asc-rank"),
    path("shop/", views.shop, name="shop"),
    path("quickview/<int:id>", views.quickview, name="quickview"),
    path("productdetails/<str:slug>", views.productdetails, name="productdetails"),
    path("productdetails/<int:cat>/<str:slug>", views.productdetails, name="productdetails"),

    path("productcompare/", views.productcompare, name="productcompare"),    
    path("checkout/", views.checkout, name="checkout"),
    path("deliverymethod/", views.deliverymethod, name="deliverymethod"),
    path("paymentmethod/", views.paymentmethod, name="paymentmethod"),
    path("tracker/<int:id>", views.tracker, name="tracker"),
    path("hoitymoppetlookbook/", views.hoitymoppetlookbook, name="hoitymoppetlookbook"),
    path("hoitymoppetlookbookdetails/<int:id>", views.hoitymoppetlookbookdetails, name="hoitymoppetlookbookdetails"),
    path("category/<int:id>", views.categorydetails, name="categorydetails"),
    path("hoitymoppetblog/", views.hoitymoppetblog, name="hoitymoppetblog"),
    path("hoitymoppetblogdetails/", views.hoitymoppetblogdetails, name="hoitymoppetblogdetails"),
    path("careinstructions/", views.careinstructions, name="careinstructions"),
    path("productsearch/", views.productsearch, name="productsearch"),
    path("addtocart/", views.add_to_cart, name="addtocart"),    
    path("addcart/<str:slug>", views.add_product_to_cart_wishlist, name="update-cart"),
    path("deletecartitem/<int:id>", views.delete_product_from_cart, name="delete-cart-item"),
    path("productwishlist/", views.productwishlist, name="productwishlist"),
    path("addwishlist/<str:slug>", views.addWishList, name="add-wishlist"),
    path("deletewishlist/<int:id>", views.deleteWishList, name="delete-wishlist"),
    path("productdetails", views.add_user_custom_size, name="customize-size"),
    path("add_single/<int:id>", views.add_single_item_from_cart, name="add-single-item-to-cart"),
    path("remove_single/<int:id>", views.remove_single_item_from_cart, name="remove-single-item-from-cart"),
    path("custom", views.custom, name="custom"),
    path("ordercompleted/", views.ordercompleted, name="ordercompleted"),
    path("addwishlist_new/<int:id>", views.add_to_wishlist, name="wishlist"),

    path("addwishlist_new_item/<int:id>", views.add_to_wishlist_item, name="wishlist-item"),

    path("hoitymoppetblogdetails/<int:id>", views.add_to_wishlist_by_lookbook, name="wishlist-lookbook"),

    path("singleorderconfirmation/", views.singleorderconfirmation, name="singleorderconfirmation"),
    path("multiorderconfirmation/", views.multiorderconfirmation, name="multiorderconfirmation"),
    path("userconfirmation/", views.userconfirmation, name="userconfirmation"),

    path("change_status/<int:id>", views.change_status, name="change_status"),
    path("change_status_done/<int:id>", views.change_status_done, name="change_status_done"),
    #####abhishek start 12-6-2020 adding url calling from Cart form Coupon Apply Button
    path("coupon_apply/>", views.coupon_apply, name="coupon_apply"),
    #####abhishek end 12-6-2020 adding url calling from Cart form Coupon Apply Button

    # Piyush: urls for sending mail on 06-08-2020
    path("send-mail/", views.cart_mail_view, name="send-mail"),

    path("custom-size/", views.getcustomsize, name="custom-size"),
    path("user-custom-size/", views.GetUserCustomSize, name="user-custom-size"),
    path("get-selected-customsize/", views.getselectedcustomsize, name="get-selected-customsize"),

    # Piyush: api's for create, update and delete
    path("create-user/", views.create_user, name="create-user"),
    path("update-user/<str:pk>/", views.update_user, name="update-user"),

    path("create-company/", views.create_company, name="create-company"),
    path("update-company/<str:pk>/", views.update_company, name="update-company"),
    path("company-list/", views.company_record, name="company-list"),

    path("create-category/", views.create_category, name="create-category"),
    path("update-category/<str:pk>/", views.update_category, name="update-category"),
    path("category-list/", views.category_record, name="category-list"),

    path("create-product/", views.create_product, name="create-product"),
    path("update-product/<str:pk>/", views.update_product, name="update-product"),

    path("create-care-instruction/", views.create_care_instruction, name="create-care-instruction"),
    path("update-care-instruction/<str:pk>/", views.update_care_instruction, name="update-care-instruction"),

    path("create-fabric/", views.create_fabric, name="create-fabric"),
    path("update-fabric/<str:pk>/", views.update_fabric, name="update-fabric"),

    path("create-color/", views.create_color, name="create-color"),
    path("update-color/<str:pk>/", views.update_color, name="update-color"),

    path("update-order/<str:pk>/", views.update_order, name="update-order"),

    path("create-images/", views.create_images, name="create-images"),

    path("create-age/", views.create_age, name="create-age"),
    path("update-age/<str:pk>/", views.update_age, name="update-age"),
    path("delete-age/<str:pk>/", views.delete_age, name="delete-age"),

    path("create-measurement-master/", views.create_measurement_master, name="create-measurement-master"),
    path("update-measurement-master/<str:pk>/", views.update_measurement_master, name="update-measurement-master"),

    path("create-measures/", views.create_measures, name="create-measures"),
    path("update-measures/<str:pk>/", views.update_measures, name="update-measures"),

    path("create-currency/", views.create_currency, name="create-currency"),
    path("create-currency-rate/", views.create_currency_rate, name="create-currency-rate"),
    path("create-country/", views.create_country, name="create-country"),
    path("create-state/", views.create_state, name="create-state"),

    path("create-coupon/", views.create_coupon, name="create-coupon"),
    path("update-coupon/<str:pk>/", views.update_coupon, name="update-coupon"),
    path("available-coupon/", views.available_coupons, name="available-coupon"),

    path("create-product-uom/", views.create_product_uom, name="create-product-uom"),
    path("update-product-uom/<str:pk>/", views.update_product_uom, name="update-product-uom"),

    path("delete-image/<str:pk>/", views.delete_images, name="delete-image"),

    path("custom-size-name/", views.unique_custom_name, name="custom-size-name"),

    # path("create-email-description/", views.create_email_description, name="create-email-description"),
    # path("update-email-description/<str:pk>/", views.update_email_description, name="update-email-description"),

    path("create-shipping-charge/", views.create_shipping_charge, name="create-shipping-charge"),
    path("update-shipping-charge/<str:pk>/", views.update_shipping_charge, name="update-shipping-charge"),

    path("create-shipping-product/", views.create_shipping_product, name="create-shipping-product"),
    path("update-shipping-product/<str:pk>/", views.update_shipping_product, name="update-shipping-product"),

]
