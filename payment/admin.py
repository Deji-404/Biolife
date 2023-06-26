from django.contrib import admin
from .models import Payment

# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['username', 'address', 'phone', 'amount', 'paid', 'order', 'updated_on']
    list_filter = ['username', 'address', 'paid', 'created_on', 'updated_on']
