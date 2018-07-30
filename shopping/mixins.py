from django.shortcuts import redirect, render
from .models import Item, OrderItem
from django.db.models import F
from carton.cart import Cart


class AddToCartMixin(object):

    def get(self, request, pk):
        return self.add_item(request, pk)

    def add_item(self, request, item_id):
        cart = Cart(session=request.session, session_key=self.session_key)
        product = self.get_product(item_id)
        cart.add(product, price=product.price)

        return redirect(self.redirect_view)

    @staticmethod
    def get_product(product_id):
        return Item.objects.get(id=product_id)


class ShowCartMixin(object):

    def get(self, request):
        cart = Cart(session=request.session, session_key=self.session_key)
        return render(request, self.template, {'cart': cart})


class RemoveCartItemMixin(AddToCartMixin, object):

    def get(self, request, pk):
        return self.remove_item(request, pk)

    def remove_item(self, request, item_id):
        cart = Cart(session=request.session, session_key=self.session_key)
        product = self.get_product(item_id)
        cart.remove_single(product)

        return redirect(self.redirect_view)


class CancelOrderMixin(object):

    @staticmethod
    def back_item(order_id):
        for order_item in OrderItem.objects.filter(order=order_id).select_related('item'):
            order_item.item.quantity = F('quantity') + order_item.quantity
            order_item.item.save()



