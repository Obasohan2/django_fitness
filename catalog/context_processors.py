from decimal import Decimal, ROUND_HALF_UP
from .models import CartItem


def cart(request):
    """Add cart data to template context"""
    session_cart = request.session.get("cart", {})

    if not isinstance(session_cart, dict):
        session_cart = {}

    count = Decimal("0")
    total = Decimal("0.00")

    cart_items = {}

    for pid, item in session_cart.items():
        if isinstance(item, dict):
            try:
                qty = Decimal(item.get("qty", 0))
                price = Decimal(item.get("price", 0))
                line_total = (qty * price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                count += qty
                total += line_total

                # copy item dict, add line_total
                cart_items[pid] = {
                    **item,
                    "qty": qty,
                    "price": price,
                    "line_total": line_total,
                }
            except (ValueError, TypeError, ArithmeticError):
                continue

    return {
        "cart_count": int(count),
        "cart_total": total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        "cart_items": cart_items,
    }


def cart_item_count(request):
    count = 0
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
    else:
        cart = request.session.get('cart', {})
        count = sum(cart.values())
    return {'cart_count': count}