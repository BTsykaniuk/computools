from django.shortcuts import render
from django.shortcuts import redirect

from carton.cart import Cart
from products.models import Item


def add_item(request, pk):
    cart = Cart(session=request.session, session_key='CART')
    product = Item.objects.get(id=pk)
    cart.add(product, price=product.price)
    request.session['cart_count'] = cart.count
    return redirect('show')


def show_cart(request):
    cart = Cart(session=request.session, session_key='CART')
    return render(request, 'shopping/cart.html', {'cart': cart})


def remove_single_item(request, pk):
    cart = Cart(session=request.session, session_key='CART')
    product = Item.objects.get(id=pk)
    cart.remove_single(product)
    request.session['cart_count'] = cart.count
    return redirect('show')


def add_to_wish(request, pk):
    wishlist = Cart(session=request.session, session_key='WISH')
    product = Item.objects.get(id=pk)
    wishlist.add(product, price=product.price)
    request.session['wish_count'] = wishlist.count
    return redirect('show_wish')


def show_wishlist(request):
    wishlist = Cart(session=request.session, session_key='WISH')
    return render(request, 'shopping/wishlist.html', {'wishlist': wishlist})


def remove_single_wish(request, pk):
    wishlist = Cart(session=request.session, session_key='WISH')
    product = Item.objects.get(id=pk)
    wishlist.remove_single(product)
    request.session['wish_count'] = wishlist.count
    return redirect('show_wish')
