from django.contrib import admin
from .models import Item, OrderItem, Order

# Register your models here.

@admin.register(Item)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price',]
    list_filter = ['name', 'price',]
    search_fields = ['name', 'desc',]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity',]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_on',]
    list_filter = ['created_on',]
    search_fields = ['user', 'id']