from django.shortcuts import render, reverse, get_object_or_404, redirect
from .models import Product
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


def product_list(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
            
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'catalog/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category,
        active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'catalog/product_detail.html', context) 


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    cart = request.session.get('cart', {})
    pid = str(product.id)
    cart[pid] = {'name': product.name, 'price': float(product.price), 'qty': cart.get(pid, {'qty':0})['qty'] + 1}
    request.session['cart'] = cart
    messages.success(request, f"Added {product.name} to cart")
    return redirect('cart_view')


def cart_view(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['qty'] for item in cart.values())
    return render(request, 'catalog/cart.html', {'cart': cart, 'total': total})


def remove_from_cart(request, pid):
    cart = request.session.get('cart', {})
    if pid in cart: del cart[pid]
    request.session['cart'] = cart
    return redirect('cart_view')


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    product_list = Product.objects.filter(category=category, active=True)
    paginator = Paginator(product_list, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'products/category.html', {
        'category': category,
        'products': products
    })