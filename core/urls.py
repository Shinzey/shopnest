"""
URL configuration for core app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/shop-owner/', views.register_shop_owner, name='register_shop_owner'),
    path('register/delivery-agent/', views.register_delivery_agent, name='register_delivery_agent'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Home & Dashboard
    path('home', views.home, name='home'),
    path('', views.landing_page, name='landing'),

    # Shops
    path('shops/', views.shops_list, name='shops_list'),
    path('shops/<int:shop_id>/', views.shop_detail, name='shop_detail'),
    path('shops/<int:shop_id>/review/', views.add_shop_review, name='add_shop_review'),
    
    # Products
    path('products/', views.products_list, name='products_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/review/', views.add_product_review, name='add_product_review'),
    
    # Shopping Lists
    path('lists/', views.shopping_lists, name='shopping_lists'),
    path('lists/create/', views.create_shopping_list, name='create_shopping_list'),
    path('lists/<int:list_id>/', views.shopping_list_detail, name='shopping_list_detail'),
    path('lists/<int:list_id>/add-item/', views.add_shopping_list_item, name='add_shopping_list_item'),
    path('lists/<int:list_id>/delete/', views.delete_shopping_list, name='delete_shopping_list'),
    
    # Cart & Checkout
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/create/', views.create_order, name='create_order'),
    
    # Orders
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    
    # Notifications
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/address/add/', views.add_address, name='add_address'),
    path('profile/address/<int:address_id>/delete/', views.delete_address, name='delete_address'),
    
    # Shop Owner
    path('shop/edit/', views.edit_shop, name='edit_shop'),
    path('orders/<int:order_id>/accept/', views.shop_owner_accept_order, name='shop_owner_accept_order'),
    path('orders/<int:order_id>/complete/', views.shop_owner_complete_order, name='shop_owner_complete_order'),
    path('orders/<int:order_id>/assign-delivery/', views.assign_delivery_agent, name='assign_delivery_agent'),
    
    # Delivery Agent
    path('delivery/<int:order_id>/accept/', views.delivery_agent_accept_order, name='delivery_agent_accept_order'),
    path('delivery/<int:order_id>/deliver/', views.delivery_agent_deliver_order, name='delivery_agent_deliver_order'),
    
    # Product Management (Shop Owner)
    path('products/shop/', views.shop_owner_products, name='shop_owner_products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
]
