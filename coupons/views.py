from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import ApplyCouponForm
from .models import Coupon
from .coupon_session import CouponSession


@require_POST
def apply_coupon(request):
    form = ApplyCouponForm(request.POST)
    cs = CouponSession(request)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            cs.set_error('Промокод не найден')
            return redirect('cart:cart_detail')

        if not coupon.is_valid():
            cs.set_error('Промокод истёк или больше не активен')
            return redirect('cart:cart_detail')

        cs.set(code)
        messages.success(request, f'Промокод {code} применён!')
    return redirect('cart:cart_detail')


@require_POST
def remove_coupon(request):
    cs = CouponSession(request)
    cs.remove()
    return redirect('cart:cart_detail')
