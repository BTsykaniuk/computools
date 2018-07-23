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
from .views import add_item, show_cart, remove_single_item, add_to_wish, show_wishlist, remove_single_wish

urlpatterns = [
    path('add/<int:pk>', add_item, name='add'),
    path('', show_cart, name='show'),
    path('remove/<int:pk>', remove_single_item, name='remove_single'),
    path('wishlist/add/<int:pk>', add_to_wish, name='add_wish'),
    path('wishlist/', show_wishlist, name='show_wish'),
    path('wishlist/remove/<int:pk>', remove_single_wish, name='remove_single_wish'),
]
