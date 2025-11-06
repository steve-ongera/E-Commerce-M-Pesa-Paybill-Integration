from .models import Category, Cart

def cart_processor(request):
    """Add cart information to all templates"""
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.total_items
        except Cart.DoesNotExist:
            cart_count = 0
    
    return {
        'cart_count': cart_count
    }

def categories_processor(request):
    """Add all categories to all templates"""
    categories = Category.objects.all()
    return {
        'all_categories': categories
    }