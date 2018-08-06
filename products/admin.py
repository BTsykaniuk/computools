from django.contrib import admin
from .models import Item, Product


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'create_date', 'update_date', 'active']

    def save_model(self, request, obj, form, change):
        if obj.quantity > 0:
            obj.active = True
        else:
            obj.active = False

        obj.save()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'create_date', 'update_date', 'active']
