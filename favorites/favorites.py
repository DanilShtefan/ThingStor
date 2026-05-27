from django.conf import settings
from main.models import Product
from .models import FavoriteItem


class Favorites:

    def __init__(self, request):
        self.session = request.session
        self.user = request.user

        if self.user.is_authenticated:
            self._storage = 'db'
            self._load_from_db()
        else:
            self._storage = 'session'
            self._load_from_session()

    def _load_from_session(self):
        fav = self.session.get(settings.FAVORITES_SESSION_ID, {})
        if not fav:
            fav = self.session[settings.FAVORITES_SESSION_ID] = {}
        self.favorites = fav

    def _load_from_db(self):
        items = FavoriteItem.objects.filter(user=self.user).only('product_id')
        self.favorites = {str(item.product_id): {} for item in items}

    def _persist(self):
        if self._storage == 'session':
            self.session[settings.FAVORITES_SESSION_ID] = self.favorites
            self.session.modified = True
        else:
            current_ids = {int(k) for k in self.favorites}
            existing = FavoriteItem.objects.filter(user=self.user)
            existing_ids = {item.product_id for item in existing}

            for item in existing:
                if item.product_id not in current_ids:
                    item.delete()

            for pid_str in self.favorites:
                pid = int(pid_str)
                FavoriteItem.objects.get_or_create(user=self.user, product_id=pid)

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.favorites:
            self.favorites[product_id] = {}
            self._persist()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.favorites:
            del self.favorites[product_id]
            self._persist()

    def toggle(self, product):
        product_id = str(product.id)
        if product_id in self.favorites:
            del self.favorites[product_id]
        else:
            self.favorites[product_id] = {}
        self._persist()

    def __iter__(self):
        product_ids = self.favorites.keys()
        products = Product.objects.filter(id__in=product_ids, available=True).select_related('category').prefetch_related('images')
        for product in products:
            yield product

    @property
    def ids(self):
        return list(self.favorites.keys())

    def has(self, product_id):
        return str(product_id) in self.favorites

    def __len__(self):
        return len(self.favorites)

    def clear(self):
        if self._storage == 'db':
            FavoriteItem.objects.filter(user=self.user).delete()
        self.favorites = {}
        if self._storage == 'session':
            if settings.FAVORITES_SESSION_ID in self.session:
                del self.session[settings.FAVORITES_SESSION_ID]
            self.session.modified = True
