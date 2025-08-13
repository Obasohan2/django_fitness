def cart(request):
    session_cart = request.session.get('cart', {})
    count = sum(item['qty'] for item in session_cart.values()) if session_cart else 0
    return {'cart_count': count}