"""
Views for ShopNest application.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import timedelta
import math

from .models import (
    User, Shop, Product, ShoppingList, ShoppingListItem, Order, OrderItem,
    Notification, Review, Address, Preference, DeliveryAgent
)
from .forms import (
    UserRegistrationForm, UserLoginForm, ShoppingListForm, ShoppingListItemForm,
    OrderForm, ReviewForm, AddressForm, ProfileForm,
    CustomerRegistrationForm, ShopOwnerRegistrationForm, DeliveryAgentRegistrationForm
)


# ==================== Authentication Views ====================

def register(request):
    """User registration role selection."""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'auth/register_role.html')


def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            Preference.objects.create(user=user)

            if user.role == 'delivery_agent':
                DeliveryAgent.objects.create(
                    user=user,
                    vehicle_type='bike',
                    status='offline'
                )

            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')

    else:
        form = CustomerRegistrationForm()

    return render(
        request,
        'auth/register.html',
        {
            'form': form,
            'role': 'Customer'
        }
    )


def register_shop_owner(request):
    """Shop owner registration."""
    if request.method == 'POST':
        form = ShopOwnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Preference.objects.create(user=user)
            messages.success(request, 'Shop owner registration successful! Please log in.')
            return redirect('login')
    else:
        form = ShopOwnerRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form, 'role': 'Shop Owner'})


def register_delivery_agent(request):
    if request.method == 'POST':
        form = DeliveryAgentRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            Preference.objects.create(user=user)

            DeliveryAgent.objects.create(
                user=user,
                vehicle_type=form.cleaned_data['vehicle_type'],
                vehicle_number=form.cleaned_data['vehicle_number'],
                status='offline'
            )

            messages.success(
                request,
                'Delivery agent registration successful! Please log in.'
            )

            return redirect('login')

    else:
        form = DeliveryAgentRegistrationForm()

    return render(
        request,
        'auth/delivery_register.html',
        {'form': form, 'role': 'Delivery Agent'}
    )


def login_view(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """User logout."""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


# ==================== Home & Dashboard ====================
def landing_page(request):
    return render(request, 'landing/landing.html')

@login_required
def home(request):
    """Home page - role-based dashboard."""
    # Shop owner dashboard
    if request.user.is_shop_owner():
        try:
            shop = request.user.shop
            active_orders = Order.objects.filter(shops=shop, status__in=['pending', 'confirmed']).order_by('-created_at')
            completed_orders = Order.objects.filter(shops=shop, status__in=['delivered', 'completed']).order_by('-created_at')
            products = shop.products.all()
            context = {
                'shop': shop,
                'active_orders': active_orders[:10],
                'completed_orders': completed_orders[:10],
                'products': products,
                'is_shop_owner': True,
            }
            return render(request, 'dashboard/shop_owner_dashboard.html', context)
        except Shop.DoesNotExist:
            messages.warning(request, 'Please create or complete your shop profile.')
            return redirect('edit_shop')
    
    # Delivery agent dashboard
    if request.user.is_delivery_agent():
        from .models import DeliveryAgent
        try:
            delivery_agent = request.user.delivery_agent
            assigned_orders = Order.objects.filter(delivery_agent=delivery_agent, status__in=['confirmed', 'out_for_delivery']).order_by('-created_at')
            completed_orders = Order.objects.filter(delivery_agent=delivery_agent, status='delivered').order_by('-created_at')
            
            context = {
                'delivery_agent': delivery_agent,
                'assigned_orders': assigned_orders,
                'completed_orders': completed_orders,
                'is_delivery_agent': True,
            }
            return render(request, 'dashboard/delivery_agent_dashboard.html', context)
        except:
            messages.error(request, 'Delivery agent profile not found.')
            return redirect('profile')
    
    # Customer home page with nearby shops
    shops = Shop.objects.all()
    
    # Filter by pincode if customer has one
    if request.user.pincode:
        shops = shops.filter(pincode=request.user.pincode)
    
    featured_products = Product.objects.filter(is_available=True)[:8]
    recent_orders = request.user.orders.all()[:5]
    
    context = {
        'shops': shops[:6],
        'featured_products': featured_products,
        'recent_orders': recent_orders,
        'user_pincode': request.user.pincode,
    }
    return render(request, 'home/index.html', context)


# ==================== Shop Views ====================

@login_required
def shops_list(request):
    """Display all shops with location-based filtering."""
    shops = Shop.objects.all()
    shop_type = request.GET.get('type')
    search = request.GET.get('q')
    show_all = request.GET.get('show_all')
    
    # Filter by location (pincode) if user has pincode and not showing all
    if request.user.pincode and not show_all:
        shops = shops.filter(pincode=request.user.pincode)
    
    if shop_type:
        shops = shops.filter(shop_type=shop_type)
    
    if search:
        shops = shops.filter(Q(name__icontains=search) | Q(address__icontains=search))
    
    shops = shops.order_by('-rating')
    
    context = {
        'shops': shops,
        'shop_types': Shop.SHOP_TYPES,
        'current_type': shop_type,
        'user_pincode': request.user.pincode,
        'showing_all': bool(show_all),
    }
    return render(request, 'shops/list.html', context)


@login_required
def shop_detail(request, shop_id):
    """Display shop details and products."""
    shop = get_object_or_404(Shop, id=shop_id)
    products = shop.products.filter(is_available=True)
    reviews = shop.reviews.all()[:5]
    
    context = {
        'shop': shop,
        'products': products,
        'reviews': reviews,
        'avg_rating': reviews.aggregate(Avg('rating'))['rating__avg'] or 0,
    }
    return render(request, 'shops/detail.html', context)


# ==================== Product Views ====================

@login_required
def products_list(request):
    products = Product.objects.filter(is_available=True)

    if request.user.pincode:
        products = products.filter(
            shop__pincode=request.user.pincode
        )

    category = request.GET.get('category')
    shop_id = request.GET.get('shop')
    search = request.GET.get('q')

    if category:
        products = products.filter(category=category)

    if shop_id:
        products = products.filter(shop_id=shop_id)

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    context = {
        'products': products,
        'categories': products.values_list(
            'category',
            flat=True
        ).distinct(),
    }

    return render(request, 'products/list.html', context)


@login_required
def product_detail(request, product_id):
    """Display product details and reviews."""
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    
    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': reviews.aggregate(Avg('rating'))['rating__avg'] or 0,
    }
    return render(request, 'products/detail.html', context)


# ==================== Shopping List Views ====================

@login_required
def shopping_lists(request):
    """Display user's shopping lists."""
    lists = request.user.shopping_lists.all()
    
    context = {
        'lists': lists,
    }
    return render(request, 'lists/list.html', context)


@login_required
def create_shopping_list(request):
    """Create a new shopping list."""
    if request.method == 'POST':
        form = ShoppingListForm(request.POST)
        if form.is_valid():
            shopping_list = form.save(commit=False)
            shopping_list.user = request.user
            shopping_list.save()
            messages.success(request, 'Shopping list created successfully!')
            return redirect('shopping_list_detail', list_id=shopping_list.id)
    else:
        form = ShoppingListForm()
    
    return render(request, 'lists/create.html', {'form': form})


@login_required
def shopping_list_detail(request, list_id):
    """Display shopping list details."""
    shopping_list = get_object_or_404(ShoppingList, id=list_id, user=request.user)
    items = shopping_list.items.all()
    
    context = {
        'shopping_list': shopping_list,
        'items': items,
    }
    return render(request, 'lists/detail.html', context)


@login_required
def add_shopping_list_item(request, list_id):
    """Add item to shopping list."""
    shopping_list = get_object_or_404(ShoppingList, id=list_id, user=request.user)
    
    if request.method == 'POST':
        form = ShoppingListItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.shopping_list = shopping_list
            item.save()
            messages.success(request, 'Item added to shopping list!')
            return redirect('shopping_list_detail', list_id=list_id)
    else:
        form = ShoppingListItemForm()
    
    context = {
        'shopping_list': shopping_list,
        'form': form,
    }
    return render(request, 'lists/add_item.html', context)


@login_required
def delete_shopping_list(request, list_id):
    """Delete shopping list."""
    shopping_list = get_object_or_404(ShoppingList, id=list_id, user=request.user)
    
    if request.method == 'POST':
        shopping_list.delete()
        messages.success(request, 'Shopping list deleted!')
        return redirect('shopping_lists')
    
    return render(request, 'lists/confirm_delete.html', {'shopping_list': shopping_list})


# ==================== Cart & Order Views ====================

@login_required
def cart(request):
    """Display shopping cart."""
    cart_items = request.session.get('cart', {})
    
    products = Product.objects.filter(id__in=cart_items.keys())
    cart_data = []
    total = 0
    
    for product in products:
        quantity = cart_items[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_data.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    
    context = {
        'cart_items': cart_data,
        'total': total,
    }
    return render(request, 'cart/index.html', context)


@login_required
def add_to_cart(request, product_id):
    """Add product to cart."""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str] += quantity
    else:
        cart[product_id_str] = quantity
    
    request.session['cart'] = cart
    messages.success(request, f'{product.name} added to cart!')
    return redirect('product_detail', product_id=product_id)


@login_required
def remove_from_cart(request, product_id):
    """Remove product from cart."""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        messages.success(request, 'Item removed from cart!')
    
    return redirect('cart')


@login_required
def checkout(request):
    """Checkout page."""
    cart_items = request.session.get('cart', {})
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')
    
    products = Product.objects.filter(id__in=cart_items.keys())
    addresses = request.user.addresses.all()
    
    cart_data = []
    total = 0
    
    for product in products:
        quantity = cart_items[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_data.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    
    context = {
        'cart_items': cart_data,
        'addresses': addresses,
        'total': total,
    }
    return render(request, 'checkout/index.html', context)


@login_required
def create_order(request):
    """Create order from cart."""
    if request.method == 'POST':
        cart_items = request.session.get('cart', {})
        
        if not cart_items:
            messages.error(request, 'Your cart is empty!')
            return redirect('cart')
        
        address_id = request.POST.get('address')
        address = get_object_or_404(Address, id=address_id, user=request.user)
        
        products = Product.objects.filter(id__in=cart_items.keys())
        
        total = sum(product.price * cart_items[str(product.id)] for product in products)
        final_amount = total  # No tax, only total amount
        
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_amount=total,
            tax=0,  # No tax
            final_amount=final_amount,
            payment_method='cod',  # Cash on Delivery
            estimated_delivery=timezone.now() + timedelta(hours=2),
        )
        
        shops = set()
        for product in products:
            quantity = cart_items[str(product.id)]
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
                total=product.price * quantity,
            )
            shops.add(product.shop_id)
        
        order.shops.set(shops)
        
        # Create notification
        Notification.objects.create(
            user=request.user,
            notification_type='order_update',
            title='Order Confirmed',
            message=f'Your order #{order.id} has been confirmed!',
            related_order=order,
        )
        
        # Clear cart
        request.session['cart'] = {}
        
        messages.success(request, f'Order #{order.id} created successfully!')
        return redirect('order_detail', order_id=order.id)
    
    return redirect('checkout')


# ==================== Order Views ====================

@login_required
def orders_list(request):
    """Display user's orders."""
    orders = request.user.orders.all()
    status = request.GET.get('status')
    
    if status:
        orders = orders.filter(status=status)
    
    context = {
        'orders': orders,
        'statuses': Order.ORDER_STATUS,
    }
    return render(request, 'orders/list.html', context)


@login_required
def order_detail(request, order_id):
    """Display order details."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'orders/detail.html', context)


@login_required
def cancel_order(request, order_id):
    """Cancel an order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status not in ['pending', 'confirmed']:
        messages.error(request, 'This order cannot be cancelled.')
        return redirect('order_detail', order_id=order_id)
    
    if request.method == 'POST':
        order.status = 'cancelled'
        order.save()
        
        Notification.objects.create(
            user=request.user,
            notification_type='order_update',
            title='Order Cancelled',
            message=f'Your order #{order.id} has been cancelled.',
            related_order=order,
        )
        
        messages.success(request, 'Order cancelled successfully!')
        return redirect('orders_list')
    
    return render(request, 'orders/confirm_cancel.html', {'order': order})


# ==================== Notification Views ====================

@login_required
def notifications_list(request):
    """Display user's notifications."""
    if request.method == 'POST':
        # Mark all notifications as read
        request.user.notifications.filter(is_read=False).update(is_read=True)
        messages.success(request, 'All notifications marked as read.')
        return redirect('notifications')
    
    notifications = request.user.notifications.all().order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notifications/list.html', context)


@login_required
def mark_notification_read(request, notification_id):
    """Mark notification as read."""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')


# ==================== Review Views ====================

@login_required
def add_product_review(request, product_id):
    """Add review to product."""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.review_type = 'product'
            review.save()
            messages.success(request, 'Review posted successfully!')
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm()
    
    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'reviews/add_product_review.html', context)


@login_required
def add_shop_review(request, shop_id):
    """Add review to shop."""
    shop = get_object_or_404(Shop, id=shop_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.shop = shop
            review.review_type = 'shop'
            review.save()
            messages.success(request, 'Review posted successfully!')
            return redirect('shop_detail', shop_id=shop_id)
    else:
        form = ReviewForm()
    
    context = {
        'shop': shop,
        'form': form,
    }
    return render(request, 'reviews/add_shop_review.html', context)


# ==================== User Profile Views ====================

@login_required
def profile(request):

    if request.user.role == 'delivery_agent':
        delivery_agent = DeliveryAgent.objects.get(user=request.user)

        if request.method == 'POST':
            delivery_agent.is_active = not delivery_agent.is_active

            if delivery_agent.is_active:
                delivery_agent.status = 'available'
            else:
                delivery_agent.status = 'offline'

            delivery_agent.save()

            return redirect('profile')

        addresses = request.user.addresses.all()

        return render(request, 'profile/delivery_profile.html', {
            'delivery_agent': delivery_agent,
            'addresses': addresses,
        })

    addresses = request.user.addresses.all()
    recent_orders = request.user.orders.all()[:5]

    return render(request, 'profile/index.html', {
        'addresses': addresses,
        'recent_orders': recent_orders,
    })


@login_required
def edit_profile(request):
    delivery_agent = None

    if request.user.role == 'delivery_agent':
        delivery_agent = request.user.delivery_agent

    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            if delivery_agent:
                delivery_agent.vehicle_type = request.POST.get(
                    'vehicle_type',
                    delivery_agent.vehicle_type
                )

                delivery_agent.vehicle_number = request.POST.get(
                    'vehicle_number',
                    delivery_agent.vehicle_number
                )

                # delivery_agent.is_active = 'is_active' in request.POST

                # if delivery_agent.is_active:
                #     delivery_agent.status = 'available'
                # else:
                #     delivery_agent.status = 'offline'

                delivery_agent.save()

            messages.success(
                request,
                'Profile updated successfully!'
            )

            return redirect('profile')

    else:
        form = ProfileForm(instance=request.user)

    return render(
        request,
        'profile/edit.html',
        {
            'form': form,
            'delivery_agent': delivery_agent
        }
    )


@login_required
def add_address(request):
    """Add new address."""
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully!')
            return redirect('profile')
    else:
        form = AddressForm()
    
    return render(request, 'profile/add_address.html', {'form': form})


@login_required
def delete_address(request, address_id):
    """Delete an address."""
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted successfully!')
    return redirect('profile')


# ==================== Shop Owner Views ====================

@login_required
def edit_shop(request):
    """Edit or create shop details (shop owner only)."""
    if not request.user.is_shop_owner():
        messages.error(request, 'Only shop owners can access this page.')
        return redirect('home')
    
    try:
        shop = request.user.shop
        is_new = False
    except Shop.DoesNotExist:
        # Create a new shop for this user if it doesn't exist
        shop = Shop(owner=request.user)
        is_new = True
    
    if request.method == 'POST':
        from .forms import ShopForm
        form = ShopForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()
            if is_new:
                messages.success(request, 'Shop created successfully!')
            else:
                messages.success(request, 'Shop updated successfully!')
            return redirect('home')
    else:
        from .forms import ShopForm
        form = ShopForm(instance=shop)
    
    context = {
        'form': form,
        'shop': shop,
        'is_new': is_new,
    }
    return render(request, 'shop/edit.html', context)


@login_required
def delete_address(request, address_id):
    """Delete address."""
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Address deleted!')
        return redirect('profile')
    
    return render(request, 'profile/confirm_delete_address.html', {'address': address})


# ==================== Shop Owner Views ====================

@login_required
def shop_owner_accept_order(request, order_id):
    """Shop owner accepts an order."""
    try:
        shop = request.user.shop
    except Shop.DoesNotExist:
        messages.error(request, 'You do not have a shop.')
        return redirect('home')
    
    order = get_object_or_404(Order, id=order_id, shops=shop)
    
    if order.status == 'pending':
        order.status = 'confirmed'
        order.save()
        
        # Create notification for customer
        Notification.objects.create(
            user=order.user,
            notification_type='order_update',
            title='Order Accepted',
            message=f'Your order #{order.id} has been accepted by {shop.name}!',
            related_order=order,
        )
        
        messages.success(request, 'Order accepted successfully!')
    else:
        messages.warning(request, 'This order cannot be accepted.')
    
    return redirect('home')


@login_required
def shop_owner_complete_order(request, order_id):
    """Shop owner marks order as ready for delivery."""
    try:
        shop = request.user.shop
    except Shop.DoesNotExist:
        messages.error(request, 'You do not have a shop.')
        return redirect('home')
    
    order = get_object_or_404(Order, id=order_id, shops=shop)
    
    if order.status == 'confirmed':
        # Find nearby delivery agents
        nearby_agents = DeliveryAgent.objects.filter(
            user__pincode=shop.pincode,
            status='available',
            is_active=True
        )
        
        if request.method == 'POST':
            delivery_agent_id = request.POST.get('delivery_agent')
            delivery_agent = get_object_or_404(DeliveryAgent, id=delivery_agent_id)
            
            # Assign delivery agent
            order.delivery_agent = delivery_agent
            order.status = 'out_for_delivery'
            order.save()
            
            # Create notification for delivery agent
            Notification.objects.create(
                user=delivery_agent.user,
                notification_type='order_update',
                title='New Delivery Assignment',
                message=f'New order #{order.id} assigned to you for delivery.',
                related_order=order,
            )
            
            # Create notification for customer
            Notification.objects.create(
                user=order.user,
                notification_type='order_update',
                title='Delivery Agent Assigned',
                message=f'Your order #{order.id} is ready for delivery and assigned to a delivery agent.',
                related_order=order,
            )
            
            messages.success(request, 'Delivery agent assigned successfully!')
            return redirect('home')
        
        context = {
            'order': order,
            'delivery_agents': nearby_agents,
            'shop': shop,
        }
        return render(request, 'orders/assign_delivery.html', context)
    else:
        messages.warning(request, 'This order cannot be marked as ready.')
        return redirect('home')


@login_required
def assign_delivery_agent(request, order_id):
    """Deprecated: Assign delivery agent to order (use shop_owner_complete_order instead)."""
    return redirect('home')


# ==================== Delivery Agent Views ====================
@login_required
def delivery_agent_accept_order(request, order_id):
    try:
        delivery_agent = request.user.delivery_agent
    except:
        messages.error(request, 'You do not have a delivery agent profile.')
        return redirect('profile')

    order = get_object_or_404(
        Order,
        id=order_id,
        delivery_agent=delivery_agent
    )

    if (
        request.method == 'POST'
        and order.status == 'out_for_delivery'
        and not order.delivery_accepted
    ):

        order.delivery_accepted = True
        order.save()

        delivery_agent.status = 'busy'
        delivery_agent.current_orders += 1
        delivery_agent.save()

        Notification.objects.create(
            user=order.user,
            notification_type='order_update',
            title='Delivery Agent Accepted',
            message=f'Delivery agent {delivery_agent.user.get_full_name()} is on the way to deliver your order #{order.id}.',
            related_order=order,
        )

        messages.success(
            request,
            'Order delivery accepted! You are on the way.'
        )

    return redirect('home')


@login_required
def delivery_agent_deliver_order(request, order_id):
    """Delivery agent marks order as delivered."""
    try:
        delivery_agent = request.user.delivery_agent
    except:
        messages.error(request, 'You do not have a delivery agent profile.')
        return redirect('profile')
    
    order = get_object_or_404(Order, id=order_id, delivery_agent=delivery_agent)
    
    if order.status == 'out_for_delivery':
        if request.method == 'POST':
            order.status = 'delivery_confirmation_pending'
            order.actual_delivery = timezone.now()
            order.save()
            
            # Update delivery agent
            delivery_agent.status = 'available'
            delivery_agent.current_orders -= 1
            delivery_agent.total_deliveries += 1
            delivery_agent.save()
            
            # # Create notification for customer
            # Notification.objects.create(
            #     user=order.user,
            #     notification_type='order_update',
            #     title='Order Delivered',
            #     message=f'Your order #{order.id} has been delivered!',
            #     related_order=order,
            # )
            Notification.objects.create(
            user=order.user,
            notification_type='order_update',
            title='Confirm Delivery',
            message=f'Please confirm that you received order #{order.id}.',
            related_order=order,
        )
            
            # Create notification for shop owner(s)
            for shop in order.shops.all():
                Notification.objects.create(
                    user=shop.owner,
                    notification_type='order_update',
                    title='Order Delivered',
                    message=f'Order #{order.id} has been delivered to the customer.',
                    related_order=order,
                )
            
            messages.success(request, 'Order marked as delivered!')
            return redirect('home')
    else:
        messages.warning(request, 'This order cannot be marked as delivered.')
    
    return render(request, 'orders/confirm_delivery.html', {'order': order})

@login_required
def customer_confirm_delivery(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if request.method == 'POST':
        order.status = 'delivered'
        order.actual_delivery = timezone.now()
        order.save()

        messages.success(
            request,
            "Delivery confirmed successfully."
        )

    return redirect('home')
# ==================== Product Management Views (Shop Owner) ====================

@login_required
def shop_owner_products(request):
    """Shop owner view their products."""
    if not request.user.is_shop_owner():
        messages.error(request, 'Only shop owners can access this page.')
        return redirect('home')
    
    try:
        shop = request.user.shop
    except Shop.DoesNotExist:
        messages.error(request, 'You do not have a shop yet.')
        return redirect('home')
    
    products = shop.products.all().order_by('-created_at')
    
    context = {
        'shop': shop,
        'products': products,
    }
    return render(request, 'products/shop_owner_list.html', context)


@login_required
def add_product(request):
    """Shop owner add a new product."""
    if not request.user.is_shop_owner():
        messages.error(request, 'Only shop owners can add products.')
        return redirect('home')
    
    try:
        shop = request.user.shop
    except Shop.DoesNotExist:
        messages.error(request, 'You do not have a shop yet.')
        return redirect('home')
    
    if request.method == 'POST':
        from .forms import ProductForm
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = shop
            product.save()
            messages.success(request, f'Product "{product.name}" added successfully!')
            return redirect('shop_owner_products')
    else:
        from .forms import ProductForm
        form = ProductForm()
    
    context = {
        'form': form,
        'shop': shop,
    }
    return render(request, 'products/add.html', context)


@login_required
def edit_product(request, product_id):
    """Shop owner edit a product."""
    if not request.user.is_shop_owner():
        messages.error(request, 'Only shop owners can edit products.')
        return redirect('home')
    
    try:
        shop = request.user.shop
    except Shop.DoesNotExist:
        messages.error(request, 'You do not have a shop yet.')
        return redirect('home')
    
    product = get_object_or_404(Product, id=product_id, shop=shop)
    
    if request.method == 'POST':
        from .forms import ProductForm
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('shop_owner_products')
    else:
        from .forms import ProductForm
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'shop': shop,
    }
    return render(request, 'products/edit.html', context)


@login_required
def delete_product(request, product_id):
    """Shop owner delete a product."""
    if not request.user.is_shop_owner():
        messages.error(request, 'Only shop owners can delete products.')
        return redirect('home')
    
    try:
        shop = request.user.shop
    except Shop.DoesNotExist:
        messages.error(request, 'You do not have a shop yet.')
        return redirect('home')
    
    product = get_object_or_404(Product, id=product_id, shop=shop)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('shop_owner_products')
    
    context = {
        'product': product,
        'shop': shop,
    }
    return render(request, 'products/confirm_delete.html', context)