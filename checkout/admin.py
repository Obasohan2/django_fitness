from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('name', 'unit_price', 'quantity', 'subtotal')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'email', 'status', 'total', 'currency',
        'created', 'is_paid'
    )
    list_filter = ('status', 'currency', 'created')
    search_fields = ('order_number', 'email', 'shipping_name', 'shipping_postcode')
    readonly_fields = (
        'order_number', 'user', 'email', 'total', 'currency', 'status',
        'stripe_session_id', 'stripe_payment_intent_id',
        'shipping_name', 'shipping_line1', 'shipping_line2',
        'shipping_city', 'shipping_postcode', 'shipping_country',
        'created', 'updated'
    )
    inlines = [OrderItemInline]
    ordering = ['-created']
    date_hierarchy = 'created'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'unit_price', 'quantity', 'subtotal')
    readonly_fields = ('subtotal',)
    search_fields = ('name',)
