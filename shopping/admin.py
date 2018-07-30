from django.contrib import admin
from django.db.models import F
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'total_price', 'total_items_count', 'status', 'create_date', 'metadata']
    inlines = [OrderItemInline]

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        # Back Order Items
        if obj.status == 'CANCEL':
            for order_item in OrderItem.objects.filter(order=obj.pk).select_related('item'):
                order_item.item.quantity = F('quantity') + order_item.quantity
                order_item.item.save()

        obj.save()


