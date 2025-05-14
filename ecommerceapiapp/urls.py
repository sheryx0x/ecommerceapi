from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.get_products),
    path('categories/', views.get_categories),
    path('checkout/', views.create_order),  
    path('cart/', views.view_cart),
    path('cart/add/', views.add_to_cart),
    path('cart/remove/', views.remove_from_cart),
    path('cart/clear/', views.clear_cart),
    path('products/', views.get_products),
    path('categories/', views.get_categories),  
]