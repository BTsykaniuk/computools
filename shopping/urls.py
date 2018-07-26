"""test_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import AddCartItemView, ShowCartView, RemoveCartItemView, AddWishItemView, ShowWishlistView, \
                   RemoveWishItemView, AddOrderView, CreateOrderView, CancelOrderView, PaymentView, CreatingChargeView

urlpatterns = [
    path('add/<int:pk>', AddCartItemView.as_view(), name='add_to_cart'),
    path('', ShowCartView.as_view(), name='show_cart'),
    path('remove/<int:pk>', RemoveCartItemView.as_view(), name='remove_single_cart'),
    path('wishlist/add/<int:pk>', AddWishItemView.as_view(), name='add_wish'),
    path('wishlist/', ShowWishlistView.as_view(), name='show_wish'),
    path('wishlist/remove/<int:pk>', RemoveWishItemView.as_view(), name='remove_single_wish'),
    path('order/', CreateOrderView.as_view(), name='show_order'),
    path('order/add', AddOrderView.as_view(), name='add_order'),
    path('order/delete/<int:pk>', CancelOrderView.as_view(), name='cancel_order'),
    path('order/payment/<int:pk>', PaymentView.as_view(), name='payment'),
    path('order/charge/', CreatingChargeView.as_view(), name='charge'),
]
