from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('materials/', views.materials, name='materials'),
    path('contacts/', views.contacts, name='contacts'),
    path('delivery/', views.delivery, name='delivery'),
    path('care/', views.care, name='care'),
    path('sizes/', views.sizes, name='sizes'),
    path('faq/', views.faq, name='faq'),
    path('category/', views.popular_list, name='popular_list'),
    path('category/<slug:category_slug>/', views.popular_list, name='popular_list_by_category'),
    path('category/<slug:category_slug>/<int:id>/', views.product_detail, name='product_detail'),
    path('new-arrivals/', views.new_arrivals, name='new_arrivals'),
]
