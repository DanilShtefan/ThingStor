from django.conf import settings


class CouponSession:
    def __init__(self, request):
        self.session = request.session
        self._load()

    def _load(self):
        self.code = self.session.get(settings.COUPON_SESSION_ID)

    def set(self, code):
        self.session[settings.COUPON_SESSION_ID] = code
        self.session.modified = True
        self.code = code

    def remove(self):
        if settings.COUPON_SESSION_ID in self.session:
            del self.session[settings.COUPON_SESSION_ID]
            self.session.modified = True
        self.code = None

    def set_error(self, msg):
        self.session['coupon_error'] = msg
        self.session.modified = True

    def get_error(self):
        return self.session.pop('coupon_error', None)

    def __str__(self):
        return self.code or ''
