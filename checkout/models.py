from django.db import models
from django.conf import settings
from main.models import Product


class DeliveryAddress(models.Model):
    ADDRESS_TYPES = [
        ('manual', 'Ручной ввод'),
        ('cdek', 'ПВЗ CDEK'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='manual')
    is_default = models.BooleanField(default=False)

    city = models.CharField(max_length=100, blank=True)
    street = models.CharField('Улица', max_length=200, blank=True)
    house = models.CharField('Дом', max_length=20, blank=True)
    apartment = models.CharField('Квартира', max_length=20, blank=True)
    postal_code = models.CharField('Индекс', max_length=20, blank=True)
    recipient_name = models.CharField('Получатель', max_length=200, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)

    cdek_pvz_code = models.CharField(max_length=20, blank=True)
    cdek_pvz_address = models.CharField('Адрес ПВЗ', max_length=500, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_default', '-created']

    def __str__(self):
        if self.address_type == 'cdek':
            return f'ПВЗ CDEK: {self.cdek_pvz_address}'
        return f'{self.city}, {self.street} {self.house}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('confirmed', 'Подтверждён'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL, null=True)
    delivery_address_snapshot = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Заказ #{self.id} — {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product_name} x{self.quantity}'
