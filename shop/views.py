from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.db import transaction
from django.conf import settings
import requests
import base64
import json
from datetime import datetime
import logging
from .models import *

logger = logging.getLogger(__name__)

from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category

def search_suggestions(request):
    """API endpoint for search autocomplete"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    # Search in product names and descriptions
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        is_active=True
    ).values('id', 'name')[:10]
    
    suggestions = [{'id': p['id'], 'name': p['name']} for p in products]
    
    return JsonResponse({'suggestions': suggestions})


def home_view(request):
    """Home page view"""
    categories = Category.objects.all()[:8]
    featured_products = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
    bestsellers = Product.objects.filter(is_active=True).order_by('-id')[:8]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'bestsellers': bestsellers,
    }
    
    return render(request, 'store/home.html', context)

import requests
import base64
import logging
from datetime import datetime
from django.conf import settings

logger = logging.getLogger(__name__)


def get_mpesa_access_token():
    """
    Get M-Pesa access token using Consumer Key and Secret
    """
    try:
        # Determine the correct URL based on environment
        if settings.MPESA_ENVIRONMENT == 'sandbox':
            url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        else:
            url = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        
        # Create Basic Auth credentials
        consumer_key = settings.MPESA_CONSUMER_KEY
        consumer_secret = settings.MPESA_CONSUMER_SECRET
        
        # Encode credentials in base64
        credentials = f"{consumer_key}:{consumer_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        # Set headers
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
        
        logger.info("Requesting M-Pesa access token...")
        
        # Make the request
        response = requests.get(url, headers=headers, timeout=30)
        
        # Log response for debugging
        logger.info(f"Access token response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            access_token = result.get('access_token')
            
            if access_token:
                logger.info("Successfully obtained M-Pesa access token")
                return access_token
            else:
                logger.error(f"No access token in response: {result}")
                return None
        else:
            logger.error(
                f"Failed to get access token. Status: {response.status_code}, "
                f"Response: {response.text}"
            )
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error getting access token: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error getting M-Pesa access token: {str(e)}")
        return None


def generate_password():
    """
    Generate password and timestamp for STK Push
    Password = Base64(Shortcode + Passkey + Timestamp)
    """
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Concatenate: Shortcode + Passkey + Timestamp
    data_to_encode = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
    
    # Encode in base64
    password = base64.b64encode(data_to_encode.encode()).decode()
    
    return password, timestamp




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Avg
from django.contrib import messages
from .models import (
    Product, ProductImage, ProductSpecification, ProductVariant,
    Review, ReviewImage, Wishlist, Cart, CartItem, Order, OrderItem
)
import json


def product_detail(request, slug):
    """
    Display product detail page with all information
    """
    # Get the product
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Increment view count
    product.view_count = (product.view_count or 0) + 1
    product.save(update_fields=['view_count'])
    
    # Get related products (same category)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    # Get all images
    product_images = product.images.all()
    
    # Get specifications
    specifications = product.specifications.all()
    
    # Get active variants
    variants = product.variants.filter(is_active=True)
    
    # Get approved reviews
    reviews = product.reviews.filter(is_approved=True).order_by('-created_at')
    
    # Calculate rating breakdown
    rating_breakdown = {}
    for i in range(1, 6):
        count = reviews.filter(rating=i).count()
        percentage = (count / reviews.count() * 100) if reviews.count() > 0 else 0
        rating_breakdown[i] = {
            'count': count,
            'percentage': percentage
        }
    
    # Check if user has purchased this product (for verified purchase badge)
    has_purchased = False
    if request.user.is_authenticated:
        has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__status='completed'
        ).exists()
    
    # Check if user already reviewed
    user_review = None
    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(product=product, user=request.user)
        except Review.DoesNotExist:
            pass
    
    context = {
        'product': product,
        'product_images': product_images,
        'specifications': specifications,
        'variants': variants,
        'reviews': reviews,
        'rating_breakdown': rating_breakdown,
        'related_products': related_products,
        'has_purchased': has_purchased,
        'user_review': user_review,
    }
    
    return render(request, 'products/product_detail.html', context)


@login_required
@require_POST
def add_to_cart(request):
    """
    Add product to cart via AJAX
    """
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        variant_id = data.get('variant_id')
        quantity = int(data.get('quantity', 1))
        
        # Get product
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Get or create cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Get variant if provided
        variant = None
        if variant_id:
            variant = get_object_or_404(ProductVariant, id=variant_id, product=product)
            
            # Check variant stock
            if variant.stock < quantity:
                return JsonResponse({
                    'success': False,
                    'message': 'Insufficient stock for selected variant'
                })
        else:
            # Check product stock
            if product.stock < quantity:
                return JsonResponse({
                    'success': False,
                    'message': 'Insufficient stock'
                })
        
        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update quantity if item already exists
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart',
            'cart_total': cart.total_items
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@login_required
@require_POST
def add_to_wishlist(request):
    """
    Add product to wishlist via AJAX
    """
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        product = get_object_or_404(Product, id=product_id)
        
        # Check if already in wishlist
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if created:
            return JsonResponse({
                'success': True,
                'message': 'Product added to wishlist'
            })
        else:
            # Remove from wishlist if already exists
            wishlist_item.delete()
            return JsonResponse({
                'success': True,
                'message': 'Product removed from wishlist'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404


@login_required
@require_POST
def toggle_wishlist(request, product_id):
    """Toggle product in user's wishlist"""
    product = get_object_or_404(Product, id=product_id)
    
    wishlist_item = Wishlist.objects.filter(
        user=request.user,
        product=product
    ).first()
    
    if wishlist_item:
        wishlist_item.delete()
        action = 'removed'
        message = f'{product.name} removed from wishlist'
    else:
        Wishlist.objects.create(
            user=request.user,
            product=product
        )
        action = 'added'
        message = f'{product.name} added to wishlist'
    
    return JsonResponse({
        'success': True,
        'action': action,
        'message': message
    })

@login_required
@require_POST
def submit_review(request, product_id):
    """
    Submit a product review
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Check if user already reviewed
    if Review.objects.filter(product=product, user=request.user).exists():
        messages.error(request, 'You have already reviewed this product.')
        return redirect('product_detail', slug=product.slug)
    
    # Get form data
    rating = request.POST.get('rating')
    title = request.POST.get('title')
    comment = request.POST.get('comment')
    images = request.FILES.getlist('images')
    
    # Check if user purchased the product
    is_verified_purchase = OrderItem.objects.filter(
        order__user=request.user,
        product=product,
        order__status='completed'
    ).exists()
    
    # Create review
    review = Review.objects.create(
        product=product,
        user=request.user,
        rating=rating,
        title=title,
        comment=comment,
        is_verified_purchase=is_verified_purchase,
        is_approved=True  # Auto-approve or set to False for moderation
    )
    
    # Add review images
    for image in images:
        ReviewImage.objects.create(
            review=review,
            image=image
        )
    
    messages.success(request, 'Thank you for your review!')
    return redirect('product_detail', slug=product.slug)


@login_required
@require_POST
def mark_review_helpful(request, review_id):
    """
    Mark a review as helpful
    """
    try:
        review = get_object_or_404(Review, id=review_id)
        review.helpful_count += 1
        review.save()
        
        return JsonResponse({
            'success': True,
            'helpful_count': review.helpful_count
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


def category_products(request, slug):
    """
    Display products by category
    """
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    # Get products in this category and subcategories
    categories = [category]
    if category.subcategories.exists():
        categories.extend(category.subcategories.filter(is_active=True))
    
    products = Product.objects.filter(
        category__in=categories,
        is_active=True
    ).order_by('-created_at')
    
    # Filters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    brand_id = request.GET.get('brand')
    sort_by = request.GET.get('sort', '-created_at')
    
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if brand_id:
        products = products.filter(brand_id=brand_id)
    
    # Sorting
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'popular':
        products = products.order_by('-sold_count')
    elif sort_by == 'rating':
        products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    
    # Get brands for filter
    brands = Brand.objects.filter(
        products__category__in=categories,
        is_active=True
    ).distinct()
    
    context = {
        'category': category,
        'products': products,
        'brands': brands,
        'subcategories': category.subcategories.filter(is_active=True),
    }
    
    return render(request, 'products/category.html', context)


def brand_products(request, slug):
    """
    Display products by brand
    """
    brand = get_object_or_404(Brand, slug=slug, is_active=True)
    
    products = Product.objects.filter(
        brand=brand,
        is_active=True
    ).order_by('-created_at')
    
    context = {
        'brand': brand,
        'products': products,
    }
    
    return render(request, 'products/brand.html', context)


def search_products(request):
    """
    Search products
    """
    query = request.GET.get('q', '')
    
    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__name__icontains=query)
        ).distinct()
    
    context = {
        'products': products,
        'query': query,
    }
    
    return render(request, 'products/search.html', context)


@login_required
def wishlist_view(request):
    """
    Display user's wishlist
    """
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    
    context = {
        'wishlist_items': wishlist_items,
    }
    
    return render(request, 'products/wishlist.html', context)


@login_required
def cart_view(request):
    """
    Display shopping cart
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all().select_related('product', 'variant')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    
    return render(request, 'store/cart.html', context)


@login_required
@require_POST
def update_cart_item(request, item_id):
    """
    Update cart item quantity
    """
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        
        if quantity <= 0:
            cart_item.delete()
            return JsonResponse({
                'success': True,
                'message': 'Item removed from cart'
            })
        
        # Check stock
        if cart_item.variant:
            if cart_item.variant.stock < quantity:
                return JsonResponse({
                    'success': False,
                    'message': 'Insufficient stock'
                })
        else:
            if cart_item.product.stock < quantity:
                return JsonResponse({
                    'success': False,
                    'message': 'Insufficient stock'
                })
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            'success': True,
            'subtotal': float(cart_item.subtotal),
            'cart_total': float(cart_item.cart.total_amount)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@login_required
@require_POST
def remove_cart_item(request, item_id):
    """
    Remove item from cart
    """
    try:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from .models import Product, Category, Brand, Wishlist
from decimal import Decimal


def product_list(request):
    """Amazon-style product listing with filters and search"""
    
    # Get all active products
    products = Product.objects.filter(is_active=True).select_related('category', 'brand')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(brand__name__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category', '')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(
            Q(category=selected_category) | 
            Q(category__parent=selected_category)
        )
    
    # Brand filter
    brand_id = request.GET.get('brand', '')
    selected_brand = None
    if brand_id:
        selected_brand = get_object_or_404(Brand, id=brand_id)
        products = products.filter(brand=selected_brand)
    
    # Price range filter
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    if min_price:
        try:
            products = products.filter(price__gte=Decimal(min_price))
        except:
            pass
    
    if max_price:
        try:
            products = products.filter(price__lte=Decimal(max_price))
        except:
            pass
    
    # Rating filter
    min_rating = request.GET.get('rating', '')
    if min_rating:
        try:
            min_rating = int(min_rating)
            # This is a simplified version - for better performance, 
            # consider adding a cached average_rating field to Product model
            products = [p for p in products if p.average_rating >= min_rating]
        except:
            pass
    
    # Special filters
    if request.GET.get('featured') == '1':
        products = products.filter(is_featured=True)
    
    if request.GET.get('bestseller') == '1':
        products = products.filter(is_bestseller=True)
    
    if request.GET.get('new_arrival') == '1':
        products = products.filter(is_new_arrival=True)
    
    if request.GET.get('free_shipping') == '1':
        products = products.filter(free_shipping=True)
    
    if request.GET.get('in_stock') == '1':
        products = products.filter(stock__gt=0)
    
    # Sorting
    sort_by = request.GET.get('sort', 'featured')
    
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == 'rating':
        products = products.order_by('-sold_count')  # Using sold_count as proxy
    else:  # featured (default)
        products = products.order_by('-is_featured', '-sold_count', '-view_count')
    
    # Get all categories and brands for filters
    categories = Category.objects.filter(
        is_active=True, 
        parent=None
    ).prefetch_related('subcategories')
    
    brands = Brand.objects.filter(is_active=True).order_by('name')
    
    # Get price range for filter
    if products:
        if isinstance(products, list):
            price_min = min(p.price for p in products)
            price_max = max(p.price for p in products)
        else:
            price_range = products.aggregate(
                min_price=models.Min('price'),
                max_price=models.Max('price')
            )
            price_min = price_range['min_price'] or 0
            price_max = price_range['max_price'] or 10000
    else:
        price_min = 0
        price_max = 10000
    
    # Get user's wishlist if authenticated
    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = Wishlist.objects.filter(
            user=request.user
        ).values_list('product_id', flat=True)
    
    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(products, 24)  # 24 products per page
    page_obj = paginator.get_page(page_number)
    
    # Calculate result count
    total_results = paginator.count
    
    context = {
        'products': page_obj,
        'categories': categories,
        'brands': brands,
        'selected_category': selected_category,
        'selected_brand': selected_brand,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_results': total_results,
        'price_min': int(price_min),
        'price_max': int(price_max),
        'current_min_price': min_price or '',
        'current_max_price': max_price or '',
        'wishlist_ids': list(wishlist_ids),
        'page_obj': page_obj,
    }
    
    return render(request, 'products/product_list.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.core.paginator import Paginator

def category_view(request, category_id):
    """Display products belonging to a specific category."""
    category = get_object_or_404(Category, id=category_id)
    products = category.products.filter(is_active=True).order_by('-created_at')

    # Optional pagination (6 products per page)
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
        'products': page_obj.object_list,  # for convenience
    }
    return render(request, 'store/category.html', context)




@login_required
@require_POST
def update_cart(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, 'Item removed from cart')
    else:
        if cart_item.product.stock >= quantity:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated')
        else:
            messages.error(request, 'Insufficient stock')
    
    return redirect('cart_view')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart')
    return redirect('cart_view')


# Checkout Views
@login_required
def checkout(request):
    """Checkout page with M-Pesa Paybill integration"""
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty')
        return redirect('cart')
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', '').strip()
        account_number = request.POST.get('account_number', '').strip()
        delivery_address = request.POST.get('delivery_address', '').strip()
        
        # Validate phone number format (Kenyan format)
        if not phone_number.startswith('254'):
            return JsonResponse({
                'success': False,
                'error': 'Phone number must start with 254 (e.g., 254712345678)'
            })
        
        if len(phone_number) != 12:
            return JsonResponse({
                'success': False,
                'error': 'Invalid phone number format. Use 254XXXXXXXXX'
            })
        
        if not account_number:
            return JsonResponse({
                'success': False,
                'error': 'Account number is required'
            })
        
        try:
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    total_amount=cart.total_amount,
                    phone_number=phone_number,
                    delivery_address=delivery_address,
                    status='pending'
                )
                
                # Create order items
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )
                    
                    # Reduce stock
                    product = cart_item.product
                    product.stock -= cart_item.quantity
                    product.save()
                
                # Clear cart
                cart.items.all().delete()
                
                # Create M-Pesa payment record
                payment = MpesaPayment.objects.create(
                    order=order,
                    phone_number=phone_number,
                    amount=order.total_amount,
                    business_number=settings.MPESA_SHORTCODE,
                    account_number=account_number,
                    status='pending'
                )
                
                # Initiate STK Push
                result = initiate_stk_push(payment)
                
                if result and result.get('ResponseCode') == '0':
                    payment.merchant_request_id = result.get('MerchantRequestID')
                    payment.checkout_request_id = result.get('CheckoutRequestID')
                    payment.save()
                    
                    logger.info(f"STK Push initiated for order {order.id}")
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'Payment request sent! Check your phone to complete payment.',
                        'order_id': order.id,
                        'checkout_request_id': payment.checkout_request_id
                    })
                else:
                    error_msg = result.get('errorMessage', 'Failed to initiate payment') if result else 'Connection error'
                    logger.error(f"STK Push failed: {error_msg}")
                    
                    # Rollback stock
                    for item in order.items.all():
                        product = item.product
                        product.stock += item.quantity
                        product.save()
                    
                    order.status = 'cancelled'
                    order.save()
                    payment.status = 'failed'
                    payment.result_description = error_msg
                    payment.save()
                    
                    return JsonResponse({
                        'success': False,
                        'error': f"Payment failed: {error_msg}"
                    })
                    
        except Exception as e:
            logger.error(f"Checkout error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': f'Error processing order: {str(e)}'
            })
    
    context = {
        'cart': cart,
        'paybill_number': settings.MPESA_SHORTCODE
    }
    return render(request, 'store/checkout.html', context)



def initiate_stk_push(payment):
    """
    Initiate M-Pesa STK Push for Paybill
    """
    try:
        # Get access token
        access_token = get_mpesa_access_token()
        if not access_token:
            logger.error("Failed to get access token")
            return {'errorMessage': 'Failed to authenticate with M-Pesa'}
        
        # Generate password and timestamp
        password, timestamp = generate_password()
        
        # Determine API URL
        if settings.MPESA_ENVIRONMENT == 'sandbox':
            url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        else:
            url = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        
        # Set headers
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Prepare payload
        payload = {
            'BusinessShortCode': settings.MPESA_SHORTCODE,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': int(payment.amount),
            'PartyA': payment.phone_number,
            'PartyB': settings.MPESA_SHORTCODE,
            'PhoneNumber': payment.phone_number,
            'CallBackURL': settings.MPESA_CALLBACK_URL,
            'AccountReference': payment.account_number,
            'TransactionDesc': f'Order #{payment.order.id}'
        }
        
        logger.info(f"Initiating STK Push for order {payment.order.id}")
        logger.info(f"Phone: {payment.phone_number}, Amount: {payment.amount}")
        
        # Make the request
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        
        # Log response
        logger.info(f"STK Push response status: {response.status_code}")
        logger.info(f"STK Push response: {response.text}")
        
        # Parse response
        result = response.json()
        
        if response.status_code == 200:
            return result
        else:
            error_msg = result.get('errorMessage', 'Unknown error')
            logger.error(f"STK Push failed: {error_msg}")
            return result
            
    except requests.exceptions.Timeout:
        logger.error("STK Push request timed out")
        return {'errorMessage': 'Request timed out. Please try again.'}
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during STK Push: {str(e)}")
        return {'errorMessage': f'Network error: {str(e)}'}
    except Exception as e:
        logger.error(f"STK Push error: {str(e)}")
        return {'errorMessage': f'Error: {str(e)}'}


def verify_credentials():
    """
    Test function to verify M-Pesa credentials
    Call this from Django shell to test your setup
    """
    print("Testing M-Pesa Credentials...")
    print(f"Environment: {settings.MPESA_ENVIRONMENT}")
    print(f"Consumer Key: {settings.MPESA_CONSUMER_KEY[:10]}...")
    print(f"Shortcode: {settings.MPESA_SHORTCODE}")
    
    token = get_mpesa_access_token()
    
    if token:
        print("✓ Credentials are valid!")
        print(f"Access Token (first 20 chars): {token[:20]}...")
        return True
    else:
        print("✗ Failed to get access token. Check your credentials.")
        return False



@csrf_exempt
@require_POST
def mpesa_callback(request):
    """Handle M-Pesa callback for payment confirmation"""
    try:
        data = json.loads(request.body)
        logger.info(f"M-Pesa Callback received: {json.dumps(data, indent=2)}")
        
        stk_callback = data.get('Body', {}).get('stkCallback', {})
        checkout_request_id = stk_callback.get('CheckoutRequestID')
        result_code = stk_callback.get('ResultCode')
        result_desc = stk_callback.get('ResultDesc')
        
        if not checkout_request_id:
            logger.error("No CheckoutRequestID in callback")
            return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Invalid callback data'})
        
        try:
            payment = MpesaPayment.objects.get(checkout_request_id=checkout_request_id)
            payment.result_code = str(result_code)
            payment.result_description = result_desc
            
            if result_code == 0:
                # Payment successful
                callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
                
                for item in callback_metadata:
                    name = item.get('Name')
                    value = item.get('Value')
                    
                    if name == 'MpesaReceiptNumber':
                        payment.mpesa_receipt_number = value
                    elif name == 'TransactionDate':
                        transaction_date = str(value)
                        payment.transaction_date = datetime.strptime(
                            transaction_date, '%Y%m%d%H%M%S'
                        )
                    elif name == 'Amount':
                        # Verify amount matches
                        if float(value) != float(payment.amount):
                            logger.warning(
                                f"Amount mismatch for order {payment.order.id}: "
                                f"Expected {payment.amount}, got {value}"
                            )
                
                payment.status = 'completed'
                payment.order.status = 'processing'
                payment.order.save()
                
                logger.info(
                    f"Payment completed for order {payment.order.id}. "
                    f"Receipt: {payment.mpesa_receipt_number}"
                )
            else:
                # Payment failed or cancelled
                payment.status = 'failed'
                payment.order.status = 'cancelled'
                payment.order.save()
                
                # Restore stock
                for item in payment.order.items.all():
                    product = item.product
                    product.stock += item.quantity
                    product.save()
                
                logger.warning(
                    f"Payment failed for order {payment.order.id}. "
                    f"Result: {result_desc}"
                )
            
            payment.save()
            
        except MpesaPayment.DoesNotExist:
            logger.error(f"Payment not found for CheckoutRequestID: {checkout_request_id}")
            return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Payment not found'})
        
        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
        
    except Exception as e:
        logger.error(f"Callback processing error: {str(e)}")
        return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Processing error'})


@login_required
@require_http_methods(["GET"])
def check_payment_status(request, order_id):
    """Check M-Pesa payment status via AJAX"""
    try:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        try:
            payment = order.mpesa_payment
            
            return JsonResponse({
                'success': True,
                'status': payment.status,
                'order_status': order.status,
                'result_description': payment.result_description,
                'mpesa_receipt': payment.mpesa_receipt_number,
                'transaction_date': payment.transaction_date.strftime('%Y-%m-%d %H:%M:%S') if payment.transaction_date else None
            })
        except MpesaPayment.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Payment record not found'
            })
            
    except Exception as e:
        logger.error(f"Error checking payment status: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def order_detail(request, order_id):
    """Display order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    try:
        payment = order.mpesa_payment
    except MpesaPayment.DoesNotExist:
        payment = None
    
    context = {
        'order': order,
        'payment': payment
    }
    return render(request, 'store/order_detail.html', context)


@login_required
def order_list(request):
    """Display user's orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_list.html', {'orders': orders})