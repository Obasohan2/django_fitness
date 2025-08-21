from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscription_plans, name='subscription_plans'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('success/', views.subscription_success, name='subscription_success'),
]
