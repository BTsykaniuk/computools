from test_store import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.db.models import F
from django.contrib import messages

from .models import Order, OrderItem
from products.models import Item
from carton.cart import Cart
from .mixins import AddToCartMixin, ShowCartMixin, RemoveCartItemMixin, CancelOrderMixin

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class AddCartItemView(AddToCartMixin, generic.View):
    """Add Items to Cart"""
    session_key = 'CART'
    redirect_view = 'show_cart'


class ShowCartView(ShowCartMixin, generic.View):
    """Show Cart details"""
    session_key = 'CART'
    template = 'shopping/cart.html'


class RemoveCartItemItemView(RemoveCartItemMixin, generic.View):
    """Remove Cart Item"""
    session_key = 'CART'
    redirect_view = 'show_cart'


class AddWishItemView(AddToCartMixin, generic.View):
    """Add Items to Wishlist"""
    session_key = 'WISH'
    redirect_view = 'show_wish'


class ShowWishlistView(ShowCartMixin, generic.View):
    """Show Wishlist details"""
    session_key = 'WISH'
    template = 'shopping/wishlist.html'


class RemoveWishItemView(RemoveCartItemMixin, generic.View):
    """Remove Wishlist Item"""
    session_key = 'WISH'
    redirect_view = 'show_wish'


class CreateOrderView(generic.View):
    """Create Order"""
    @staticmethod
    def get(request):
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
                                   metadata={})

            order_obj.save()

            """Add data to OrderItem"""
            for item in cart.items:
                item_obj = OrderItem(order=order_obj,
                                     item=Item.objects.get(id=item.product.id),
                                     quantity=item.quantity,
                                     total_price=item.subtotal)

                item_obj.save()

                # Update Item quantity
                item_quantity = Item.objects.get(id=item_obj.item.id)

                new_quantity = item_quantity.quantity - item_obj.quantity

                if new_quantity > 0:
                    item_quantity.quantity = F('quantity') - item_obj.quantity
                    item_quantity.save()
                else:
                    Item.objects.filter(id=item_obj.item.id).update(quantity=0, active=False)

            # Clear Cart
            request.session['CART'] = {}
            request.session.modified = True
            request.session['cart_count'] = 0

            return redirect('payment', pk=order_obj.pk)

        else:
            # Add message
            messages.error(request, 'Error!')
            return redirect('show_cart')

    @staticmethod
    def valid(items):
        """Validate cart items data"""

        valid = True
        for item in items:
            quantity = Item.objects.get(id=item.product.id)
            if item.quantity > quantity.quantity:
                valid = False

        return valid


class PaymentView(generic.DetailView):
    """View for Payment page"""
    model = Order
    template_name = "shopping/payment.html"

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context['stripe_key'] = settings.STRIPE_PUBLIC_KEY
        amount = Order.objects.get(pk=self.kwargs['pk'])
        context['stripe_amount'] = int(amount.total_price * 100)

        return context


class CancelOrderView(CancelOrderMixin, generic.View):
    """Cancel Order -> Change payment status to Cancel and back Items"""
    model = Order

    def get(self, request, pk):
        # Change payment status to Cancel
        self.model.objects.filter(pk=pk).update(status='CANCEL')

        # Back Items from Order
        self.back_item(pk)

        return redirect('index')


class CreatingChargeView(generic.View):
    """View for create Charge"""

    @staticmethod
    def post(request):
        token = request.POST.get('stripeToken')

        order_pk = request.POST['order_pk']

        amount = Order.objects.get(pk=order_pk)

        try:
            charge = stripe.Charge.create(
                amount=int(amount.total_price * 100),
                currency='usd',
                description=f'Charge for Order #{order_pk}',
                source=token,
            )

            # update Order payment status
            Order.objects.filter(pk=order_pk).update(status='SUCCESS', charge_id=charge.id)

            messages.success(request, 'Payment was successful! Thanks for the purchase!')

            return redirect('index')

        except stripe.error.CardError as ce:
            Order.objects.filter(pk=order_pk).update(status='ERROR')

            messages.error(request, 'Error! The payment has not passed!')

            return redirect('index')
