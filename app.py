import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['*'])  # Allow all origins for testing

# Debug information
print(f"Python version: {sys.version}")
print(f"Environment variables: {os.environ}")

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

@app.route('/api/health')
def health_check():
    # Return details about the environment for debugging
    return jsonify({
        "status": "healthy",
        "python_version": sys.version,
        "environment": str(dict(os.environ)),
        "message": "Health check endpoint is working"
    })

@app.route('/api/customers')
def get_customers():
    return jsonify(customers)

@app.route('/api/products')
def get_products():
    return jsonify(products)

@app.route('/api/orders')
def get_orders():
    return jsonify(orders)

# POST route for creating new customers
@app.route('/api/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    new_id = max([c['id'] for c in customers]) + 1 if customers else 1
    customer = {
        'id': new_id,
        'company_name': data.get('company_name', ''),
        'contact_person': data.get('contact_person', ''),
        'email': data.get('email', ''),
        'phone': data.get('phone', ''),
        'billing_address': data.get('billing_address', '')
    }
    customers.append(customer)
    return jsonify(customer), 201

# PUT route for updating customers
@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    for customer in customers:
        if customer['id'] == customer_id:
            customer.update(data)
            return jsonify(customer)
    return jsonify({'error': 'Customer not found'}), 404

# POST route for creating new products
@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_id = max([p['id'] for p in products]) + 1 if products else 1
    product = {
        'id': new_id,
        'sku': data.get('sku', ''),
        'product_name': data.get('product_name', ''),
        'description': data.get('description', ''),
        'unit_price': float(data.get('unit_price', 0)),
        'inventory_quantity': int(data.get('inventory_quantity', 0))
    }
    products.append(product)
    return jsonify(product), 201

# PUT route for updating products
@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    for product in products:
        if product['id'] == product_id:
            product.update(data)
            return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

# POST route for creating new orders
@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_id = max([o['id'] for o in orders]) + 1 if orders else 1
    
    # Find customer
    customer = next((c for c in customers if c['id'] == int(data.get('customer_id'))), None)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 400
    
    # Generate order number
    from datetime import datetime
    order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{new_id:03d}"
    
    # Calculate total from line items
    line_items = data.get('line_items', [])
    total_amount = sum(item['quantity'] * item['unit_price'] for item in line_items)
    
    order = {
        'id': new_id,
        'order_number': order_number,
        'customer_id': int(data.get('customer_id')),
        'order_date': datetime.now().isoformat(),
        'status': 'unissued',
        'payment_status': 'unpaid',
        'total_amount': total_amount,
        'delivery_address': data.get('delivery_address', ''),
        'customer': customer,
        'line_items': line_items
    }
    orders.append(order)
    return jsonify(order), 201

# Order action routes
@app.route('/api/orders/<int:order_id>/issue', methods=['POST'])
def issue_order(order_id):
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'issued'
            return jsonify(order)
    return jsonify({'error': 'Order not found'}), 404

@app.route('/api/orders/<int:order_id>/complete', methods=['POST'])
def complete_order(order_id):
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'complete'
            return jsonify(order)
    return jsonify({'error': 'Order not found'}), 404

@app.route('/api/orders/<int:order_id>/void', methods=['POST'])
def void_order(order_id):
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'voided'
            return jsonify(order)
    return jsonify({'error': 'Order not found'}), 404

# Get single order
@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    for order in orders:
        if order['id'] == order_id:
            return jsonify(order)
    return jsonify({'error': 'Order not found'}), 404

# Payment routes
@app.route('/api/orders/<int:order_id>/payments', methods=['GET'])
def get_order_payments(order_id):
    # For now, return empty array as we're using in-memory data
    return jsonify([])

@app.route('/api/orders/<int:order_id>/payments', methods=['POST'])
def create_payment(order_id):
    data = request.get_json()
    # For now, just return success as we're using in-memory data
    return jsonify({'message': 'Payment recorded', 'order_id': order_id}), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
