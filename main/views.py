from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Product, Category
from cart.forms import CartAddProductForm


def popular_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True).select_related('category').prefetch_related('images')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('product/_products.html', {
            'products': page_obj,
        })
        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next(),
        })

    return render(request, 'product/list.html', {
        'products': page_obj,
        'category': category,
        'categories': Category.objects.all(),
        'page_obj': page_obj,
        'paginator': paginator,
    })

def homepage(request):
    products = Product.objects.filter(available=True).select_related('category').prefetch_related('images').order_by('-created')[:4]
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

def about(request):
    return render(request, 'pages/about.html')

def materials(request):
    return render(request, 'pages/materials.html')

def contacts(request):
    return render(request, 'pages/contacts.html')

def delivery(request):
    return render(request, 'pages/delivery.html')

def care(request):
    return render(request, 'pages/care.html')

def sizes(request):
    return render(request, 'pages/sizes.html')

def faq(request):
    return render(request, 'pages/faq.html')