from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from .models import (
    Category, Brand, Product, ProductImage, ProductSpecification,
    ProductVariant, Review, ReviewImage, Wishlist, Order, OrderItem,
    OrderStatusHistory, MpesaPayment, Cart, CartItem, Coupon, Address
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active', 'display_order', 'created_at']
    list_filter = ['is_active', 'created_at', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'display_order']
    ordering = ['display_order', 'name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'display_order']


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1
    fields = ['name', 'value', 'display_order']


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = ['name', 'sku', 'price_adjustment', 'stock', 'is_active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'brand', 'price', 'stock', 
        'stock_status', 'is_featured', 'is_active', 'view_count', 'sold_count'
    ]
    list_filter = [
        'is_active', 'is_featured', 'is_bestseller', 'is_new_arrival',
        'category', 'brand', 'created_at'
    ]
    search_fields = ['name', 'description', 'sku']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'is_featured', 'price']
    readonly_fields = ['view_count', 'sold_count', 'created_at', 'updated_at']
    inlines = [ProductImageInline, ProductSpecificationInline, ProductVariantInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'brand', 'description', 'image')
        }),
        ('Pricing', {
            'fields': ('price', 'compare_at_price', 'cost_price')
        }),
        ('Inventory', {
            'fields': ('stock', 'sku', 'low_stock_threshold')
        }),
        ('Product Details', {
            'fields': ('weight', 'dimensions')
        }),
        ('Features', {
            'fields': ('is_active', 'is_featured', 'is_bestseller', 'is_new_arrival')
        }),
        ('Shipping & Returns', {
            'fields': ('free_shipping', 'shipping_days', 'warranty_period', 'return_policy_days')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('view_count', 'sold_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def stock_status(self, obj):
        if obj.stock == 0:
            color = 'red'
            status = 'Out of Stock'
        elif obj.is_low_stock:
            color = 'orange'
            status = 'Low Stock'
        else:
            color = 'green'
            status = 'In Stock'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, status
        )
    stock_status.short_description = 'Stock Status'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'alt_text', 'display_order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__name', 'alt_text']


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'value', 'display_order']
    list_filter = ['name']
    search_fields = ['product__name', 'name', 'value']


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'sku', 'price_adjustment', 'stock', 'is_active']
    list_filter = ['is_active']
    search_fields = ['product__name', 'name', 'sku']
    list_editable = ['is_active', 'stock']


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'user', 'rating', 'is_verified_purchase',
        'is_approved', 'helpful_count', 'created_at'
    ]
    list_filter = ['rating', 'is_verified_purchase', 'is_approved', 'created_at']
    search_fields = ['product__name', 'user__username', 'title', 'comment']
    list_editable = ['is_approved']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ReviewImageInline]


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ['review', 'image', 'created_at']
    list_filter = ['created_at']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__name']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'variant', 'quantity', 'price', 'subtotal']
    can_delete = False


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ['status', 'notes', 'created_by', 'created_at']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'user', 'total_amount', 'status',
        'payment_status', 'created_at'
    ]
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = [
        'order_number', 'user__username', 'user__email',
        'phone_number', 'tracking_number'
    ]
    readonly_fields = [
        'order_number', 'user', 'subtotal', 'shipping_cost',
        'tax', 'discount', 'total_amount', 'created_at', 'updated_at'
    ]
    list_editable = ['status']
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_status')
        }),
        ('Amounts', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'discount', 'total_amount')
        }),
        ('Delivery Information', {
            'fields': ('phone_number', 'delivery_address', 'city', 'postal_code')
        }),
        ('Tracking', {
            'fields': ('tracking_number', 'estimated_delivery_date', 'delivered_at')
        }),
        ('Notes', {
            'fields': ('customer_notes', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            # Create status history entry
            OrderStatusHistory.objects.create(
                order=obj,
                status=obj.status,
                created_by=request.user
            )
        super().save_model(request, obj, form, change)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'variant', 'quantity', 'price', 'get_subtotal']
    list_filter = ['order__created_at']
    search_fields = ['order__order_number', 'product__name', 'product_sku']
    readonly_fields = ['order', 'product', 'variant', 'quantity', 'price']
    
    def get_subtotal(self, obj):
        return obj.subtotal
    get_subtotal.short_description = 'Subtotal'


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order__order_number', 'notes']
    readonly_fields = ['order', 'status', 'created_by', 'created_at']


@admin.register(MpesaPayment)
class MpesaPaymentAdmin(admin.ModelAdmin):
    list_display = [
        'order', 'phone_number', 'amount', 'status',
        'mpesa_receipt_number', 'transaction_date'
    ]
    list_filter = ['status', 'created_at', 'transaction_date']
    search_fields = [
        'order__order_number', 'phone_number', 'mpesa_receipt_number',
        'merchant_request_id', 'checkout_request_id'
    ]
    readonly_fields = [
        'order', 'phone_number', 'amount', 'merchant_request_id',
        'checkout_request_id', 'mpesa_receipt_number', 'transaction_date',
        'result_code', 'result_description', 'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order', 'phone_number', 'amount', 'status')
        }),
        ('Paybill Details', {
            'fields': ('business_number', 'account_number')
        }),
        ('M-Pesa Response', {
            'fields': (
                'merchant_request_id', 'checkout_request_id',
                'mpesa_receipt_number', 'transaction_date',
                'result_code', 'result_description'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'variant', 'quantity', 'get_subtotal']
    
    def get_subtotal(self, obj):
        return obj.subtotal
    get_subtotal.short_description = 'Subtotal'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_total_items', 'get_total_amount', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['user', 'created_at', 'updated_at']
    inlines = [CartItemInline]
    
    def get_total_items(self, obj):
        return obj.total_items
    get_total_items.short_description = 'Total Items'
    
    def get_total_amount(self, obj):
        return f"KES {obj.total_amount}"
    get_total_amount.short_description = 'Total Amount'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'variant', 'quantity', 'get_subtotal']
    search_fields = ['cart__user__username', 'product__name']
    readonly_fields = ['cart', 'product', 'variant']
    
    def get_subtotal(self, obj):
        return obj.subtotal
    get_subtotal.short_description = 'Subtotal'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'discount_type', 'discount_value', 'usage_limit',
        'used_count', 'is_active', 'valid_from', 'valid_to'
    ]
    list_filter = ['discount_type', 'is_active', 'created_at']
    search_fields = ['code']
    list_editable = ['is_active']
    readonly_fields = ['used_count', 'created_at']
    
    fieldsets = (
        ('Coupon Details', {
            'fields': ('code', 'discount_type', 'discount_value', 'is_active')
        }),
        ('Restrictions', {
            'fields': ('min_purchase', 'max_discount', 'usage_limit', 'used_count')
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_to')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'address_type', 'full_name', 'phone_number',
        'city', 'is_default', 'created_at'
    ]
    list_filter = ['address_type', 'is_default', 'city', 'created_at']
    search_fields = ['user__username', 'full_name', 'phone_number', 'city']
    list_editable = ['is_default']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'address_type', 'is_default')
        }),
        ('Contact Details', {
            'fields': ('full_name', 'phone_number')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'postal_code')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

admin.site.site_header = "Paybill E-commerce Admin"
admin.site.site_title = "Paybill E-commerce Admin Portal"
admin.site.index_title = "Welcome to Paybill E-commerce Admin Portal"
