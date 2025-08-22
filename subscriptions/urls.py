from django.urls import path
from . import views

app_name = "subscriptions"

urlpatterns = [
    path("", views.subscription_plans, name="plans"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("success/", views.subscription_success, name="subscription_success"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("cancel/", views.cancel_subscription, name="cancel_subscription"),
]
