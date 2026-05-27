from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product
from .favorites import Favorites


@require_POST
def favorites_add(request, product_id):
    fav = Favorites(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    fav.add(product)
    return redirect(request.META.get('HTTP_REFERER', 'favorites:favorites_detail'))

@require_POST
def favorites_remove(request, product_id):
    fav = Favorites(request)
    product = get_object_or_404(Product, id=product_id)
    fav.remove(product)
    return redirect(request.META.get('HTTP_REFERER', 'favorites:favorites_detail'))

@require_POST
def favorites_toggle(request, product_id):
    fav = Favorites(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    fav.toggle(product)
    return redirect(request.META.get('HTTP_REFERER', 'favorites:favorites_detail'))

def favorites_detail(request):
    fav = Favorites(request)
    return render(request, 'favorites/favorites.html', {
        'favorites': fav
    })
