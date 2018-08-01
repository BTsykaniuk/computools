from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from products_api.views import ProductsListView, ProductChangeView


schema_view = get_swagger_view(title='Product API')

# router = DefaultRouter()
# router.register(r'products',  ProductsListView)

urlpatterns = [
    path('products/', ProductsListView.as_view()),
    path('products/<int:pk>', ProductChangeView.as_view()),
    path('swagger/', schema_view),
]
