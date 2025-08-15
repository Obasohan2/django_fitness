# subscriptions/urls.py
from django.urls import path
from . import views

app_name = "subscriptions"

urlpatterns = [
    path("", views.subscribe_index, name="index"),
]
