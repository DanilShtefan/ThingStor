from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Coupon(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Процент'),
        ('fixed', 'Фиксированная сумма'),
    ]

    code = models.CharField('Промокод', max_length=50, unique=True)
    discount_type = models.CharField('Тип скидки', max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField('Значение скидки', max_digits=10, decimal_places=2,
        help_text='Процент (0–100) или фиксированная сумма в €')
    valid_from = models.DateTimeField('Действует с')
    valid_to = models.DateTimeField('Действует до')
    active = models.BooleanField('Активен', default=True)
    min_cart_amount = models.DecimalField('Мин. сумма корзины', max_digits=10, decimal_places=2,
        default=Decimal('0.00'))
    max_uses = models.PositiveIntegerField('Макс. использований', default=0,
        help_text='0 = без ограничений')
    max_discount_amount = models.DecimalField('Макс. сумма скидки', max_digits=10, decimal_places=2,
        default=Decimal('0'),
        help_text='0 = без ограничений. Для процентных купонов — максимальная скидка в €')
    used_count = models.PositiveIntegerField('Использовано раз', default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return self.code

    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return (
            self.active
            and self.valid_from <= now <= self.valid_to
            and (self.max_uses == 0 or self.used_count < self.max_uses)
        )

    def apply_discount(self, total):
        if self.discount_type == 'percentage':
            raw_discount = total * self.discount_value / Decimal('100')
            if self.max_discount_amount > 0 and raw_discount > self.max_discount_amount:
                return total - self.max_discount_amount
            return total - raw_discount
        return max(total - self.discount_value, Decimal('0'))
