from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'total_price', 'total_items_count', 'status', 'create_date', 'metadata']
    inlines = [OrderItemInline]

    def total_price(self, obj):
        return obj.total_price

