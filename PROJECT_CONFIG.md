# Sales Order Management System - Configuration & Deployment Guide

## 🏗️ Project Overview
A complete full-stack sales order management system built with React frontend and Flask backend, deployed on Microsoft Azure.

## 📁 Project Structure
```
sales-order-backend/          # Flask API Backend
├── app.py                   # Main Flask application
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── .github/workflows/       # CI/CD pipelines
└── src/                    # Source code modules

sales-order-frontend/        # React Frontend
├── src/App.jsx             # Main React application
├── package.json            # Node.js dependencies
├── staticwebapp.config.json # Azure Static Web Apps config
└── .github/workflows/      # CI/CD pipelines
```

## 🔗 Live Application URLs
- **Frontend**: https://orange-bay-0d657f50f.1.azurestaticapps.net
- **Backend API**: https://sales-order-backend.blueocean-64f72639.eastus.azurecontainerapps.io

## 🔧 Azure Resources Created

### Backend (Azure Container Apps)
```
Resource Group: sales-order-rg
Location: East US
Environment: sales-order-env
Container App: sales-order-backend
Container Registry: ca5b36a8af2eacr.azurecr.io
Port: 8080
```

### Frontend (Azure Static Web Apps)
```
Static Web App: orange-bay-0d657f50f
GitHub Repository: HudsonLorantine/sales-order-frontend27
Auto-deployment: Enabled via GitHub Actions
```

## 🔑 Key Configuration Files

### Backend Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p src/database
ENV PORT=8080
ENV PYTHONPATH=/app
ENV WEBSITE_HOSTNAME=0.0.0.0
EXPOSE $PORT
CMD gunicorn --bind 0.0.0.0:$PORT --timeout 120 --access-logfile - --error-logfile - app:app
```

### Frontend API Configuration
```javascript
const API_BASE_URL = 'https://sales-order-backend.blueocean-64f72639.eastus.azurecontainerapps.io/api';
```

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.1.1
- **Language**: Python 3.11
- **Server**: Gunicorn 23.0.0
- **CORS**: Flask-CORS 6.0.0
- **Container**: Docker
- **Hosting**: Azure Container Apps

### Frontend
- **Framework**: React 18+ with Vite
- **UI Library**: Shadcn/ui components
- **Styling**: Tailwind CSS
- **Routing**: React Router
- **Hosting**: Azure Static Web Apps

## 📊 API Endpoints

### Customers
- `GET /api/customers` - List all customers
- `POST /api/customers` - Create new customer
- `PUT /api/customers/<id>` - Update customer

### Products
- `GET /api/products` - List all products
- `POST /api/products` - Create new product
- `PUT /api/products/<id>` - Update product

### Orders
- `GET /api/orders` - List all orders
- `POST /api/orders` - Create new order
- `GET /api/orders/<id>` - Get single order
- `POST /api/orders/<id>/issue` - Issue order
- `POST /api/orders/<id>/complete` - Complete order
- `POST /api/orders/<id>/void` - Void order

### Payments
- `GET /api/orders/<id>/payments` - Get order payments
- `POST /api/orders/<id>/payments` - Record payment

## 🔄 CI/CD Pipeline

### Backend Deployment
1. Code pushed to GitHub (HudsonLorantine/sales-order-backend27)
2. GitHub Actions builds Docker image
3. Image pushed to Azure Container Registry
4. Azure Container Apps automatically deploys new revision

### Frontend Deployment
1. Code pushed to GitHub (HudsonLorantine/sales-order-frontend27)
2. GitHub Actions builds React app
3. Static files deployed to Azure Static Web Apps
4. CDN cache invalidated automatically

## 🗄️ Database Schema (In-Memory)

### Customers
```python
{
    "id": int,
    "company_name": str,
    "contact_person": str,
    "email": str,
    "phone": str,
    "billing_address": str
}
```

### Products
```python
{
    "id": int,
    "sku": str,
    "product_name": str,
    "description": str,
    "unit_price": float,
    "inventory_quantity": int
}
```

### Orders
```python
{
    "id": int,
    "order_number": str,
    "customer_id": int,
    "order_date": str (ISO format),
    "status": str (unissued|issued|complete|voided),
    "payment_status": str (unpaid|partial|paid),
    "total_amount": float,
    "delivery_address": str,
    "customer": dict,
    "line_items": list
}
```

## 🚀 Deployment Commands

### Backend Deployment
```bash
az containerapp up --name sales-order-backend --resource-group sales-order-rg --environment sales-order-env --source . --target-port 8080 --ingress external
```

### Local Development
```bash
# Backend
cd sales-order-backend
python app.py

# Frontend
cd sales-order-frontend
npm run dev
```

## 🔐 Security Considerations
- CORS enabled for all origins (development setup)
- HTTPS enforced on all endpoints
- Input validation on API routes
- Error handling with appropriate HTTP status codes

## 📝 Notes
- Data is stored in-memory (resets on container restart)
- For production, consider implementing persistent database
- Monitor Azure costs and resource usage
- Consider implementing authentication for production use

## 🎯 Future Enhancements
- Database integration (Azure SQL/PostgreSQL)
- User authentication and authorization
- Email notifications
- Inventory management
- Reporting and analytics
- Mobile responsive improvements

---
**Created**: June 27, 2025
**Last Updated**: June 27, 2025
**Version**: 1.0 (Master/Production)
