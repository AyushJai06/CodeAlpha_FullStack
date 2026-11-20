
from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    products = Product.objects.filter(
        available=True
    ).order_by('-created_at')

    return render(request, 'home.html', {
        'products': products
    })


def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    return render(request, 'product_detail.html', {
        'product': product
    })
