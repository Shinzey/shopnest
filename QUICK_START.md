# ShopNest Django - Quick Start Guide

## ⚡ Get Started in 5 Minutes

### Step 1: Setup Python Environment
```bash
cd shopnest_django
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup Database
```bash
python manage.py migrate
```

### Step 4: Create Admin User
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### Step 5: Run Server
```bash
python manage.py runserver
```

## 🌐 Access Points

- **Main App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Login**: http://localhost:8000/login
- **Register**: http://localhost:8000/register

## 📊 Add Sample Data

```bash
python manage.py shell

# Create a shop
from core.models import Shop, Product
from decimal import Decimal

shop = Shop.objects.create(
    name="Fresh Grocery",
    shop_type="grocery",
    address="123 Main Street",
    latitude=10.5276,
    longitude=76.2144,
    opening_time="08:00:00",
    closing_time="22:00:00",
    delivery_time=30,
    rating=4.5
)

# Create products
Product.objects.create(
    shop=shop,
    name="Milk (1L)",
    price=Decimal("60.00"),
    stock=50,
    sku="MILK001",
    category="Dairy"
)

Product.objects.create(
    shop=shop,
    name="Bread",
    price=Decimal("40.00"),
    stock=30,
    sku="BREAD001",
    category="Bakery"
)

# Exit
exit()
```

## 🧪 Test Workflow

1. **Register**: Create a new account at `/register/`
2. **Login**: Login with your credentials
3. **Browse**: Visit `/shops/` and `/products/`
4. **Add to Cart**: Click "Add to Cart" on any product
5. **Checkout**: Go to `/cart/` and proceed to checkout
6. **Place Order**: Complete the order process

## 📱 Available Pages

| Page | URL | Features |
|------|-----|----------|
| Home | `/` | Dashboard, featured items |
| Shops | `/shops/` | Shop listing, filtering |
| Products | `/products/` | Product search, filtering |
| Cart | `/cart/` | Cart management |
| Checkout | `/checkout/` | Order summary |
| Orders | `/orders/` | Order history, tracking |
| Profile | `/profile/` | User settings, addresses |
| Admin | `/admin/` | Django admin panel |

## 🔧 Common Commands

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Access shell
python manage.py shell

# See all available commands
python manage.py help
```

## 🚀 Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn shopnest.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker
```bash
# Build image
docker build -t shopnest-django .

# Run container
docker run -p 8000:8000 shopnest-django
```

## 🔐 Security Checklist

Before production:
- [ ] Set `DEBUG = False` in settings
- [ ] Generate new `SECRET_KEY`
- [ ] Set `ALLOWED_HOSTS` correctly
- [ ] Use HTTPS
- [ ] Configure database password
- [ ] Enable CSRF protection
- [ ] Set secure session cookies

## 📝 Project Structure

```
shopnest_django/
├── core/                    # Django app (models, views, forms)
├── shopnest/                # Django project (settings, urls, wsgi)
├── templates/               # HTML templates (Bootstrap5)
├── static/                  # CSS, JS, images
├── media/                   # User uploads
├── manage.py                # Django CLI
└── requirements.txt         # Dependencies
```

## 🐛 Troubleshooting

**Problem**: `python: command not found`
- Solution: Install Python 3.10+ or use `python3`

**Problem**: Port 8000 already in use
- Solution: `python manage.py runserver 8001`

**Problem**: Static files not loading
- Solution: `python manage.py collectstatic --noinput`

**Problem**: Database locked
- Solution: Delete `db.sqlite3` and run migrations again

**Problem**: Import errors
- Solution: Ensure virtual environment is activated and pip install done

## 📚 Key Files

| File | Purpose |
|------|---------|
| `models.py` | Database models |
| `views.py` | View logic (3000+ lines) |
| `forms.py` | Django forms |
| `urls.py` | URL routing |
| `admin.py` | Admin configuration |
| `base.html` | Base template |

## 🎨 Bootstrap5 Components Used

- Navbar with dropdown menus
- Cards for product/shop display
- Tables for orders and items
- Forms with validation
- Modals and alerts
- Responsive grid layout
- Navigation breadcrumbs
- Badges and pills
- Button groups

## ✨ Features Implemented

✅ User Authentication (Register/Login/Logout)
✅ Profile Management
✅ Shop Browsing with Filtering
✅ Product Catalog
✅ Shopping Cart
✅ Order Creation & Tracking
✅ Shopping Lists
✅ Notifications
✅ Reviews & Ratings
✅ Address Management
✅ Admin Panel
✅ Responsive Design

## 🔄 Next Steps

1. **Customize**: Modify templates and colors
2. **Add Content**: Populate with shops and products
3. **Deploy**: Use Docker or cloud platform
4. **Monitor**: Check logs and user feedback
5. **Scale**: Add caching and optimization

## 📞 Need Help?

- Check `SETUP.md` for detailed documentation
- Review `README.md` for overview
- Check Django official docs: https://docs.djangoproject.com/
- See Django admin: http://localhost:8000/admin/

---

**Ready to launch? Start the server and visit http://localhost:8000!** 🚀
