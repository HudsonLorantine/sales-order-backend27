from flask import Blueprint, request, jsonify
from src.models.database import db, Customer

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/customers', methods=['GET'])
def get_customers():
    """Get all customers with optional search"""
    search = request.args.get('search', '')
    
    query = Customer.query
    if search:
        query = query.filter(
            Customer.company_name.contains(search) |
            Customer.contact_person.contains(search) |
            Customer.email.contains(search)
        )
    
    customers = query.all()
    return jsonify([customer.to_dict() for customer in customers])

@customers_bp.route('/customers', methods=['POST'])
def create_customer():
    """Create a new customer"""
    data = request.get_json()
    
    if not data or not data.get('company_name') or not data.get('email'):
        return jsonify({'error': 'Company name and email are required'}), 400
    
    customer = Customer(
        company_name=data['company_name'],
        contact_person=data.get('contact_person'),
        email=data['email'],
        phone=data.get('phone'),
        billing_address=data.get('billing_address')
    )
    
    try:
        db.session.add(customer)
        db.session.commit()
        return jsonify(customer.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customers_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get a specific customer"""
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.to_dict())

@customers_bp.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Update a customer"""
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    customer.company_name = data.get('company_name', customer.company_name)
    customer.contact_person = data.get('contact_person', customer.contact_person)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)
    customer.billing_address = data.get('billing_address', customer.billing_address)
    
    try:
        db.session.commit()
        return jsonify(customer.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customers_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """Delete a customer"""
    customer = Customer.query.get_or_404(customer_id)
    
    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

