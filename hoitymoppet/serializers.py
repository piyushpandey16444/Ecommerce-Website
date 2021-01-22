from rest_framework import serializers
# from hoitymoppet.models import Categories, Product, Careinstructions, Fabric, Age, Color, Photo, Order
from hoitymoppet.models import *
from django.contrib.auth.models import Associated_Company, User
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth.hashers import make_password


# Piyush: code for category serializer
class CategoriesSerializer(serializers.ModelSerializer):
    category_image = Base64ImageField(use_url=True, required=False)  # for encoding image in django

    class Meta:
        model = Categories
        fields = '__all__'


# Piyush: code for company serializer
class CompanySerializer(serializers.ModelSerializer):
    company_logo = Base64ImageField(use_url=True)  # for encoding image in django

    class Meta:
        model = Associated_Company
        fields = '__all__'


# Piyush: code for user serializer on 22-08-2020
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = make_password(validated_data['password'])
        associated_company = validated_data.pop('associated_company')
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        default_company = validated_data.pop('default_company')
        first_name = validated_data.pop('first_name')
        is_active = validated_data.pop('is_active')
        is_superuser = validated_data.pop('is_superuser')
        is_staff = validated_data.pop('is_staff')
        last_name = validated_data.pop('last_name')

        user_obj = User.objects.create(username=username, default_company=default_company,
                                       is_active=is_active, first_name=first_name, last_name=last_name, email=email,
                                       is_superuser=is_superuser, is_staff=is_staff)

        user_obj.set_password(password)
        user_obj.save()

        # adding many2many fields i.e companies to the above created user object
        if associated_company:
            for company in associated_company:
                user_obj.associated_company.add(company)
                user_obj.save()
            return user_obj

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        user = super(UserSerializer, self).update(instance, validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
# Piyush: code for user serializer on 22-08-2020 ends here


# Piyush: code for product serializer on 22-08-2020
class ProductSerializer(serializers.ModelSerializer):
    productimage = Base64ImageField(use_url=True)  # for encoding image in django
    # photos =

    class Meta:
        model = Product
        fields = '__all__'

    # overriding create function for fetching data from the sent dictionary
    def create(self, validated_data):
        product_name = validated_data.pop('product_name')
        slug = validated_data.pop('slug')
        associated_company = validated_data.pop('associated_company')
        price = validated_data.pop('price')
        discount_price = validated_data.pop('discount_price')
        age = validated_data.pop('age')
        # country = validated_data.pop('country')
        color = validated_data.pop('color')
        categories = validated_data.pop('categories')
        categories_erp = validated_data.pop('categories_erp')
        reference_id = validated_data.pop('reference_id')
        item_detail = validated_data.pop('item_detail')
        productimage = validated_data.pop('productimage')
        migrate_data = validated_data.pop('migrate_data')
        status = validated_data.pop('status')
        relative_product = validated_data.pop('relative_product')
        expected_delivery_date = validated_data.pop('expected_delivery_date')
        product_uom = validated_data.pop('product_uom')

        # creating product instance
        product_obj = Product.objects.create(product_name=product_name, reference_id=reference_id, price=price,
                                             associated_company=associated_company, item_detail=item_detail,
                                             status=status, productimage=productimage, product_uom=product_uom,
                                             migrate_data=migrate_data, expected_delivery_date=expected_delivery_date,
                                             discount_price=discount_price, categories_erp=categories_erp)

        # adding many2many fields to the above created product object
        if categories:
            for category in categories:
                product_obj.categories.add(category)
                product_obj.save()

        if color:
            for clr in color:
                product_obj.color.add(clr)
                product_obj.save()

        if age:
            for ag in age:
                product_obj.age.add(ag)
                product_obj.save()

        if relative_product:
            for pro in relative_product:
                product_obj.relative_product.add(pro)
                product_obj.save()
        return product_obj

    def update(self, instance, validated_data):
        relative_product = validated_data.pop('relative_product')
        product_instance = super(ProductSerializer, self).update(instance, validated_data)
        if relative_product:
            for pro in relative_product:
                product_instance.relative_product.add(pro)
                product_instance.save()
        return product_instance
# P: code for product ends here


# Piyush: code for Care serializer on 22-08-2020
class CareinstructionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Careinstructions
        fields = "__all__"


# Piyush: code for Fabric serializer on 22-08-2020
class FabricSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fabric
        fields = "__all__"


# Piyush: code for Age serializer on 22-08-2020
class AgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Age
        fields = "__all__"


# Piyush: code for Color serializer on 22-08-2020
class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = "__all__"


# Piyush: code for company serializer
class PhotoSerializer(serializers.ModelSerializer):
    image = Base64ImageField(use_url=True)  # for encoding image in django

    class Meta:
        model = Photo
        fields = '__all__'

        def create(self, validated_data):
            product = validated_data.pop('product')
            image = validated_data.pop('image')
            return Photo.objects.create(product=product, image=image)

        def update(self, instance, validated_data):
            product = validated_data.pop('product')
            image_instance = super(PhotoSerializer, self).update(instance, validated_data)
            if product:
                image_instance.save()
            return image_instance
# code ends here for PhotoSerializer


# Piyush: code for Measurement master serializer on 19-09-2020
class MeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measurement_Master
        fields = "__all__"
# Piyush: code for Measurement master serializer on 19-09-2020 ends here


# Piyush: code for Measures serializer on 19-09-2020
class MeasuresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measures
        fields = "__all__"
# Piyush: code for Measures serializer on 19-09-2020 ends here


# Piyush: code for AvailableCoupons serializer on 01-10-2020
class AvailableCouponsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = "__all__"

    # overriding create function for fetching data from the sent dictionary
    def create(self, validated_data):
        code = validated_data.pop('code')
        company_id = validated_data.pop('company_id')
        valid_from = validated_data.pop('valid_from')
        valid_to = validated_data.pop('valid_to')
        minimum_amount = validated_data.pop('minimum_amount')
        limit_number = validated_data.pop('limit_number')
        discount_type = validated_data.pop('discount_type')
        discount = validated_data.pop('discount')
        reference_id = validated_data.pop('reference_id')
        migrate_data = validated_data.pop('migrate_data')
        active = validated_data.pop('active')
        customer = validated_data.pop('customer')
        all_customer = validated_data.pop('all_customer')
        coupon_description = validated_data.pop('coupon_description')


        # creating coupon instance
        coupon_obj = Coupon.objects.create(code=code, reference_id=reference_id, company_id=company_id,
                                             valid_from=valid_from, valid_to=valid_to, all_customer=all_customer,
                                             active=active, minimum_amount=minimum_amount, coupon_description=coupon_description, 
                                             migrate_data=migrate_data, discount=discount,
                                             limit_number=limit_number, discount_type=discount_type)

        # adding many2many fields to the above created coupon object
        if customer:
            for user in customer:
                coupon_obj.customer.add(user)
                coupon_obj.save()

        return coupon_obj
# Piyush: code for AvailableCoupons serializer on 01-10-2020 ends here


# Piyush: code for ResCurrency serializer
class ResCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = HoityCurrency
        fields = '__all__'
# code ends here


# Piyush: code for ResCurrencyRate serializer
class ResCurrencyRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = HoityCurrencyRate
        fields = '__all__'
# code ends here


# Piyush: code for ResCountry serializer
class ResCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = HoityCountry
        fields = '__all__'
# code ends here


# Piyush: code for ResState serializer
class ResStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = HoityState
        fields = '__all__'
# code ends here


# Piyush: code for Color serializer on 22-08-2020
class ProductUomSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductUom
        fields = "__all__"


# Piyush: code for Shipping Charges serializer on 15-12-2020
class ShippingChargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCharges
        fields = "__all__"
# Piyush: code for Shipping Charges serializer on 15-12-2020 ends here


# Piyush: code for Shipping Charges serializer on 16dec
class ShippingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingProduct
        fields = "__all__"
# Piyush: code for Shipping Charges serializer on 16dec ends here
