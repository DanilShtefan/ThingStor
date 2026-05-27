from django.conf import settings
from decimal import Decimal
from main.models import Product
from .models import CartItem


class Cart:

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
        cart = self.session.get(settings.CART_SESSION_ID, {})
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def _load_from_db(self):
        items = CartItem.objects.filter(user=self.user).select_related('product')
        cart = {}
        for item in items:
            cart[str(item.product_id)] = {
                'quantity': item.quantity,
                'price': str(item.product.price),
            }
        self.cart = cart

    def _persist(self):
        if self._storage == 'session':
            self.session[settings.CART_SESSION_ID] = self.cart
            self.session.modified = True
        else:
            current_ids = {int(k) for k in self.cart}
            existing = CartItem.objects.filter(user=self.user)
            existing_ids = {item.product_id for item in existing}

            for item in existing:
                if item.product_id not in current_ids:
                    item.delete()

            for pid_str, data in self.cart.items():
                pid = int(pid_str)
                CartItem.objects.update_or_create(
                    user=self.user, product_id=pid,
                    defaults={'quantity': data['quantity']}
                )

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self._persist()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self._persist()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids).select_related('category').prefetch_related('images')
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        if self._storage == 'db':
            CartItem.objects.filter(user=self.user).delete()
        self.cart = {}
        if self._storage == 'session':
            if settings.CART_SESSION_ID in self.session:
                del self.session[settings.CART_SESSION_ID]
            self.session.modified = True

    def get_total_price(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids).only('id', 'discount')
        discounts = {str(p.id): p.discount for p in products}
        total = sum(
            (Decimal(item['price']) - (Decimal(item['price']) * Decimal(discounts.get(pid, 0) / 100))) * item['quantity']
            for pid, item in self.cart.items()
        )
        return format(total, '.2f')
