from test_store import settings
from django.shortcuts import render
from django.shortcuts import redirect, HttpResponse
from django.views import generic
from django.urls import reverse_lazy

from carton.cart import Cart
from .models import Order, OrderItem
from products.models import Item

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class AddCartItemView(generic.View):

    def get(self, request, pk):
        cart = Cart(session=request.session, session_key='CART')
        product = Item.objects.get(id=pk)
        cart.add(product, price=product.price)
        request.session['cart_count'] = cart.count
        return redirect('show_cart')


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
        return redirect('show_cart')


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


class CreateOrderView(generic.View):
    """Create Order"""

    def get(self, request):
        cart = Cart(session=request.session, session_key='CART')
        return render(request, 'shopping/create_order.html', {'order': cart})


class AddOrderView(generic.View):
    """Add order data to models Order & OrderItem"""
    model = Order

    def get(self, request):
        cart = Cart(session=request.session, session_key='CART')

        if self.valid(cart.items):
            """Add data to Order"""
            order_obj = self.model(total_price=cart.total,
                                   total_items_count=cart.count,
                                   status='WAITING',
                                   metadata={'None': 'None'})

            order_obj.save()

            """Add data to OrderItem"""
            for item in cart.items:
                item_obj = OrderItem(order=order_obj,
                                     item=Item.objects.get(name=item.product.name),
                                     quantity=item.quantity,
                                     total_price=item.subtotal)

                item_obj.save()

                # Update Item quantity
                item_quantity = Item.objects.filter(name=item_obj.item.name).values_list('quantity', flat=True)[0]

                new_quantity = item_quantity-item_obj.quantity
                print(new_quantity)

                if new_quantity > 0:
                    Item.objects.filter(name=item_obj.item.name).update(quantity=new_quantity)
                else:
                    Item.objects.filter(name=item_obj.item.name).update(quantity=0, active=False)

            request.session['CART'] = {}
            request.session.modified = True
            request.session['cart_count'] = 0
            request.session['order'] = True

            return redirect('payment', pk=order_obj.pk)

        else:
            return HttpResponse('Error!')

    @staticmethod
    def valid(items):
        """Validate cart items data"""

        valid = True
        for item in items:
            quantity = Item.objects.filter(name=item.product.name).values_list('quantity', flat=True)[0]
            if item.quantity >= quantity:
                valid = False

        return valid


class PaymentView(generic.DetailView):
    """View for Payment page"""
    model = Order
    template_name = "shopping/payment.html"

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context['stripe_key'] = settings.STRIPE_PUBLIC_KEY
        amount = Order.objects.filter(pk=self.kwargs['pk']).values_list('total_price', flat=True)[0]
        context['stripe_amount'] = int(amount*100)

        return context


class CancelOrderView(generic.DeleteView):
    """Cancel Order -> Delete order data from DB"""
    model = Order
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):

        request.session['order'] = False
        return super(CancelOrderView, self).delete(self, request, *args, **kwargs)


class CreatingChargeView(generic.View):
    """View for create Charge"""

    def post(self, request):
        print(self.request.session['order'])
        token = request.POST.get('stripeToken')

        order_pk = request.POST['order_pk']

        amount = Order.objects.filter(pk=order_pk).values_list('total_price', flat=True)[0]

        try:
            charge = stripe.Charge.create(
                amount=int(amount * 100),
                currency='usd',
                description=f'Charge for Order #{order_pk}',
                source=token,
            )

            # update Order payment status
            Order.objects.filter(pk=order_pk).update(status='SUCCESS', charge_id=charge.id)

            return HttpResponse('Payment success!')

        except stripe.error.CardError as ce:
            Order.objects.filter(pk=order_pk).update(status='ERROR')

            return HttpResponse('Payment error!')
