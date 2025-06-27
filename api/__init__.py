import logging
import azure.functions as func
from flask import Flask, jsonify, request

app = Flask(__name__)

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

def main(req: func.HttpRequest) -> func.HttpResponse:
    route = req.route_params.get('route', '')
    
    if route == '' or route == 'index':
        return func.HttpResponse(
            jsonify({"message": "Sales Order API is running"}).data,
            mimetype="application/json"
        )
    elif route == 'health':
        return func.HttpResponse(
            jsonify({
                "status": "healthy",
                "message": "Health check endpoint is working"
            }).data,
            mimetype="application/json"
        )
    elif route == 'customers':
        return func.HttpResponse(
            jsonify(customers).data,
            mimetype="application/json"
        )
    elif route == 'products':
        return func.HttpResponse(
            jsonify(products).data,
            mimetype="application/json"
        )
    elif route == 'orders':
        return func.HttpResponse(
            jsonify(orders).data,
            mimetype="application/json"
        )
    else:
        return func.HttpResponse(
            jsonify({"error": "Route not found"}).data,
            mimetype="application/json",
            status_code=404
        )
