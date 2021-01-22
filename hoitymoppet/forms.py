from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *
from accounts.models import *
from hoitymoppet.models import *


class UserCustomSizeform(forms.ModelForm):
    class Meta:
        model = UserCustomSize
        fields = '__all__'


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


class UserQueriesform(forms.ModelForm):
    class Meta:
        model = UserQueries
        fields = '__all__'


# Coupon code
class CouponApplyForm(forms.Form):
	code = forms.CharField()


# user custom size new concept | 08 Sep 2020
# class UserCustomSizeform(forms.ModelForm):
#     class Meta:
#         model = Age
#         fields = '__all__