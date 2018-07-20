from django.views import generic
from .models import Product, Item


class ProductListView(generic.ListView):
    """View for product list"""
    template_name = 'index.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Product.objects.filter(active=True).all()


class ProductDetailsView(generic.DeleteView):
    """View for product details"""
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailsView, self).get_context_data(**kwargs)
        # print(kwargs)
        context['items'] = Item.objects.filter(product=kwargs['object']).all()
        return context

