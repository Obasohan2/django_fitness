from decimal import Decimal, ROUND_HALF_UP
from .models import Product, CartItem

def cart(request):
    """
    Provides cart_items, cart_count, cart_total, and grand_total for templates.
    Handles both authenticated users (DB) and anonymous users (session).
    """
    cart_items = []
    cart_total = Decimal("0.00")
    cart_count = 0  # total quantity of items

    if request.user.is_authenticated:
        user_cart_items = CartItem.objects.filter(user=request.user)
        for item in user_cart_items:
            line_total = (item.quantity * item.product.price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            cart_total += line_total
            cart_count += item.quantity

            cart_items.append({
                "product": item.product,
                "quantity": item.quantity,
                "price": item.product.price,
                "total": line_total,
            })
    else:
        session_cart = request.session.get("cart", {})
        if not isinstance(session_cart, dict):
            session_cart = {}

        for pid, item in session_cart.items():
            if isinstance(item, dict):
                try:
                    qty = int(item.get("qty", 0))
                    price = Decimal(str(item.get("price", "0.00")))
                    line_total = (qty * price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                    try:
                        product = Product.objects.get(pk=pid)
                    except Product.DoesNotExist:
                        continue

                    cart_total += line_total
                    cart_count += qty

                    cart_items.append({
                        "product": product,
                        "quantity": qty,
                        "price": price,
                        "total": line_total,
                    })

                except (ValueError, TypeError, ArithmeticError):
                    continue

    # For now, grand_total is same as cart_total (extendable to include tax/delivery)
    grand_total = cart_total

    return {
        "cart_items": cart_items,
        "cart_count": cart_count,
        "cart_total": cart_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        "grand_total": grand_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
    }
