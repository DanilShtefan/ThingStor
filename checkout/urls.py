from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('addresses/', views.address_list, name='address_list'),
    path('addresses/create/', views.address_create, name='address_create'),
    path('addresses/<int:address_id>/edit/', views.address_edit, name='address_edit'),
    path('addresses/<int:address_id>/delete/', views.address_delete, name='address_delete'),
    path('addresses/<int:address_id>/set-default/', views.address_set_default, name='address_set_default'),
    path('addresses/cdek/', views.address_cdek, name='address_cdek'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/pay/', views.order_pay, name='order_pay'),
    path('orders/<int:order_id>/cancel/', views.order_cancel, name='order_cancel'),
    path('cdek/cities/', views.cdek_cities, name='cdek_cities'),
    path('cdek/pvz/', views.cdek_pvz, name='cdek_pvz'),
]
