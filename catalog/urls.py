from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="products"),
    # Cart URLs - all under cart/ prefix
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),
    
    # Product detail
    path("<slug:slug>/", views.product_detail, name="product_detail"),
]