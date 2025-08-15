from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProfileForm

# Create your views here.


@login_required
def me(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile_me')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/me.html', {'form': form})