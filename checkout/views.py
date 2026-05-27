import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import DeliveryAddress, Order, OrderItem
from .forms import AddressForm, CdekAddressForm
from .cdek_api import CdekApi
from cart.cart import Cart


@login_required
def address_list(request):
    addresses = DeliveryAddress.objects.filter(user=request.user)
    return render(request, 'checkout/address_list.html', {'addresses': addresses})


@login_required
def address_create(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            addr = form.save(commit=False)
            addr.user = request.user
            if not DeliveryAddress.objects.filter(user=request.user).exists():
                addr.is_default = True
            addr.save()
            messages.success(request, 'Адрес добавлен')
            return redirect('checkout:address_list')
    else:
        form = AddressForm(initial={'address_type': 'manual'})
    return render(request, 'checkout/address_form.html', {'form': form, 'title': 'Новый адрес'})


@login_required
def address_edit(request, address_id):
    addr = get_object_or_404(DeliveryAddress, id=address_id, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=addr)
        if form.is_valid():
            form.save()
            messages.success(request, 'Адрес обновлён')
            return redirect('checkout:address_list')
    else:
        form = AddressForm(instance=addr)
    return render(request, 'checkout/address_form.html', {'form': form, 'title': 'Редактировать адрес'})


@login_required
def address_delete(request, address_id):
    addr = get_object_or_404(DeliveryAddress, id=address_id, user=request.user)
    addr.delete()
    messages.success(request, 'Адрес удалён')
    return redirect('checkout:address_list')


@login_required
def address_set_default(request, address_id):
    addr = get_object_or_404(DeliveryAddress, id=address_id, user=request.user)
    DeliveryAddress.objects.filter(user=request.user).update(is_default=False)
    addr.is_default = True
    addr.save()
    return redirect('checkout:address_list')


@login_required
def address_cdek(request):
    if request.method == 'POST':
        form = CdekAddressForm(request.POST)
        if form.is_valid():
            addr = form.save(commit=False)
            addr.user = request.user
            if not DeliveryAddress.objects.filter(user=request.user).exists():
                addr.is_default = True
            addr.save()
            messages.success(request, 'ПВЗ CDEK добавлен')
            return redirect('checkout:address_list')
    else:
        form = CdekAddressForm(initial={'address_type': 'cdek'})
    return render(request, 'checkout/address_cdek.html', {'form': form})


@require_GET
def cdek_cities(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'cities': []})
    api = CdekApi()
    try:
        cities = api.search_cities(query)
    except Exception:
        return JsonResponse([], safe=False)
    return JsonResponse(cities, safe=False)


@require_GET
def cdek_pvz(request):
    city_code = request.GET.get('city_code', '')
    api = CdekApi()
    try:
        pvz_list = api.get_pvz(city_code=city_code if city_code else None)
    except Exception:
        return JsonResponse([], safe=False)
    return JsonResponse(pvz_list, safe=False)


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Корзина пуста')
        return redirect('cart:cart_detail')

    addresses = DeliveryAddress.objects.filter(user=request.user)
    default_addr = addresses.filter(is_default=True).first()

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        if not address_id:
            messages.error(request, 'Выберите адрес доставки')
            return redirect('checkout:checkout')

        addr = get_object_or_404(DeliveryAddress, id=address_id, user=request.user)
        total = cart.get_total_price()

        order = Order.objects.create(
            user=request.user,
            delivery_address=addr,
            delivery_address_snapshot=str(addr),
            total_price=total,
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                product_name=item['product'].name,
                product_price=item['price'],
                quantity=item['quantity'],
            )

        cart.clear()
        messages.success(request, f'Заказ #{order.id} оформлен!')
        return redirect('checkout:order_detail', order_id=order.id)

    return render(request, 'checkout/checkout.html', {
        'cart': cart,
        'addresses': addresses,
        'default_addr': default_addr,
    })


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'checkout/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'checkout/order_detail.html', {'order': order})
