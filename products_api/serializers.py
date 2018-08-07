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

    def validate(self, attrs):

        errors_dict = {}

        for item in attrs['items']:
            if 'quantity' in item:
                if item['quantity'] < 0:
                    errors_dict['item.quantity'] = 'Item quantity must be positive'

                if item['quantity'] == 0:
                    item['active'] = False

            if 'price' in item:
                if item['price'] <= 0:
                    errors_dict['item.price'] = 'Item price must be positive'

        if errors_dict:
            raise serializers.ValidationError(errors_dict)

        return attrs

    def create(self, validated_data):
        """Create or delete Product items"""
        items_data = validated_data.pop('items')
        instance = Product.objects.get(name=validated_data['name'])

        self.create_delete_item(instance, items_data)

        return instance

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
        self.update_item(instance, items_data)

        return instance

    @staticmethod
    def create_delete_item(instance, active_items):
        """Create Item if id not exist"""

        items_to_delete = list(instance.items.values_list('id', flat=True))

        for item in active_items:
            item_id = item.get('id', None)

            if item_id:
                if item_id in items_to_delete:
                    items_to_delete.remove(item_id)
            else:
                """Create Item"""
                Item.objects.create(product=instance, **item)

        if items_to_delete:
            """Delete Items"""
            for item in items_to_delete:
                item_instance = Item.objects.get(id=item)
                item_instance.delete()

    @staticmethod
    def update_item(instance, items):
        """Update Item if exist"""

        for item in items:
            item_id = item.get('id', None)

            if item_id:
                Item.objects.filter(id=item_id, product=instance.id).update(product=instance, **item)
            else:
                raise ValueError('Missing item id')
