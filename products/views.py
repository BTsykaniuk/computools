from django.views import generic
from .models import *

# Create your views here.


class ProductList(generic.ListView):
    """View for product list"""
    model = Product
    template_name = 'index.html'

    context_object_name = 'product_list'

    def get_queryset(self):
        return Product.objects.all()
