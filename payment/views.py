from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib import messages
from decimal import Decimal
import stripe
from checkout.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('main:homepage')
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        line_items = []
        for item in order.items.all():
            line_items.append({
                'price_data': {
                    'unit_amount': int(item.product_price * Decimal('100')),
                    'currency': 'eur',
                    'product_data': {'name': item.product_name},
                },
                'quantity': item.quantity,
            })

        session_data = {
            'mode': 'payment',
            'client_reference_id': str(order.id),
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': line_items,
        }

        if order.discount_amount and order.coupon_code:
            coupon = stripe.Coupon.create(
                amount_off=int(order.discount_amount * Decimal('100')),
                currency='eur',
                duration='once',
            )
            session_data['discounts'] = [{'coupon': coupon.id}]

        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)

    return render(request, 'payment/process.html', {'order': order})


def payment_completed(request):
    order_id = request.session.pop('order_id', None)
    if order_id:
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            order.paid = True
            order.save(update_fields=['paid'])
            messages.success(request, f'Заказ #{order.id} оплачен!')
        except Order.DoesNotExist:
            pass
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
