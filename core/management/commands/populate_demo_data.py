"""
Management command to populate demo data for ShopNest.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import User, Shop, Product, ShoppingList, Order, OrderItem, DeliveryAgent, Preference
import random


class Command(BaseCommand):
    help = 'Populate demo data for ShopNest'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo data...')
        
        # Clear existing demo data
        User.objects.filter(email__contains='@shopnest.com').delete()
        
        # Create demo customers
        customers = []
        pincodes = ['110001', '110002', '110005', '110015']  # Delhi pincodes
        cities = ['Delhi', 'Delhi', 'Delhi', 'Delhi']
        villages = ['', '', 'Dwarka', 'Rohini']
        
        for i in range(3):
            user = User.objects.create_user(
                username=f'customer{i+1}@shopnest.com',
                email=f'customer{i+1}@shopnest.com',
                password='demo@1234',
                first_name=f'Customer',
                last_name=f'{i+1}',
                role='customer',
                phone=f'9800{i:06d}',
                pincode=pincodes[i],
                city=cities[i],
                village=villages[i],
                is_verified=True,
            )
            Preference.objects.create(user=user)
            customers.append(user)
            self.stdout.write(self.style.SUCCESS(f'✓ Created customer: {user.email}'))
        
        # Create demo shop owners
        shop_owners = []
        for i in range(2):
            user = User.objects.create_user(
                username=f'owner{i+1}@shopnest.com',
                email=f'owner{i+1}@shopnest.com',
                password='demo@1234',
                first_name=f'Shop Owner',
                last_name=f'{i+1}',
                role='shop_owner',
                phone=f'9900{i:06d}',
                pincode=pincodes[i],
                city=cities[i],
                village=villages[i] if i == 1 else '',
                is_verified=True,
            )
            Preference.objects.create(user=user)
            shop_owners.append(user)
            self.stdout.write(self.style.SUCCESS(f'✓ Created shop owner: {user.email}'))
        
        # Create more demo shop owners (ensure they don't exist)
        for i in range(2, 5):
            username = f'owner{i}@shopnest.com'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=username,
                    password='demo@1234',
                    first_name=f'Shop Owner',
                    last_name=f'{i}',
                    role='shop_owner',
                    phone=f'9900{i:06d}',
                    pincode=pincodes[i % len(pincodes)],
                    city=cities[i % len(cities)],
                    village=villages[i % len(villages)],
                    is_verified=True,
                )
                Preference.objects.create(user=user)
                shop_owners.append(user)
                self.stdout.write(self.style.SUCCESS(f'✓ Created shop owner: {user.email}'))
        
        # Create demo delivery agents
        delivery_agents = []
        for i in range(2):
            user = User.objects.create_user(
                username=f'delivery{i+1}@shopnest.com',
                email=f'delivery{i+1}@shopnest.com',
                password='demo@1234',
                first_name=f'Delivery Agent',
                last_name=f'{i+1}',
                role='delivery_agent',
                phone=f'9700{i:06d}',
                pincode=pincodes[i],
                city=cities[i],
                village=villages[i] if i == 1 else '',
                is_verified=True,
            )
            Preference.objects.create(user=user)
            delivery_agents.append(user)
            
            # Create DeliveryAgent profile
            DeliveryAgent.objects.create(
                user=user,
                vehicle_type='bike' if i % 2 == 0 else 'car',
                vehicle_number=f'DL{i:02d}AB{i:04d}',
                status='available',
                rating=4.5 + random.random(),
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Created delivery agent: {user.email}'))
        
        # Create demo shops
        shops_data = [
            {
                'name': 'Fresh Fruits Market',
                'address': 'MG Road, Delhi',
                'pincode': '110001',
                'city': 'Delhi',
                'village': '',
                'shop_type': 'grocery',
            },
            {
                'name': 'Spice Junction',
                'address': 'Khan Market, Delhi',
                'pincode': '110002',
                'city': 'Delhi',
                'village': '',
                'shop_type': 'grocery',
            },
            {
                'name': 'Daily Essentials',
                'address': 'Dwarka, Delhi',
                'pincode': '110005',
                'city': 'Delhi',
                'village': '',
                'shop_type': 'grocery',
            },
        ]
        
        from datetime import time
        shops = []
        for i, shop_data in enumerate(shops_data):
            shop = Shop.objects.create(
                name=shop_data['name'],
                address=shop_data['address'],
                pincode=shop_data['pincode'],
                city=shop_data['city'],
                village=shop_data.get('village', ''),
                shop_type=shop_data['shop_type'],
                owner=shop_owners[i % len(shop_owners)],
                latitude=28.6139 + i * 0.01,
                longitude=77.2090 + i * 0.01,
                opening_time=time(9, 0),
                closing_time=time(22, 0),
                delivery_time=30,
                min_order=50,
                delivery_charge=10,
                rating=4.0 + random.random(),
            )
            shops.append(shop)
            self.stdout.write(self.style.SUCCESS(f'✓ Created shop: {shop.name}'))
        
        # Create demo products
        products_data = [
            {'name': 'Fresh Apples', 'category': 'fruits', 'price': 60, 'stock': 50},
            {'name': 'Organic Spinach', 'category': 'vegetables', 'price': 30, 'stock': 100},
            {'name': 'Red Tomatoes', 'category': 'vegetables', 'price': 40, 'stock': 80},
            {'name': 'Basmati Rice (1kg)', 'category': 'grains', 'price': 150, 'stock': 100},
            {'name': 'Turmeric Powder (100g)', 'category': 'spices', 'price': 80, 'stock': 60},
            {'name': 'Chaat Masala (50g)', 'category': 'spices', 'price': 50, 'stock': 70},
            {'name': 'Bananas (Bunch)', 'category': 'fruits', 'price': 50, 'stock': 90},
            {'name': 'Milk (1L)', 'category': 'dairy', 'price': 45, 'stock': 120},
        ]
        
        for shop in shops:
            for j, product_data in enumerate(products_data):
                product = Product.objects.create(
                    shop=shop,
                    name=product_data['name'],
                    description=f'High-quality {product_data["name"].lower()}',
                    category=product_data['category'],
                    price=product_data['price'],
                    stock=product_data['stock'],
                    sku=f'SKU-{shop.id}-{j+1}',
                    is_available=True,
                )
                self.stdout.write(f'  ✓ Created product: {product.name}')
        
        # Create demo shopping lists
        for customer in customers[:1]:
            shopping_list = ShoppingList.objects.create(
                user=customer,
                shop=shops[0],
                name='Weekly Groceries',
                description='Weekly shopping list for family',
                status='draft',
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Created shopping list: {shopping_list.name}'))
        
        # Create demo orders
        from core.models import Address
        from datetime import timedelta
        for customer in customers[:1]:
            # Create an address for the customer
            address = Address.objects.create(
                user=customer,
                address_type='home',
                address='123 Main Street, Delhi',
                latitude=28.6139,
                longitude=77.2090,
                is_primary=True,
            )
            
            order = Order.objects.create(
                user=customer,
                address=address,
                delivery_agent=DeliveryAgent.objects.filter(user__role='delivery_agent').first(),
                total_amount=500,
                final_amount=510,
                tax=10,
                status='pending',
                payment_method='cash_on_delivery',
                estimated_delivery=timezone.now() + timedelta(hours=1),
            )
            
            # Add shops to the order
            order.shops.add(shops[0])
            
            # Add order items
            for product in shops[0].products.all()[:2]:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=2,
                    price=product.price,
                    total=product.price * 2,
                )
            
            self.stdout.write(self.style.SUCCESS(f'✓ Created order: Order #{order.id}'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Demo data population completed!'))
        self.stdout.write(self.style.WARNING('\n📝 Demo Credentials:'))
        self.stdout.write('Customer: customer1@shopnest.com | demo@1234')
        self.stdout.write('Shop Owner: owner1@shopnest.com | demo@1234')
        self.stdout.write('Delivery Agent: delivery1@shopnest.com | demo@1234')
