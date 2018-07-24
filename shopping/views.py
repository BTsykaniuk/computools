from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic

from carton.cart import Cart
from products.models import Item


class AddCartItemView(generic.View):

    def get(self, request, pk):
        cart = Cart(session=request.session, session_key='CART')
        product = Item.objects.get(id=pk)
        cart.add(product, price=product.price)
        request.session['cart_count'] = cart.count
        return redirect('show')


class ShowCartView(generic.View):

    def get(self, request):
        cart = Cart(session=request.session, session_key='CART')
        return render(request, 'shopping/cart.html', {'cart': cart})


class RemoveCartItemView(generic.View):

    def get(self, request, pk):
        cart = Cart(session=request.session, session_key='CART')
        product = Item.objects.get(id=pk)
        cart.remove_single(product)
        request.session['cart_count'] = cart.count
        return redirect('show')


class AddWishItemView(generic.View):

    def get(self, request, pk):
        wishlist = Cart(session=request.session, session_key='WISH')
        product = Item.objects.get(id=pk)
        wishlist.add(product, price=product.price)
        request.session['wish_count'] = wishlist.count
        return redirect('show_wish')


class ShowWishlistView(generic.View):

    def get(self, request):
        wishlist = Cart(session=request.session, session_key='WISH')
        return render(request, 'shopping/wishlist.html', {'wishlist': wishlist})


class RemoveWishItemView(generic.View):

    def get(self, request, pk):
        wishlist = Cart(session=request.session, session_key='WISH')
        product = Item.objects.get(id=pk)
        wishlist.remove_single(product)
        request.session['wish_count'] = wishlist.count
        return redirect('show_wish')
