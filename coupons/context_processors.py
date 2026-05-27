from .coupon_session import CouponSession
from .models import Coupon


def coupon(request):
    cs = CouponSession(request)
    if cs.code:
        try:
            coupon = Coupon.objects.get(code=cs.code)
            if coupon.is_valid():
                return {'coupon': coupon}
        except Coupon.DoesNotExist:
            pass
    return {'coupon': None}
