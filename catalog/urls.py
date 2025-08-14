from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/remove/<str:pid>/', views.remove_from_cart, name='cart_remove'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:slug>/add/', views.add_to_cart, name='add_to_cart'),
]