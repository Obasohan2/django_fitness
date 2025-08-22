import uuid
from datetime import datetime
import random
import string
from decimal import Decimal

from django.db import models
from django.contrib.auth import get_user_model
from catalog.models import Product

User = get_user_model()


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_FAILED = 'failed'
    STATUS_REFUNDED = 'refunded'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_PAID, 'Paid'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_REFUNDED, 'Refunded'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(blank=True)

    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='gbp')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)

    stripe_session_id = models.CharField(max_length=255, unique=True, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)

    shipping_name = models.CharField(max_length=120, blank=True)
    shipping_line1 = models.CharField(max_length=120, blank=True)
    shipping_line2 = models.CharField(max_length=120, blank=True)
    shipping_city = models.CharField(max_length=120, blank=True)
    shipping_postcode = models.CharField(max_length=20, blank=True)
    shipping_country = models.CharField(max_length=2, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    order_number = models.CharField(max_length=32, unique=True, editable=False, blank=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['stripe_session_id']),
            models.Index(fields=['status']),
            models.Index(fields=['created']),
            models.Index(fields=['order_number']),
        ]

    def __str__(self):
        return f"Order #{self.order_number or self.id or '—'} · {self.get_status_display()} · {self.total} {self.currency.upper()}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_unique_order_number()
        super().save(*args, **kwargs)

    def _generate_unique_order_number(self):
        """
        Generate a unique order number in the format: ORD-YYYYMMDD-XXXXXX
        """
        date_str = datetime.now().strftime("%Y%m%d")
        prefix = "ORD"
        while True:
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            order_number = f"{prefix}-{date_str}-{random_suffix}"
            if not Order.objects.filter(order_number=order_number).exists():
                return order_number

    @property
    def is_paid(self):
        return self.status == self.STATUS_PAID

    def recalc_total(self):
        total = sum((item.subtotal for item in self.items.all()), Decimal('0.00'))
        self.total = total.quantize(Decimal('0.01'))
        return self.total

