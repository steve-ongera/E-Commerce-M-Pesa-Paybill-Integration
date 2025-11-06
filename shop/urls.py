from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/search-suggestions/', views.search_suggestions, name='search'),
    # Product URLs
    path('products/', views.product_list, name='products'),
    path('category/<int:category_id>/', views.category_view, name='category'),

     path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_products, name='category'),
    path('brand/<slug:slug>/', views.brand_products, name='brand'),
    path('search/', views.search_products, name='search'),
    
    # Cart URLs
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    
    # Wishlist URLs
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/', views.add_to_wishlist, name='add_to_wishlist'),
    
    # Review URLs
    path('product/<int:product_id>/review/', views.submit_review, name='submit_review'),
    path('reviews/<int:review_id>/helpful/', views.mark_review_helpful, name='mark_review_helpful'),
    
    # Checkout & Payment URLs
    path('checkout/', views.checkout, name='checkout'),
    path('mpesa/check-payment-status/<int:order_id>/', views.check_payment_status, name='check_payment_status'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
    
    # Order URLs
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]