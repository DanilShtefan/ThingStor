from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from checkout.models import DeliveryAddress, Order


class AddressInline(admin.TabularInline):
    model = DeliveryAddress
    extra = 0
    fields = ['address_type', 'cdek_pvz_address', 'city', 'street', 'house', 'phone', 'is_default']
    readonly_fields = ['address_type', 'cdek_pvz_address', 'city', 'street', 'house', 'phone']
    can_delete = False
    max_num = 0
    verbose_name = 'Адрес'
    verbose_name_plural = 'Адреса доставки'


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    fields = ['id', 'status', 'total_price', 'created']
    readonly_fields = ['id', 'total_price', 'created']
    can_delete = False
    max_num = 0
    verbose_name = 'Заказ'
    verbose_name_plural = 'Заказы'
    show_change_link = True


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'order_count']
    list_filter = ['is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    inlines = [AddressInline, OrderInline]

    @admin.display(description='Заказов')
    def order_count(self, obj):
        return obj.orders.count()
