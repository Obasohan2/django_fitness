from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SubscriptionPlan, UserSubscription
from .forms import SubscriptionSelectForm
import stripe  # <-- needed for cancel_subscription

@login_required
def subscription_plans(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'subscriptions/plans.html', {'plans': plans})

@login_required
def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionSelectForm(request.POST)
        if form.is_valid():
            plan = form.cleaned_data['plan']
            subscription, _ = UserSubscription.objects.get_or_create(user=request.user)
            subscription.plan = plan
            subscription.active = True
            subscription.save()
            return redirect('subscriptions:subscription_success')  # namespaced if using app_name
    else:
        form = SubscriptionSelectForm()
    return render(request, 'subscriptions/subscribe.html', {'form': form})

@login_required
def subscription_success(request):
    return render(request, 'subscriptions/success.html')

@login_required
def dashboard(request):
    user_sub = UserSubscription.objects.filter(user=request.user).first()
    return render(request, 'subscriptions/dashboard.html', {'user_sub': user_sub})

@login_required
def cancel_subscription(request):
    try:
        user_sub = UserSubscription.objects.get(user=request.user)
        if getattr(user_sub, "stripe_subscription_id", None):
            stripe.Subscription.modify(
                user_sub.stripe_subscription_id,
                cancel_at_period_end=True,
            )
            user_sub.status = 'canceled'
            user_sub.save()
            message = "Subscription cancellation requested. You'll retain access until the end of your billing cycle."
        else:
            message = "No active subscription found."
    except UserSubscription.DoesNotExist:
        message = "No subscription found."
    return render(request, 'subscriptions/cancel_confirm.html', {'message': message})
