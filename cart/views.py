from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.models import Coupon
from coupons.coupon_session import CouponSession


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id = product_id, available=True)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product = product, quantity = cd['quantity'], override_quantity = cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id = product_id)
    cart.remove(product = product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    cs = CouponSession(request)
    coupon_error = cs.get_error()

    total_raw = Decimal(cart.get_total_price())
    discount = Decimal('0')
    if cs.code:
        try:
            coupon = Coupon.objects.get(code=cs.code)
            if coupon.is_valid():
                discounted = coupon.apply_discount(total_raw)
                discount = total_raw - discounted
        except Coupon.DoesNotExist:
            pass

    return render(request, 'cart/detail.html', {
        'cart': cart,
        'coupon_error': coupon_error,
        'discount': discount,
        'total_raw': total_raw,
        'total_discounted': total_raw - discount,
    })