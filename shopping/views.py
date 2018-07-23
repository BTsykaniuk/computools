from django.shortcuts import render
from django.http import HttpResponse

from carton.cart import Cart
from products.models import Item


def add(request, pk):
    cart = Cart(request.session)
    print(request)
    product = Item.objects.get(id=pk)
    cart.add(product, price=product.price)
    return HttpResponse("Added")


def show(request):
    return render(request, 'shopping/cart.html')
