from django import template
from IFish.models import Category, CartItem, Cart

register = template.Library()


@register.simple_tag
def get_objects():
    return Category.objects.all()


@register.simple_tag
def get_cart(request):
    return Cart.objects.get(user=request.user)

@register.simple_tag
def get_cartItems(request):
    carts = Cart.objects.filter(user=request.user).order_by('createdAt').reverse()[:1]
    cart = carts[0]
    cartItems = CartItem.objects.filter(cart=cart)
    return len(cartItems)
