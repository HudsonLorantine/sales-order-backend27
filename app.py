import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:5173",
    "https://brave-coast-082fed100.2.azurestaticapps.net"
])

# Sample data for quick testing
customers = [
    {
        "id": 1,
        "company_name": "Acme Corporation",
        "contact_person": "John Doe",
        "email": "john@acme.com",
        "phone": "555-1234",
        "billing_address": "123 Main St, Anytown, USA"
    },
    {
        "id": 2,
        "company_name": "Globex Industries",
        "contact_person": "Jane Smith",
        "email": "jane@globex.com",
        "phone": "555-5678",
        "billing_address": "456 Oak Ave, Somewhere, USA"
    }
]

products = [
    {
        "id": 1,
        "sku": "PROD-001",
        "product_name": "Deluxe Widget",
        "description": "A premium quality widget",
        "unit_price": 29.99,
        "inventory_quantity": 100
    },
    {
        "id": 2,
        "sku": "PROD-002",
        "product_name": "Super Gadget",
        "description": "The latest in gadget technology",
        "unit_price": 49.99,
        "inventory_quantity": 50
    }
]

orders = [
    {
        "id": 1,
        "order_number": "ORD-20250626-001",
        "customer_id": 1,
        "order_date": "2025-06-20T08:00:00",
        "status": "issued",
        "payment_status": "unpaid",
        "total_amount": 149.95,
        "customer": customers[0]
    },
    {
        "id": 2,
        "order_number": "ORD-20250626-002",
        "customer_id": 2,
        "order_date": "2025-06-22T09:30:00",
        "status": "complete",
        "payment_status": "paid",
        "total_amount": 299.90,
        "customer": customers[1]
    }
]

@app.route('/')
def index():
    return jsonify({"message": "Sales Order API is running"})

@app.route('/api/customers')
def get_customers():
    return jsonify(customers)

@app.route('/api/products')
def get_products():
    return jsonify(products)

@app.route('/api/orders')
def get_orders():
    return jsonify(orders)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
