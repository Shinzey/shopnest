# ShopNest - Django & Bootstrap5 Version

This is a complete rewrite of ShopNest from Node.js/React to **Python/Django** with **Bootstrap5** frontend (no external APIs).

## 🎯 What's Changed

- **Backend**: Node.js/Express → **Django**
- **Frontend**: React → **Bootstrap5** (Server-side rendered HTML templates)
- **Database**: MongoDB → **SQLite** (default, easily switchable to PostgreSQL)
- **Styling**: Custom CSS → **Bootstrap5** + Custom CSS
- **APIs**: Removed all external APIs (Google Maps, etc.)

## 📋 Prerequisites

- Python 3.10+
- pip (Python package manager)
- Virtual environment (venv)

## 🚀 Installation & Setup

### 1. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
# By default, SQLite is used, so minimal configuration needed
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Follow the prompts to create an admin account
```

### 6. Load Sample Data (Optional)
```bash
# Create initial shops, products, etc.
python manage.py shell
# Inside the shell, you can create sample data
```

### 7. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Access the application at: **http://localhost:8000**

Admin panel: **http://localhost:8000/admin**

## 📁 Project Structure

```
shopnest_django/
├── shopnest/                    # Main Django project
│   ├── settings.py              # Settings
│   ├── urls.py                  # Main URLs
│   ├── wsgi.py                  # WSGI config
│
├── core/                        # Main Django app
│   ├── models.py                # Database models
│   ├── views.py                 # View logic
│   ├── forms.py                 # Django forms
│   ├── urls.py                  # App URLs
│   ├── admin.py                 # Admin configuration
│   └── apps.py                  # App config
│
├── templates/                   # HTML templates
│   ├── base.html                # Base template
│   ├── auth/                    # Authentication templates
│   ├── home/                    # Home page
│   ├── shops/                   # Shop templates
│   ├── products/                # Product templates
│   ├── orders/                  # Order templates
│   ├── cart/                    # Cart templates
│   ├── lists/                   # Shopping lists
│   ├── notifications/           # Notifications
│   ├── profile/                 # User profile
│   └── reviews/                 # Review templates
│
├── static/                      # Static files (CSS, JS, Images)
│   ├── css/                     # Custom CSS
│   ├── js/                      # Custom JavaScript
│   └── images/                  # Images
│
├── media/                       # User uploaded files
│   ├── avatars/                 # User avatars
│   ├── shop_logos/              # Shop logos
│   └── products/                # Product images
│
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
└── .env.example                 # Environment variables example
```

## 🗄️ Database Models

### User (Extended Django User)
- username (email-based)
- first_name, last_name
- phone number
- avatar

### Shop
- name
- type (instamart, swiggy, quickcommerce, grocery)
- location (lat, lng)
- rating
- delivery_time
- opening/closing hours

### Product
- name, description
- price, stock
- category
- shop (ForeignKey)

### ShoppingList
- user (ForeignKey)
- name, description
- items (with quantity, unit, estimated price)

### Order
- user (ForeignKey)
- shops (ManyToMany)
- address (ForeignKey)
- items (OrderItem)
- status (pending, confirmed, preparing, out_for_delivery, delivered, cancelled)
- payment_status

### Notification
- user (ForeignKey)
- type (order_update, deal, price_drop, reminder)
- message
- related_order, related_shop, related_product

### Review
- user (ForeignKey)
- shop or product (ForeignKey)
- rating, title, comment

## 🎨 Features & Views

### Authentication
- ✅ User Registration
- ✅ User Login/Logout
- ✅ Profile Management

### Shops & Products
- ✅ Browse Shops (with filtering)
- ✅ Shop Details & Products
- ✅ Product Search & Details
- ✅ Add Reviews to Shops & Products

### Shopping Lists
- ✅ Create/Edit Shopping Lists
- ✅ Add Items to Lists
- ✅ Mark Items as Completed
- ✅ Share Lists (template ready)

### Cart & Orders
- ✅ Add Products to Cart
- ✅ Checkout Process
- ✅ Create Orders
- ✅ Order History
- ✅ Track Orders

### Notifications
- ✅ View Notifications
- ✅ Mark as Read
- ✅ Auto-generated for Order Updates

### User Profile
- ✅ Update Profile Information
- ✅ Manage Addresses
- ✅ View Order History

## 📝 Forms Available

- UserRegistrationForm
- UserLoginForm
- ProfileForm
- AddressForm
- ShoppingListForm
- ShoppingListItemForm
- OrderForm
- ReviewForm

## 🔐 Admin Panel

Access Django admin at `/admin/` with your superuser credentials.

Features:
- Manage Users, Shops, Products
- View Orders and Notifications
- Manage Shopping Lists
- Monitor Reviews

## 🌐 URL Patterns

```
/                                  # Home
/register/                         # Register
/login/                            # Login
/logout/                           # Logout
/profile/                          # User Profile
/profile/edit/                     # Edit Profile
/profile/address/add/              # Add Address
/shops/                            # All Shops
/shops/<id>/                       # Shop Detail
/products/                         # All Products
/products/<id>/                    # Product Detail
/cart/                             # Shopping Cart
/cart/add/<product_id>/            # Add to Cart
/checkout/                         # Checkout
/orders/                           # Order History
/orders/<id>/                      # Order Detail
/lists/                            # Shopping Lists
/lists/create/                     # Create List
/notifications/                    # Notifications
```

## 🛠️ Common Tasks

### Run Tests
```bash
python manage.py test
```

### Create Sample Data
```bash
python manage.py shell

# Inside shell:
from core.models import Shop, Product, User
from decimal import Decimal

# Create a shop
shop = Shop.objects.create(
    name="Sample Shop",
    shop_type="grocery",
    address="123 Main St",
    latitude=10.5276,
    longitude=76.2144,
    delivery_time=30,
    rating=4.5
)

# Create a product
Product.objects.create(
    shop=shop,
    name="Milk",
    price=Decimal("50.00"),
    stock=100,
    sku="MILK001",
    category="Dairy"
)
```

### Reset Database
```bash
# Delete migrations (careful!)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Create fresh database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 📦 Deployment

### Using Gunicorn (Production)
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn shopnest.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker
```bash
docker build -t shopnest-django .
docker run -p 8000:8000 shopnest-django
```

### Environment Variables for Production
```bash
DEBUG=False
SECRET_KEY=your-secure-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=shopnest_prod
DATABASE_USER=postgres
DATABASE_PASSWORD=secure-password
DATABASE_HOST=your-db-host
DATABASE_PORT=5432
```

## 📚 Switching Databases

### SQLite to PostgreSQL

1. Install PostgreSQL package:
```bash
pip install psycopg2-binary
```

2. Update `.env`:
```
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=shopnest_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

3. Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DATABASE_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST': os.environ.get('DATABASE_HOST', ''),
        'PORT': os.environ.get('DATABASE_PORT', ''),
    }
}
```

4. Run migrations:
```bash
python manage.py migrate
```

## 🐛 Troubleshooting

### Issue: Port 8000 already in use
```bash
python manage.py runserver 8001
```

### Issue: Static files not loading
```bash
python manage.py collectstatic
```

### Issue: Migrations conflict
```bash
python manage.py migrate --fake
python manage.py migrate --fake-initial
```

### Issue: Import errors
Ensure virtual environment is activated and packages are installed:
```bash
pip install -r requirements.txt
```

## 🔗 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Models](https://docs.djangoproject.com/en/4.2/topics/db/models/)

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## ✅ Todo

- [ ] Complete all templates (shops/detail, products/detail, etc.)
- [ ] Add pagination to list views
- [ ] Implement search functionality
- [ ] Add image upload for products/shops
- [ ] Email notifications
- [ ] SMS notifications
- [ ] Map integration (Leaflet.js)
- [ ] Payment gateway integration
- [ ] Advanced filtering
- [ ] Analytics dashboard
- [ ] API endpoints (if needed later)
- [ ] Mobile responsiveness polish
- [ ] Performance optimization
- [ ] Caching strategy
- [ ] Unit tests

## 📞 Support

For issues and questions, please open an issue on GitHub or contact support@shopnest.com
