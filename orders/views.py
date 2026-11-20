
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from decimal import Decimal

from .models import Order, OrderItem
from store.models import Product


def checkout(request):

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart_detail')

    products = Product.objects.filter(
        id__in=cart.keys(),
        available=True
    )

    cart_items = []
    total = Decimal('0.00')

    for product in products:

        quantity = int(cart.get(str(product.id), 0))

        if quantity <= 0:
            continue

        subtotal = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

        total += subtotal

    if not cart_items:
        return redirect('cart_detail')

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()

        if not all([
            name, email, phone, address,
            city, state, pincode
        ]):
            return render(request, 'orders/checkout.html', {
                'cart_items': cart_items,
                'total': total,
                'error': 'Please fill in all fields.'
            })

        try:
            with transaction.atomic():

                product_ids = [item['product'].id for item in cart_items]

                locked_products = {
                    p.id: p for p in Product.objects.select_for_update().filter(
                        id__in=product_ids,
                        available=True
                    )
                }

                for item in cart_items:
                    product = locked_products.get(item['product'].id)

                    if not product or product.stock < item['quantity']:
                        raise ValueError(
                            f"Insufficient stock for {item['product'].name}."
                        )

                order = Order.objects.create(
                    customer_name=name,
                    email=email,
                    phone=phone,
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode,
                    total_amount=total,
                    payment_method='COD'
                )

                for item in cart_items:

                    product = locked_products[item['product'].id]

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                        price=product.price
                    )

                    product.stock -= item['quantity']
                    product.save(update_fields=['stock'])

        except ValueError as error:
            return render(request, 'orders/checkout.html', {
                'cart_items': cart_items,
                'total': total,
                'error': str(error)
            })

        request.session['cart'] = {}
        request.session.modified = True

        return redirect('order_success', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


def order_success(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    return render(request, 'orders/success.html', {
        'order': order
    })
