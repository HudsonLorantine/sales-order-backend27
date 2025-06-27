from flask import Blueprint, request, jsonify
from src.models.database import db, Customer, Product
from datetime import datetime
import uuid

quotes_bp = Blueprint('quotes', __name__)

# In-memory storage for quotes (since no Quote model exists yet)
quotes_storage = []
quote_counter = 1

def generate_quote_number():
    """Generate a unique quote number"""
    return f"QT-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

@quotes_bp.route('/quotes', methods=['GET'])
def get_quotes():
    """Get all quotes with optional filtering"""
    status = request.args.get('status')
    customer_id = request.args.get('customer_id')
    
    filtered_quotes = quotes_storage
    if status:
        filtered_quotes = [q for q in filtered_quotes if q.get('status') == status]
    if customer_id:
        filtered_quotes = [q for q in filtered_quotes if q.get('customer_id') == int(customer_id)]
    
    return jsonify(filtered_quotes)

@quotes_bp.route('/quotes', methods=['POST'])
def create_quote():
    """Create a new quote"""
    global quote_counter
    data = request.get_json()
    
    if not data or not data.get('customer_id') or not data.get('items'):
        return jsonify({'error': 'Customer ID and items are required'}), 400
    
    # Verify customer exists
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    # Calculate totals
    subtotal = 0
    processed_items = []
    
    for item_data in data['items']:
        product = Product.query.get(item_data['product_id'])
        if not product:
            return jsonify({'error': f'Product {item_data["product_id"]} not found'}), 404
        
        quantity = item_data['quantity']
        unit_price = item_data.get('unit_price', float(product.unit_price))
        line_total = quantity * unit_price
        
        processed_items.append({
            'id': len(processed_items) + 1,
            'product_id': product.id,
            'product_name': product.product_name,
            'quantity': quantity,
            'unit_price': unit_price,
            'line_total': line_total
        })
        
        subtotal += line_total
    
    tax_rate = data.get('tax_rate', 0.0)
    tax_amount = subtotal * (tax_rate / 100)
    total_amount = subtotal + tax_amount
    
    quote = {
        'id': quote_counter,
        'quote_number': generate_quote_number(),
        'customer_id': data['customer_id'],
        'customer': customer.to_dict(),
        'quote_date': datetime.now().isoformat(),
        'expiry_date': data.get('expiry_date'),
        'status': 'draft',
        'subtotal': round(subtotal, 2),
        'tax_rate': tax_rate,
        'tax_amount': round(tax_amount, 2),
        'total_amount': round(total_amount, 2),
        'notes': data.get('notes'),
        'items': processed_items,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    quotes_storage.append(quote)
    quote_counter += 1
    
    return jsonify(quote), 201

@quotes_bp.route('/quotes/<int:quote_id>', methods=['GET'])
def get_quote(quote_id):
    """Get a specific quote"""
    quote = next((q for q in quotes_storage if q['id'] == quote_id), None)
    if not quote:
        return jsonify({'error': 'Quote not found'}), 404
    return jsonify(quote)

@quotes_bp.route('/quotes/<int:quote_id>', methods=['PUT'])
def update_quote(quote_id):
    """Update a quote (only if draft)"""
    quote = next((q for q in quotes_storage if q['id'] == quote_id), None)
    if not quote:
        return jsonify({'error': 'Quote not found'}), 404
    
    if quote['status'] != 'draft':
        return jsonify({'error': 'Can only edit draft quotes'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update basic fields
    quote['notes'] = data.get('notes', quote['notes'])
    quote['expiry_date'] = data.get('expiry_date', quote['expiry_date'])
    quote['updated_at'] = datetime.now().isoformat()
    
    return jsonify(quote)

@quotes_bp.route('/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    """Delete a quote"""
    global quotes_storage
    quote = next((q for q in quotes_storage if q['id'] == quote_id), None)
    if not quote:
        return jsonify({'error': 'Quote not found'}), 404
    
    quotes_storage = [q for q in quotes_storage if q['id'] != quote_id]
    return jsonify({'message': 'Quote deleted successfully'})

@quotes_bp.route('/quotes/<int:quote_id>/convert', methods=['POST'])
def convert_quote_to_order(quote_id):
    """Convert a quote to an order"""
    quote = next((q for q in quotes_storage if q['id'] == quote_id), None)
    if not quote:
        return jsonify({'error': 'Quote not found'}), 404
    
    if quote['status'] != 'accepted':
        return jsonify({'error': 'Quote must be accepted before conversion'}), 400
    
    # This would create an actual order - for now just return success
    quote['status'] = 'converted'
    quote['updated_at'] = datetime.now().isoformat()
    
    return jsonify({
        'message': 'Quote converted to order successfully',
        'order_id': 999  # Mock order ID
    })
