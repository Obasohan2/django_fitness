# subscriptions/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SubscriptionPlan, UserSubscription
from .forms import SubscriptionSelectForm

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
            subscription, created = UserSubscription.objects.get_or_create(user=request.user)
            subscription.plan = plan
            subscription.active = True
            subscription.save()
            return redirect('subscription_success')
    else:
        form = SubscriptionSelectForm()
    
    return render(request, 'subscriptions/subscribe.html', {'form': form})


@login_required
def subscription_success(request):
    return render(request, 'subscriptions/success.html')
