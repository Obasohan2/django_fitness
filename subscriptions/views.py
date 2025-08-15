from django.shortcuts import render

# Create your views here.


def subscribe_index(request):
    return render(request, "subscriptions/index.html")