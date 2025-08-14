from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib import messages


def product_list(request):
    products = Product.objects.filter(active=True)
    return render(request, 'catalog/product_list.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    return render(request, 'catalog/product_detail.html', {'product': product})


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    cart = request.session.get('cart', {})
    pid = str(product.id)
    cart[pid] = {'name': product.name, 'price': float(product.price), 'qty': cart.get(pid, {'qty':0})['qty'] + 1}
    request.session['cart'] = cart
    messages.success(request, f"Added {product.name} to cart")
    return redirect('cart_view')


def cart_view(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['qty'] for item in cart.values())
    return render(request, 'catalog/cart.html', {'cart': cart, 'total': total})


def remove_from_cart(request, pid):
    cart = request.session.get('cart', {})
    if pid in cart: del cart[pid]
    request.session['cart'] = cart
    return redirect('cart_view')