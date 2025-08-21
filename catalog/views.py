from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


def product_list(request):
    products = Product.objects.filter(active=True)
    return render(request, 'catalog/product_list.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    return render(request, 'catalog/product_detail.html', {'product': product})


def cart_view(request):
    if request.user.is_authenticated:
        # Use CartItem model for logged-in users
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        context_cart_items = cart_items  # list of CartItem instances
    else:
        # Use session-based cart for anonymous users
        session_cart = request.session.get('cart', {})
        cart_items = []
        total_price = 0

        for product_id, quantity in session_cart.items():
            try:
                product = Product.objects.get(id=int(product_id))
                item_total = product.price * quantity
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total': item_total
                })
                total_price += item_total
            except (Product.DoesNotExist, ValueError):
                continue

        context_cart_items = cart_items  # list of dicts

    return render(request, 'catalog/cart.html', {
        'cart_items': context_cart_items,
        'total_price': total_price,
        'cart_count': len(context_cart_items),
        'user_is_authenticated': request.user.is_authenticated,
    })


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart = request.session.get('cart', {})
        product_id = str(product.id)

        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1

        request.session['cart'] = cart
    messages.success(request, f"Added {product.name} to cart")
    print(request.session['cart'])
    return redirect('product_detail', slug=slug)


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user, product=product).delete()
    else:
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        if product_id_str in cart:
            del cart[product_id_str]
            request.session['cart'] = cart

    messages.success(request, f"Removed {product.name} from cart.")
    return redirect('cart_view')


def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)

        try:
            quantity = int(quantity)
            product = get_object_or_404(Product, id=product_id)

            if request.user.is_authenticated:
                cart_item = CartItem.objects.get(user=request.user, product=product)
                if quantity > 0:
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    cart_item.delete()
            else:
                cart = request.session.get('cart', {})
                product_id_str = str(product_id)

                if quantity > 0:
                    cart[product_id_str] = quantity
                else:
                    cart.pop(product_id_str, None)

                request.session['cart'] = cart

            messages.success(request, "Cart updated successfully")

        except (ValueError, CartItem.DoesNotExist):
            messages.error(request, "Invalid operation")

    return redirect('cart_view')


def clear_cart(request):
    """Clear all items from cart"""
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user).delete()
    else:
        if 'cart' in request.session:
            del request.session['cart']

    messages.success(request, "Cart cleared successfully")
    return redirect('cart_view')


def checkout(request):
    return HttpResponse("Checkout page coming soon.")