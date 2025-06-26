# Sales Order Management System - Backend API

A robust Flask-based REST API for managing sales orders, customers, and products with SQLAlchemy ORM.

## 🚀 Live Deployment

- **Production API**: https://sales-backend-new-7821.azurewebsites.net/api
- **Health Check**: https://sales-backend-new-7821.azurewebsites.net/api/customers

## 🛠️ Technology Stack

- **Framework**: Flask 3.1.1
- **Database**: SQLAlchemy 2.0.41 with SQLite (development) 
- **Authentication**: Flask-JWT-Extended 4.6.0
- **Password Hashing**: Flask-Bcrypt 1.0.1
- **CORS**: Flask-CORS 6.0.0
- **Server**: Gunicorn 23.0.0 (production)
- **Python**: 3.11+

## 🏗️ Project Structure

```
src/
├── models/              # Database models
│   ├── database.py      # Database configuration
│   └── user.py          # User model
├── routes/              # API route handlers
│   ├── auth.py          # Authentication routes
│   ├── customers.py     # Customer CRUD operations
│   ├── orders.py        # Order management
│   ├── payments.py      # Payment tracking
│   ├── products.py      # Product catalog
│   └── user.py          # User management
└── main.py              # Application entry point
```

## 💻 Local Development

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/sales-order-backend-new.git
cd sales-order-backend-new

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create database directory
mkdir -p src/database

# Run the application
python src/main.py
```

The API will be available at `http://localhost:5000`

## 📡 API Endpoints

### Customers
- `GET /api/customers` - List all customers
- `POST /api/customers` - Create new customer
- `GET /api/customers/{id}` - Get customer by ID
- `PUT /api/customers/{id}` - Update customer
- `DELETE /api/customers/{id}` - Delete customer

### Products
- `GET /api/products` - List all products
- `POST /api/products` - Create new product
- `GET /api/products/{id}` - Get product by ID
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product

### Orders
- `GET /api/orders` - List all orders
- `POST /api/orders` - Create new order
- `GET /api/orders/{id}` - Get order by ID
- `PUT /api/orders/{id}` - Update order
- `POST /api/orders/{id}/issue` - Issue order
- `POST /api/orders/{id}/complete` - Complete order
- `POST /api/orders/{id}/void` - Void order

### Payments
- `GET /api/orders/{id}/payments` - Get order payments
- `POST /api/orders/{id}/payments` - Record payment

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

## 🔧 Configuration

### Environment Variables
The application uses the following configuration:

```python
# Secret keys (change in production!)
SECRET_KEY = 'asdf#FGSgvasgf$5$WGT'
JWT_SECRET_KEY = 'super-secret'

# Database (SQLite for development)
SQLALCHEMY_DATABASE_URI = 'sqlite:///src/database/app.db'

# CORS Origins
CORS_ORIGINS = [
    "http://localhost:5173",  # Local development
    "https://brave-coast-082fed100.2.azurestaticapps.net"  # Production frontend
]
```

### Production Configuration
For production deployment, consider:
- Using PostgreSQL instead of SQLite
- Setting secure random secret keys
- Configuring proper logging
- Adding rate limiting
- Using environment variables for sensitive data

## 🚀 Deployment

### Automatic Deployment
This repository is configured with GitHub Actions for automatic deployment to Azure App Service.

**Deployment triggers:**
- Push to `main` or `master` branch
- Pull requests to `main` or `master` branch

### Manual Deployment

```bash
# Build deployment package
zip -r deployment.zip . -x "venv/*" ".git/*" ".github/*" "*.md"

# Deploy using Azure CLI
az webapp deploy --resource-group My_SalesSystem --name sales-backend-new-7821 --src-path deployment.zip --type zip
```

## 🔐 Secrets Configuration

For automated deployment, configure these secrets in your GitHub repository:

1. Go to Repository Settings → Secrets and variables → Actions
2. Add new repository secrets:
   - `AZURE_WEBAPP_NAME`: `sales-backend-new-7821`
   - `AZURE_WEBAPP_PUBLISH_PROFILE`: (Download from Azure portal)

### Getting Publish Profile:
1. Go to Azure Portal → App Services → sales-backend-new-7821
2. Click "Download publish profile"
3. Copy the entire XML content as the secret value

## 📊 Database Schema

### Customers
- id, company_name, contact_person, email, phone, billing_address
- created_at, updated_at

### Products  
- id, sku, product_name, description, unit_price, inventory_quantity
- created_at, updated_at

### Orders
- id, order_number, customer_id, order_date, delivery_address
- status (unissued, issued, complete, voided)
- payment_status (unpaid, partial, paid)
- total_amount, created_at, updated_at

### Line Items
- id, order_id, product_id, quantity, unit_price, line_total
- fulfillment_status, fulfilled_quantity

### Payments
- id, order_id, payment_amount, payment_date
- payment_method, reference_number

## 🔗 Related Repositories

- **Frontend**: [sales-order-frontend-new](https://github.com/your-username/sales-order-frontend-new)

## 🛠️ Development

### Running Tests
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run tests (when implemented)
python -m pytest tests/
```

### Database Migrations
```bash
# Initialize database
python -c "from src.main import app; app.app_context().push(); from src.models.database import db; db.create_all()"
```

## 🐛 Troubleshooting

### Common Issues

**Database Errors:**
- Ensure `src/database/` directory exists
- Check file permissions for SQLite database

**CORS Issues:**
- Verify frontend URL is in CORS_ORIGINS list
- Check if frontend URL matches exactly (no trailing slashes)

**Import Errors:**
- Ensure virtual environment is activated
- Verify all dependencies are installed with `pip install -r requirements.txt`

### Logging
Application logs can be viewed in Azure:
```bash
az webapp log tail --resource-group My_SalesSystem --name sales-backend-new-7821
```

## 📄 License

This project is proprietary software for sales order management.
