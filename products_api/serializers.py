from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """DRF serializer for Product model"""

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'active', 'image')
