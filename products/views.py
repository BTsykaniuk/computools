from django.views import generic
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from .models import Product, Item


class ProductListView(generic.ListView):
    """View for product list"""
    template_name = 'index.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Product.objects.filter(active=True).all()


class ProductDetailsView(generic.DetailView):
    """View for product details"""
    model = Product
    template_name = 'products/product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailsView, self).get_context_data(**kwargs)
        context['items'] = Item.objects.filter(product=kwargs['object'], active=True).all()
        return context


class ProductSearchView(generic.ListView):
    """View for Product search form"""
    model = Product
    template_name = 'index.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        query = Product.objects.filter(active=True).all()

        keys = self.request.GET.get('keys')

        if keys:
            search_q = SearchQuery(keys)
            vector = SearchVector('name')
            query = query.annotate(search=vector).filter(search=search_q)
            query = query.annotate(rank=SearchRank(vector, search_q)).order_by('-rank')

        return query

