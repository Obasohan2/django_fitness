from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal, ROUND_HALF_UP
from .models import Product, CartItem


def product_list(request):
    products = Product.objects.filter(active=True)
    return render(request, 'catalog/product_list.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    return render(request, 'catalog/product_detail.html', {'product': product})


def cart_view(request):
    cart_items = []
    total_price = Decimal("0.00")
    cart_count = 0

    if request.user.is_authenticated:
        # Use CartItem model for logged-in users
        user_cart_items = CartItem.objects.filter(user=request.user)

        for item in user_cart_items:
            line_total = (item.product.price * item.quantity).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            cart_items.append({
                'product': item.product,
                'quantity': item.quantity,
                'total': line_total
            })
            total_price += line_total
            cart_count += item.quantity

    else:
        # Use session-based cart for anonymous users
        session_cart = request.session.get('cart', {})
        if not isinstance(session_cart, dict):
            session_cart = {}

        for product_id, item in session_cart.items():
            try:
                product = Product.objects.get(id=int(product_id))
                qty = int(item.get('qty', 0))
                price = Decimal(str(item.get('price', product.price)))
                line_total = (qty * price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                cart_items.append({
                    'product': product,
                    'quantity': qty,
                    'total': line_total
                })
                total_price += line_total
                cart_count += qty

            except (Product.DoesNotExist, ValueError, TypeError):
                continue

    # Render the cart page with all cart context
    return render(request, 'catalog/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        'cart_count': cart_count,
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

        if product_id in cart and isinstance(cart[product_id], dict):
            cart[product_id]['qty'] += 1
        else:
            cart[product_id] = {
                'qty': 1,
                'price': str(product.price)
            }

        request.session['cart'] = cart
        request.session.modified = True  # Ensures Django saves the session

    messages.success(request, f"Added {product.name} to cart")
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
            request.session.modified = True

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
                    if product_id_str in cart and isinstance(cart[product_id_str], dict):
                        cart[product_id_str]['qty'] = quantity
                    else:
                        cart[product_id_str] = {
                            'qty': quantity,
                            'price': str(product.price)
                        }
                else:
                    cart.pop(product_id_str, None)

                request.session['cart'] = cart
                request.session.modified = True

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
            request.session.modified = True

    messages.success(request, "Cart cleared successfully")
    return redirect('cart_view')


def checkout(request):
    return HttpResponse("Checkout page coming soon.")
