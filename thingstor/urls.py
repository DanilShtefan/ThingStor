from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from decouple import config

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('favorites/', include('favorites.urls', namespace='favorites')),
    path('users/', include('users.urls', namespace='users')),
    path('', include('checkout.urls', namespace='checkout')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('contacts/', include('contact.urls', namespace='contact')),
    path('', include('main.urls', namespace='main')),
]

if settings.DEBUG or config('RENDER', default='false').lower() == 'true':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
