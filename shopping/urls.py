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
from .views import AddToCartView, ShowCartView, RemoveSingleItemView

urlpatterns = [
    path('add/<int:pk>', AddToCartView.as_view(), name='add'),
    path('', ShowCartView.as_view(), name='show'),
    path('remove/<int:pk>', RemoveSingleItemView.as_view(), name='remove_single'),
]
