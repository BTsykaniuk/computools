from rest_framework import generics
from rest_framework.parsers import MultiPartParser

from products.models import Product
from products_api.serializers import ProductSerializer


class ProductsListView(generics.ListCreateAPIView):
    """CBV for all products"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser,)


class ProductChangeView(generics.RetrieveUpdateDestroyAPIView):
    """CBV for read, write, delete and update single Product"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser,)

