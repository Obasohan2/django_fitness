# from django.db import models
# from django.contrib.auth.models import User

# # Create your models here.

# INTERVALS = (
#     ('month','Monthly'),
#     ('year','Yearly'),
# )


# class SubscriptionPlan(models.Model):
#     name = models.CharField(max_length=120)
#     description = models.TextField(blank=True)
#     interval = models.CharField(max_length=10, choices=INTERVALS, default='month')
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     stripe_price_id = models.CharField(max_length=120, help_text='Price ID from Stripe', unique=True)
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name


# class UserSubscription(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
#     status = models.CharField(max_length=32, default='incomplete')  # active, canceled, past_due, etc
#     current_period_end = models.DateTimeField(null=True, blank=True)
#     stripe_subscription_id = models.CharField(max_length=120, blank=True)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user} → {self.plan} ({self.status})"