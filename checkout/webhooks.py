import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from subscriptions.models import UserSubscription, SubscriptionPlan

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return HttpResponse(status=400)

    # Handle subscription events
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        if session.get('mode') == 'subscription':
            sub_id = session.get('subscription')
            email = session.get('customer_details', {}).get('email')
            try:
                us = UserSubscription.objects.filter(user__email=email).latest('created')
                us.status = 'active'
                us.stripe_subscription_id = sub_id
                us.save()
            except UserSubscription.DoesNotExist:
                pass

    if event['type'] == 'customer.subscription.updated':
        obj = event['data']['object']
        sub_id = obj['id']
        status = obj['status']
        period_end = obj['current_period_end']
        UserSubscription.objects.filter(stripe_subscription_id=sub_id).update(status=status)

    if event['type'] == 'customer.subscription.deleted':
        obj = event['data']['object']
        sub_id = obj['id']
        UserSubscription.objects.filter(stripe_subscription_id=sub_id).update(status='canceled')

    return HttpResponse(status=200)