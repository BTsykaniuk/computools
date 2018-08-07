from django.db.models import Q

from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions

from products.models import Product
from products_api.serializers import ProductSerializer


class ProductsListView(generics.ListCreateAPIView):
    """CBV for all products"""

    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('active',)

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.all()
        query = self.request.GET.get('q')

        if query == 'items':
            queryset = queryset.exclude(items__isnull=True)

        return query


class ProductChangeView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    """CBV for read, write, delete and update single Product"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = (permissions.IsAdminUser, )
