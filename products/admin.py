from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'create_date', 'update_date', 'active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'create_date', 'update_date', 'active']



