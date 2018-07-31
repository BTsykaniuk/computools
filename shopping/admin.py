from django.contrib import admin
from .models import Order, OrderItem
from .mixins import CancelOrderMixin


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(CancelOrderMixin, admin.ModelAdmin):
    list_display = ['id', 'total_price', 'total_items_count', 'status', 'create_date', 'metadata']
    inlines = [OrderItemInline]
    list_filter = ['status']

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        # Back Order Items
        if obj.status == 'CANCEL':
            self.back_item(obj.pk)

        obj.save()


