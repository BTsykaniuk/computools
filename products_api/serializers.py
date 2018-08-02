from rest_framework import serializers

from products.models import Product, Item


class ItemSerializer(serializers.ModelSerializer):
    """DRF serializer for Item model"""
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Item
        fields = ('id', 'name', 'active', 'price', 'quantity', 'metadata')


class ProductSerializer(serializers.ModelSerializer):
    """DRF serializer for Product model"""
    items = ItemSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'active', 'image', 'items')

    def create(self, valid_data):
        """Save data to Item model"""
        items = valid_data.pop('items')
        product = Product.objects.create(**valid_data)

        for item in items:
            Item.objects.create(product=product, **item)

        return product

    def update(self, instance, validated_data):
        """Full update Product and Items"""
        items_data = validated_data.pop('items')

        # Update Product model
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.image = validated_data.get('image', instance.image)

        instance.save()

        # Update or create items
        for item in items_data:
            item_id = item.get('id', None)

            if item_id:
                Item.objects.filter(id=item_id, product=instance.id).update(product=instance, **item)
            else:
                Item.objects.create(product=instance, **item)

        return instance
