from flask import Blueprint, request, jsonify
from src.models.database import db, SalesOrder, OrderLineItem, Product, Customer
from datetime import datetime
import uuid

orders_bp = Blueprint('orders', __name__)

def generate_order_number():
    """Generate a unique order number"""
    return f"SO-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

@orders_bp.route('/orders', methods=['GET'])
def get_orders():
    """Get all orders with optional filtering"""
    status = request.args.get('status')
    customer_id = request.args.get('customer_id')
    
    query = SalesOrder.query
    if status:
        query = query.filter(SalesOrder.status == status)
    if customer_id:
        query = query.filter(SalesOrder.customer_id == customer_id)
    
    orders = query.order_by(SalesOrder.created_at.desc()).all()
    return jsonify([order.to_dict() for order in orders])

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    """Create a new sales order"""
    data = request.get_json()
    
    if not data or not data.get('customer_id') or not data.get('line_items'):
        return jsonify({'error': 'Customer ID and line items are required'}), 400
    
    # Verify customer exists
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    # Create order
    order = SalesOrder(
        order_number=generate_order_number(),
        customer_id=data['customer_id'],
        delivery_address=data.get('delivery_address'),
        status='unissued'
    )
    
    total_amount = 0
    
    try:
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Add line items
        for item_data in data['line_items']:
            product = Product.query.get(item_data['product_id'])
            if not product:
                return jsonify({'error': f'Product {item_data["product_id"]} not found'}), 404
            
            quantity = item_data['quantity']
            unit_price = item_data.get('unit_price', product.unit_price)
            line_total = quantity * float(unit_price)
            
            line_item = OrderLineItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total
            )
            
            db.session.add(line_item)
            total_amount += line_total
        
        order.total_amount = total_amount
        db.session.commit()
        
        return jsonify(order.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get a specific order"""
    order = SalesOrder.query.get_or_404(order_id)
    return jsonify(order.to_dict())

@orders_bp.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """Update an order (only if unissued)"""
    order = SalesOrder.query.get_or_404(order_id)
    
    if order.status != 'unissued':
        return jsonify({'error': 'Can only edit unissued orders'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    order.delivery_address = data.get('delivery_address', order.delivery_address)
    
    try:
        db.session.commit()
        return jsonify(order.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/orders/<int:order_id>/issue', methods=['POST'])
def issue_order(order_id):
    """Issue an order (allocate inventory)"""
    order = SalesOrder.query.get_or_404(order_id)
    
    if order.status != 'unissued':
        return jsonify({'error': 'Order is already issued or completed'}), 400
    
    try:
        # Check inventory availability and allocate
        for line_item in order.line_items:
            product = line_item.product
            if product.inventory_quantity < line_item.quantity:
                return jsonify({
                    'error': f'Insufficient inventory for {product.product_name}. Available: {product.inventory_quantity}, Required: {line_item.quantity}'
                }), 400
        
        # Allocate inventory
        for line_item in order.line_items:
            product = line_item.product
            product.inventory_quantity -= line_item.quantity
        
        order.status = 'issued'
        db.session.commit()
        
        return jsonify(order.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/orders/<int:order_id>/void', methods=['POST'])
def void_order(order_id):
    """Void an order (return allocated inventory)"""
    order = SalesOrder.query.get_or_404(order_id)
    
    if order.status not in ['issued', 'unissued']:
        return jsonify({'error': 'Cannot void completed orders'}), 400
    
    try:
        # Return allocated inventory if order was issued
        if order.status == 'issued':
            for line_item in order.line_items:
                product = line_item.product
                product.inventory_quantity += line_item.quantity
        
        order.status = 'voided'
        db.session.commit()
        
        return jsonify(order.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/orders/<int:order_id>/complete', methods=['POST'])
def complete_order(order_id):
    """Complete an order"""
    order = SalesOrder.query.get_or_404(order_id)
    
    if order.status != 'issued':
        return jsonify({'error': 'Order must be issued before completion'}), 400
    
    try:
        # Mark all unfulfilled items as fulfilled
        for line_item in order.line_items:
            if line_item.fulfillment_status == 'unfulfilled':
                line_item.fulfillment_status = 'fulfilled'
                line_item.fulfilled_quantity = line_item.quantity
        
        order.status = 'complete'
        db.session.commit()
        
        return jsonify(order.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/orders/<int:order_id>/line-items/<int:line_item_id>/fulfill', methods=['POST'])
def fulfill_line_item(order_id, line_item_id):
    """Fulfill a specific line item"""
    order = SalesOrder.query.get_or_404(order_id)
    line_item = OrderLineItem.query.filter_by(id=line_item_id, order_id=order_id).first_or_404()
    
    if order.status != 'issued':
        return jsonify({'error': 'Order must be issued before fulfillment'}), 400
    
    data = request.get_json()
    fulfill_quantity = data.get('quantity', line_item.quantity)
    
    if fulfill_quantity > (line_item.quantity - line_item.fulfilled_quantity):
        return jsonify({'error': 'Cannot fulfill more than remaining quantity'}), 400
    
    try:
        line_item.fulfilled_quantity += fulfill_quantity
        
        if line_item.fulfilled_quantity == line_item.quantity:
            line_item.fulfillment_status = 'fulfilled'
        elif line_item.fulfilled_quantity > 0:
            line_item.fulfillment_status = 'partially_fulfilled'
        
        # Check if all line items are fulfilled
        all_fulfilled = all(item.fulfillment_status == 'fulfilled' for item in order.line_items)
        if all_fulfilled:
            order.status = 'complete'
        
        db.session.commit()
        return jsonify(order.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

