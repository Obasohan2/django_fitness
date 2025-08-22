from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('name', 'unit_price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'total', 'currency', 'email', 'created')
    list_filter = ('status', 'currency', 'created')
    search_fields = ('id', 'email', 'stripe_session_id', 'stripe_payment_intent_id')
    date_hierarchy = 'created'
    inlines = [OrderItemInline]
    readonly_fields = ('created', 'updated')
