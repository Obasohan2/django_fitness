# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.conf import settings
# from .models import SubscriptionPlan, UserSubscription
# import stripe

# stripe.api_key = settings.STRIPE_SECRET_KEY


# def plans(request):
#     return render(request, 'subscriptions/plans.html', {'plans': SubscriptionPlan.objects.filter(active=True)})

# @login_required
# def start_checkout(request, plan_id):
#     plan = get_object_or_404(SubscriptionPlan, pk=plan_id, active=True)
#     session = stripe.checkout.Session.create(
#         mode='subscription',
#         line_items=[{'price': plan.stripe_price_id, 'quantity': 1}],
#         success_url=f"{settings.SITE_URL}/subscribe/success/?session_id={{CHECKOUT_SESSION_ID}}",
#         cancel_url=f"{settings.SITE_URL}/subscribe/cancel/",
#         customer_email=request.user.email or None,
#     )
#     # Create or mark a pending subscription locally
#     UserSubscription.objects.update_or_create(user=request.user, plan=plan, defaults={'status': 'incomplete'})
#     return redirect(session.url)


# def success(request):
#     return render(request, 'subscriptions/success.html')


# def cancel(request):
#     return render(request, 'subscriptions/cancel.html')

from django.shortcuts import render

def plans(request):
    return render(request, 'subscriptions/plans.html') 