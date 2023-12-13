from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .cart import Cart
from product.models import Product


def add_to_cart(request, id):
    cart = Cart(request)
    cart.add(id)

    return render(request, 'cart/partials/menu_cart.html')


def cart(request):
    context = {}
    return render(request, 'cart/cart.html', context)


def update_cart(request, product_id, action):
    cart = Cart(request)

    if action == 'increment':
        cart.add(product_id, 1, True)
    else:
        cart.add(product_id, -1, True)

    product = Product.objects.get(pk=product_id)
    quantity = cart.get_item(product_id)
    

    if quantity:
        quantity = quantity['quantity']

        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'image': product.image,
                'get_thumbnail': product.get_thumbnail(),
                'price': product.get_display_price(),
            },
            'total_price': (quantity * product.get_display_price()) ,
            'quantity': quantity,
        }
    else:
        item = None


    context = {
        'item': item,
    }

    response = render(request, 'cart/partials/cart_item.html', context)
    response['HX-Trigger'] = 'update-menu-cart'

    return response


@login_required
def checkout(request):
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE

    context = {'pub_key': pub_key}
    return render(request, 'cart/checkout.html', context)


def success(request):
    return render(request, 'cart/success.html', {})


def hx_menu_cart(request):
    return render(request, 'cart/partials/menu_cart.html')

def hx_cart_total(request):
    return render(request, 'cart/partials/cart_total.html')