"""
Django admin configuration for ShopNest.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    User, Address, Shop, Product, ShoppingList, ShoppingListItem, Order, OrderItem,
    Notification, Review, Preference,DeliveryAgent
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_active')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_type', 'address', 'is_primary')
    list_filter = ('address_type', 'is_primary')
    search_fields = ('user__username', 'address')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop_type', 'rating_display', 'is_open', 'delivery_time', 'created_at')
    list_filter = ('shop_type', 'is_open', 'created_at')
    search_fields = ('name', 'address')
    readonly_fields = ('created_at', 'updated_at')
    
    def rating_display(self, obj):
        color = 'green' if obj.rating >= 4 else 'orange' if obj.rating >= 3 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">★ {}</span>',
            color,
            obj.rating
        )
    rating_display.short_description = 'Rating'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'category', 'price', 'stock', 'is_available')
    list_filter = ('is_available', 'category', 'shop', 'created_at')
    search_fields = ('name', 'sku')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'total_estimated_bill', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ShoppingListItem)
class ShoppingListItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'shopping_list', 'quantity', 'unit', 'is_checked')
    list_filter = ('is_checked', 'created_at')
    search_fields = ('name', 'shopping_list__name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status_display', 'payment_status', 'final_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('id', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    
    def status_display(self, obj):
        colors = {
            'pending': 'orange',
            'confirmed': 'blue',
            'preparing': 'purple',
            'out_for_delivery': 'cyan',
            'delivered': 'green',
            'cancelled': 'red',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: white; background-color: {}; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'price', 'total')
    list_filter = ('order__created_at',)
    search_fields = ('product__name', 'order__id')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'user__username')
    readonly_fields = ('created_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'rating_display', 'review_type', 'created_at')
    list_filter = ('rating', 'review_type', 'created_at')
    search_fields = ('title', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    
    def rating_display(self, obj):
        return format_html('<span style="font-weight: bold;">★ {}</span>', obj.rating)
    rating_display.short_description = 'Rating'


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'notifications_enabled', 'language', 'theme')
    list_filter = ('notifications_enabled', 'language', 'theme')
    search_fields = ('user__username',)


@admin.register(DeliveryAgent)
class DeliveryAgentAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle_type', 'vehicle_number', 'status_display', 'total_deliveries', 'rating_display', 'is_active')
    list_filter = ('status', 'is_active', 'vehicle_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'vehicle_number')
    readonly_fields = ('created_at', 'updated_at')
    
    def status_display(self, obj):
        colors = {
            'available': 'green',
            'busy': 'orange',
            'offline': 'gray',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: white; background-color: {}; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def rating_display(self, obj):
        color = 'green' if obj.rating >= 4 else 'orange' if obj.rating >= 3 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">★ {}</span>',
            color,
            obj.rating
        )
    rating_display.short_description = 'Rating'
