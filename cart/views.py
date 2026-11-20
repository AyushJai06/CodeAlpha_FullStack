
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product


def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    current_quantity = cart.get(product_id, 0)

    if current_quantity < product.stock:
        cart[product_id] = current_quantity + 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')


def cart_detail(request):

    cart = request.session.get('cart', {})

    products = Product.objects.filter(
        id__in=cart.keys()
    )

    cart_items = []
    total = 0

    for product in products:

        quantity = cart.get(str(product.id), 0)

        subtotal = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

        total += subtotal

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@require_POST
def remove_from_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')

@require_POST
def update_quantity(request, product_id, action):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id not in cart:
        return redirect('cart_detail')

    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    quantity = cart[product_id]

    if action == 'increase':
        if quantity < product.stock:
            cart[product_id] = quantity + 1

    elif action == 'decrease':
        if quantity > 1:
            cart[product_id] = quantity - 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')

