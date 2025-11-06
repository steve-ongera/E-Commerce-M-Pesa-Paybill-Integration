from django.urls import path
from . import views

urlpatterns = [
    # Product URLs
    path('', views.product_list, name='product_list'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Cart URLs
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Checkout & Payment URLs
    path('checkout/', views.checkout, name='checkout'),
    path('check-payment-status/<int:order_id>/', views.check_payment_status, name='check_payment_status'),
    
    # M-Pesa Callback URL
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
    
    # Order URLs
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]