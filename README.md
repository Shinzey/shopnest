# ShopNest - Django + Bootstrap5 Edition

A complete rewrite of the ShopNest platform from Node.js/React to **Python/Django** with **Bootstrap5** frontend. This is a full-stack e-commerce solution combining the features of Instamart, Swiggy, Blinkit, and more.

## 🎯 Key Features

### 🏪 Shop Discovery
- Browse nearby shops with ratings and reviews
- Filter by shop type (Instamart, Swiggy, Quick Commerce, Grocery)
- Real-time shop status and delivery times
- Shop details and available products

### 📝 Shopping Lists
- Create and manage multiple shopping lists
- Add items with quantity and estimated price
- Track completed items
- Organize by categories

### 🛒 Shopping Experience
- Add products to cart from multiple shops
- Real-time cart updates
- One-click checkout
- Multiple payment methods support

### 💳 Billing & Orders
- Smart billing with automatic calculations
- Tax calculation (5% default)
- Order history and tracking
- Order status updates (pending, confirmed, preparing, out_for_delivery, delivered, cancelled)

### 🔔 Notifications
- Order update notifications
- Deal and promotion alerts
- Price drop notifications
- Reminder notifications

### 👤 User Management
- User registration and authentication
- Profile management
- Multiple address management
- Password management

### ⭐ Reviews & Ratings
- Rate shops
- Review products
- View community ratings

## 🏗️ Project Architecture

### Technology Stack
- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5 + HTML/CSS/JS (Server-side rendered)
- **Database**: SQLite (default), PostgreSQL compatible
- **Authentication**: Django built-in auth
- **Forms**: Django Forms

### System Design
- **Models**: 12+ Django models for complete e-commerce functionality
- **Views**: Function-based views with proper authentication
- **Templates**: Responsive Bootstrap5 templates
- **Admin**: Full Django admin interface
- **Forms**: Clean, reusable form classes
- **Security**: CSRF protection, password hashing, user authentication

## 📊 Database Models

1. **User** - Extended Django User model
2. **Address** - User addresses
3. **Shop** - Stores/shops information
4. **Product** - Products available in shops
5. **ShoppingList** - User shopping lists
6. **ShoppingListItem** - Items in shopping lists
7. **Order** - Customer orders
8. **OrderItem** - Items in orders
9. **Notification** - User notifications
10. **Review** - Shop and product reviews
11. **Preference** - User preferences

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation (5 minutes)

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Create admin user
python manage.py createsuperuser

# 5. Start server
python manage.py runserver
```

Access at: **http://localhost:8000**

## 📂 File Structure

```
shopnest_django/
├── core/                          # Main Django app
│   ├── models.py                  # Database models
│   ├── views.py                   # View logic (3000+ lines)
│   ├── forms.py                   # Django forms
│   ├── urls.py                    # URL routing
│   ├── admin.py                   # Admin configuration
│   └── apps.py                    # App config
│
├── shopnest/                      # Django project settings
│   ├── settings.py                # Settings
│   ├── urls.py                    # Main URL config
│   └── wsgi.py                    # WSGI config
│
├── templates/                     # HTML templates (20+ files)
│   ├── base.html                  # Base template
│   ├── auth/                      # Auth templates
│   ├── home/                      # Home page
│   ├── shops/                     # Shop templates
│   ├── products/                  # Product templates
│   ├── orders/                    # Order templates
│   ├── cart/                      # Cart template
│   ├── lists/                     # Shopping list templates
│   ├── profile/                   # Profile templates
│   ├── notifications/             # Notification templates
│   └── reviews/                   # Review templates
│
├── static/                        # Static files
├── media/                         # User uploads
├── manage.py                      # Django CLI
├── requirements.txt               # Python dependencies
└── SETUP.md                       # Detailed setup guide
```

## 🎨 Features Overview

### Authentication System
- User registration with email validation
- Secure login/logout
- Password hashing with Django's built-in system
- Session management

### Shopping & Cart
- Browse unlimited shops and products
- Add items to cart
- View cart summary with totals
- Checkout process with address selection
- Automatic tax calculation

### Order Management
- Create orders from cart
- Track order status
- View order history
- Cancel orders (if pending)
- Receive notifications on order updates

### Notifications
- Auto-generated order notifications
- Mark notifications as read
- Filter by notification type
- 30-day expiration

### Admin Interface
- Manage all entities (shops, products, users, orders)
- View analytics (sales, reviews, ratings)
- Create sample data
- Bulk operations

## 🛠️ Common Operations

### Add Sample Data
```bash
python manage.py shell
>>> from core.models import Shop, Product
>>> shop = Shop.objects.create(name="Sample Shop", ...)
>>> Product.objects.create(shop=shop, ...)
```

### Reset Database
```bash
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

### Collect Static Files
```bash
python manage.py collectstatic
```

### Create Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 🔒 Security Features

- ✅ CSRF protection on all forms
- ✅ Password hashing (PBKDF2)
- ✅ SQL injection prevention (Django ORM)
- ✅ User authentication required for sensitive operations
- ✅ Session-based authentication
- ✅ Input validation and sanitization

## 📈 Scalability

Current architecture supports:
- Thousands of users
- Millions of products
- Real-time order processing
- Can be deployed on AWS, Heroku, DigitalOcean, etc.

Optimization ready for:
- Database indexing
- Caching (Redis)
- CDN integration
- Load balancing

## 🌍 Deployment Options

### Local Development
```bash
python manage.py runserver
```

### Production with Gunicorn
```bash
gunicorn shopnest.wsgi:application
```

### Docker
```bash
docker build -t shopnest .
docker run -p 8000:8000 shopnest
```

### Cloud Platforms
- Heroku: `Procfile` ready
- PythonAnywhere
- AWS Elastic Beanstalk
- DigitalOcean App Platform

## 📝 API-Free Architecture

Unlike the original Node.js version:
- ❌ No external APIs (Google Maps, etc.)
- ❌ No third-party integrations
- ✅ Pure Django with built-in features
- ✅ Self-contained solution
- ✅ Easier to customize and deploy

## 🎓 Learning Resources

- [Django Official Docs](https://docs.djangoproject.com/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [Django Models Guide](https://docs.djangoproject.com/en/4.2/topics/db/models/)
- [Django Views Guide](https://docs.djangoproject.com/en/4.2/topics/http/views/)
- [Django Templates Guide](https://docs.djangoproject.com/en/4.2/topics/templates/)

## 🐛 Troubleshooting

**Issue**: Port already in use
```bash
python manage.py runserver 8001
```

**Issue**: ModuleNotFoundError
```bash
pip install -r requirements.txt
```

**Issue**: Static files not loading
```bash
python manage.py collectstatic
```

## 📞 Support & Contact

- GitHub Issues: Report bugs and suggest features
- Email: support@shopnest.com
- Documentation: See SETUP.md for detailed guide

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and create a Pull Request

## 📄 License

MIT License - Free for personal and commercial use

## 🎉 What's Next?

- [ ] Complete all template pages
- [ ] Add image upload functionality
- [ ] Email notifications
- [ ] Payment gateway integration
- [ ] Advanced search and filtering
- [ ] Mobile app version
- [ ] REST API (if needed)
- [ ] Performance optimization
- [ ] Unit & integration tests
- [ ] Deployment guides

---

**Built with ❤️ using Django and Bootstrap5**

Completely migrated from Node.js/React architecture to Python/Django with Bootstrap5 frontend.
superuser:admin
pass:123


shopowner
email:shop1@gmail.com, shop2@gmail.com
pass:helium@helium


customer
mail:customer1@gmail.com
pass:helium@helium

delivery
mail:delivery1@gmail.com
pass:helium@helium

https://outpour-unnamable-oink.ngrok-free.dev

shinan added git
safal bk

    delivery:
	delivery4@gmail.com	helium@helium

    customer:
	customer2@gmail.com
    customer1@gmail.com

    shop:
	shop2@gmail.com	
    shop1@gmail.com

	admin					123
	
	

