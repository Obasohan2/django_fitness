from django.urls import path
from . import views
from .webhooks import stripe_webhook

urlpatterns = [
    path('start/', views.start_payment, name='start_payment'),
    path('success/', views.success, name='checkout_success'),
    path('webhooks/stripe/', stripe_webhook, name='stripe_webhook'),
]