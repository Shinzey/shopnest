"""
Django models for ShopNest application.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta


def get_notification_expiry():
    """Get notification expiry time (30 days from now)."""
    return timezone.now() + timedelta(days=30)


class User(AbstractUser):
    """Extended User model with additional ShopNest fields."""
    USER_ROLES = [
        ('customer', 'Regular Customer'),
        ('shop_owner', 'Shop Owner'),
        ('delivery_agent', 'Delivery Agent'),
    ]
    
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='customer')
    pincode = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=100, blank=True)
    village = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    def is_customer(self):
        return self.role == 'customer'
    
    def is_shop_owner(self):
        return self.role == 'shop_owner'
    
    def is_delivery_agent(self):
        return self.role == 'delivery_agent'


class Address(models.Model):
    """User addresses."""
    ADDRESS_TYPES = [
        ('home', 'Home'),
        ('office', 'Office'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.address_type.title()} - {self.address[:50]}"


class Shop(models.Model):
    """Shop/Store model."""
    SHOP_TYPES = [
        ('supermarket', 'Supermarket'),
        ('stationary', 'Stationary'),
        ('quickcommerce', 'Quick Commerce'),
        ('grocery', 'Grocery'),
    ]
    
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop', limit_choices_to={'role': 'shop_owner'}, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    shop_type = models.CharField(max_length=50, choices=SHOP_TYPES, blank=True)
    logo = models.ImageField(upload_to='shop_logos/', blank=True, null=True)
    address = models.TextField(blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=100, blank=True)
    village = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    is_open = models.BooleanField(default=True)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    review_count = models.IntegerField(default=0)
    delivery_time = models.IntegerField(help_text="Delivery time in minutes", blank=True, null=True)
    min_order = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    categories = models.JSONField(default=list, help_text="Categories available in shop")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'
        ordering = ['-rating']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model."""
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.IntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.shop.name}"


class ShoppingList(models.Model):
    """Shopping list model."""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted to Shop'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shopping_lists', limit_choices_to={'role': 'customer'})
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shopping_lists', null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='shopping_lists/', null=True, blank=True, help_text="Upload image of wanted items")
    total_estimated_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Shopping List'
        verbose_name_plural = 'Shopping Lists'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.user.get_full_name()}"


class DeliveryAgent(models.Model):
    """Delivery Agent model."""
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('offline', 'Offline'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='delivery_agent', limit_choices_to={'role': 'delivery_agent'})
    vehicle_type = models.CharField(max_length=50, default='bike', choices=[('bike', 'Bike'), ('car', 'Car'), ('scooter', 'Scooter')])
    vehicle_number = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline')
    current_orders = models.IntegerField(default=0)
    total_deliveries = models.IntegerField(default=0)
    rating = models.FloatField(default=5.0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Delivery Agent'
        verbose_name_plural = 'Delivery Agents'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_status_display()}"


class ShoppingListItem(models.Model):
    """Items in a shopping list."""
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit = models.CharField(max_length=50, default='piece')
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Shopping List Item'
        verbose_name_plural = 'Shopping List Items'

    def __str__(self):
        return f"{self.name} x {self.quantity} {self.unit}"


class Order(models.Model):
    """Order model."""
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', limit_choices_to={'role': 'customer'})
    shops = models.ManyToManyField(Shop)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    delivery_agent = models.ForeignKey('DeliveryAgent', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=50, default='cod')
    estimated_delivery = models.DateTimeField()
    actual_delivery = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.get_full_name()}"


class OrderItem(models.Model):
    """Items in an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Notification(models.Model):
    """Notification model."""
    NOTIFICATION_TYPES = [
        ('order_update', 'Order Update'),
        ('deal', 'Deal Alert'),
        ('price_drop', 'Price Drop'),
        ('reminder', 'Reminder'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    related_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
    related_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_notification_expiry)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.get_full_name()}"


class Review(models.Model):
    """Review model for shops and products."""
    REVIEW_TYPES = [
        ('shop', 'Shop'),
        ('product', 'Product'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    review_type = models.CharField(max_length=20, choices=REVIEW_TYPES)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=255)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.get_full_name()}"


class Preference(models.Model):
    """User preferences."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    notifications_enabled = models.BooleanField(default=True)
    language = models.CharField(max_length=10, default='en')
    theme = models.CharField(max_length=10, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
    do_not_disturb_start = models.TimeField(null=True, blank=True)
    do_not_disturb_end = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Preference'
        verbose_name_plural = 'Preferences'

    def __str__(self):
        return f"Preferences for {self.user.get_full_name()}"
