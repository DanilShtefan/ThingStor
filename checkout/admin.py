from django.contrib import admin
from .models import DeliveryAddress, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['product', 'product_name', 'product_price', 'quantity']
    readonly_fields = ['product', 'product_name', 'product_price', 'quantity']
    can_delete = False
    max_num = 0


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address_type', 'display_address', 'phone', 'is_default', 'created']
    list_filter = ['address_type', 'is_default']
    search_fields = ['user__username', 'cdek_pvz_address', 'city', 'street', 'phone']

    @admin.display(description='Адрес')
    def display_address(self, obj):
        return str(obj)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created']
    list_filter = ['status', 'created']
    search_fields = ['user__username', 'id']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['delivery_address_snapshot', 'created', 'updated']
