from django.shortcuts import render, redirect
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def start_payment(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_view')
    line_items = []
    for pid, item in cart.items():
        line_items.append({
            'price_data': {
                'currency': 'gbp',
                'product_data': {'name': item['name']},
                'unit_amount': int(float(item['price']) * 100)
            },
            'quantity': int(item['qty']),
        })
    session = stripe.checkout.Session.create(
        mode='payment',
        line_items=line_items,
        success_url=f"{settings.SITE_URL}/checkout/success/?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{settings.SITE_URL}/shop/cart/",
    )
    return redirect(session.url)


def success(request):
    # clear cart and show thanks
    request.session['cart'] = {}
    return render(request, 'checkout/success.html')