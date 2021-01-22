from django import template
from hoitymoppet.models import UserCart, UserWishList

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = UserCart.objects.filter(user=user, ordered=False).count()
        if qs:
            return qs
    return 0


@register.filter
def wishlist_item_count(user):
    if user.is_authenticated:
        qs = UserWishList.objects.filter(user=user).count()
        if qs:
            return qs
    return 0