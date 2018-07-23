from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

from carton.cart import Cart
from products.models import Item


class AddToCartView(generic.View):
    """View for adding Item to Cart"""

    def get(self, request, pk):
        cart = Cart(request.session)
        product = Item.objects.get(id=pk)
        cart.add(product, price=product.price)
        return redirect('show')


class ShowCartView(generic.View):
    """View for showing Items in Cart"""

    def get(self, request):
        return render(request, 'shopping/cart.html')


class RemoveSingleItemView(generic.View):
    """View for remove single item in Cart"""

    def get (self, request, pk):
        cart = Cart(request.session)
        product = Item.objects.get(id=pk)
        cart.remove_single(product)
        return redirect('show')
