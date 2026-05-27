from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.conf import settings
from cart.models import CartItem
from favorites.models import FavoriteItem


@receiver(user_logged_in)
def migrate_cart_on_login(sender, request, user, **kwargs):
    session = request.session

    cart_data = session.get(settings.CART_SESSION_ID, {})
    if cart_data:
        for pid_str, data in cart_data.items():
            CartItem.objects.update_or_create(
                user=user, product_id=int(pid_str),
                defaults={'quantity': data.get('quantity', 1)}
            )
        del session[settings.CART_SESSION_ID]
        session.modified = True

    fav_data = session.get(settings.FAVORITES_SESSION_ID, {})
    if fav_data:
        for pid_str in fav_data:
            FavoriteItem.objects.get_or_create(
                user=user, product_id=int(pid_str)
            )
        del session[settings.FAVORITES_SESSION_ID]
        session.modified = True
