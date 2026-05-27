from django.conf import settings
from main.models import Product


class Favorites:

    def __init__(self, request):
        self.session = request.session
        fav = self.session.get(settings.FAVORITES_SESSION_ID)

        if not fav:
            fav = self.session[settings.FAVORITES_SESSION_ID] = {}
        self.favorites = fav

    def add(self, product):
        product_id = str(product.id)

        if product_id not in self.favorites:
            self.favorites[product_id] = {}
            self.save()

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.favorites:
            del self.favorites[product_id]
            self.save()

    def toggle(self, product):
        product_id = str(product.id)

        if product_id in self.favorites:
            del self.favorites[product_id]
        else:
            self.favorites[product_id] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.favorites.keys()
        products = Product.objects.filter(id__in=product_ids, available=True).select_related('category').prefetch_related('images')
        for product in products:
            yield product

    @property
    def ids(self):
        return list(self.favorites.keys())

    def __len__(self):
        return len(self.favorites)

    def clear(self):
        del self.session[settings.FAVORITES_SESSION_ID]
