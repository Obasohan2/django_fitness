from django.shortcuts import render

# Create your views here.


def checkout(request):
    # You can add cart/order retrieval logic here
    return render(request, "orders/checkout.html")
