from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.core.cache import cache
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.cache import cache_page
from .models import Product, Category
from cart.forms import CartAddProductForm


def popular_list(request, category_slug=None):
    category = None
    page_number = request.GET.get('page', 1)
    cache_key = f'products:{category_slug or "all"}:{page_number}'
    cached = cache.get(cache_key)

    if cached:
        page_products, total, has_next = cached
    else:
        products = Product.objects.filter(available=True).select_related('category').prefetch_related('images')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        paginator = Paginator(products, 8)
        page_obj = paginator.get_page(page_number)
        page_products = list(page_obj)
        total = paginator.count
        has_next = page_obj.has_next()
        cache.set(cache_key, (page_products, total, has_next), 300)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('product/_products.html', {
            'products': page_products,
        }, request=request)
        return JsonResponse({
            'html': html,
            'has_next': has_next,
        })

    return render(request, 'product/list.html', {
        'products': page_products,
        'category': category,
        'categories': Category.objects.all(),
        'has_next': has_next,
    })

def homepage(request):
    cache_key = 'homepage_products'
    products = cache.get(cache_key)
    if products is None:
        products = list(Product.objects.filter(available=True).select_related('category').prefetch_related('images').order_by('-created')[:4])
        cache.set(cache_key, products, 300)
    return render(request, 'main/index.html', {
        'products': products,
    })

def product_detail(request, category_slug, id):
    product = get_object_or_404(Product.objects.select_related('category').prefetch_related('images'), category__slug=category_slug, id=id)
    cart_product_form = CartAddProductForm()

    return render(request, 'product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
    })

def new_arrivals(request):
    page_number = request.GET.get('page', 1)
    cache_key = f'newarrivals:{page_number}'
    cached = cache.get(cache_key)

    if cached:
        page_products, total, has_next = cached
    else:
        thirty_days_ago = timezone.now() - timedelta(days=30)
        products = Product.objects.filter(
            available=True, created__gte=thirty_days_ago
        ).select_related('category').prefetch_related('images').order_by('-created')

        paginator = Paginator(products, 8)
        page_obj = paginator.get_page(page_number)
        page_products = list(page_obj)
        total = paginator.count
        has_next = page_obj.has_next()
        cache.set(cache_key, (page_products, total, has_next), 300)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('product/_products.html', {
            'products': page_products,
        }, request=request)
        return JsonResponse({
            'html': html,
            'has_next': has_next,
        })

    return render(request, 'product/list.html', {
        'products': page_products,
        'categories': Category.objects.all(),
        'has_next': has_next,
        'is_new_arrivals': True,
    })

@cache_page(86400)
def about(request):
    return render(request, 'pages/about.html')

@cache_page(86400)
def materials(request):
    return render(request, 'pages/materials.html')

@cache_page(86400)
def contacts(request):
    return render(request, 'pages/contacts.html')

@cache_page(86400)
def delivery(request):
    return render(request, 'pages/delivery.html')

@cache_page(86400)
def care(request):
    return render(request, 'pages/care.html')

@cache_page(86400)
def sizes(request):
    return render(request, 'pages/sizes.html')

@cache_page(86400)
def faq(request):
    return render(request, 'pages/faq.html')