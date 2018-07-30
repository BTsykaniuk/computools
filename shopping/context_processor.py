from carton.cart import Cart


def cart_items_count(request):
    """Custom context processor for counting items in Cart and Wishlist"""
    cart = Cart(session=request.session, session_key='CART')
    wish = Cart(session=request.session, session_key='WISH')

    request.session['cart_count'] = cart.count
    request.session['wish_count'] = wish.count

    return {'cart_count': request.session['cart_count'],
            'wish_count': request.session['wish_count']}
