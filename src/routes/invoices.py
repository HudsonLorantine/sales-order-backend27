from flask import Blueprint, request, jsonify
from src.models.database import db, Customer, Product
from datetime import datetime, timedelta
import uuid

invoices_bp = Blueprint('invoices', __name__)

# In-memory storage for invoices (since no Invoice model exists yet)
invoices_storage = []
invoice_counter = 1

def generate_invoice_number():
    """Generate a unique invoice number"""
    return f"INV-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

@invoices_bp.route('/invoices', methods=['GET'])
def get_invoices():
    """Get all invoices with optional filtering"""
    status = request.args.get('status')
    customer_id = request.args.get('customer_id')
    
    filtered_invoices = invoices_storage
    if status:
        filtered_invoices = [i for i in filtered_invoices if i.get('status') == status]
    if customer_id:
        filtered_invoices = [i for i in filtered_invoices if i.get('customer_id') == int(customer_id)]
    
    return jsonify(filtered_invoices)

@invoices_bp.route('/invoices', methods=['POST'])
def create_invoice():
    """Create a new invoice"""
    global invoice_counter
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
    
    # Calculate due date
    payment_terms = data.get('payment_terms', 30)  # Default 30 days
    due_date = datetime.now() + timedelta(days=payment_terms)
    
    invoice = {
        'id': invoice_counter,
        'invoice_number': generate_invoice_number(),
        'customer_id': data['customer_id'],
        'customer': customer.to_dict(),
        'invoice_date': datetime.now().isoformat(),
        'due_date': due_date.isoformat(),
        'payment_terms': payment_terms,
        'status': 'sent',
        'payment_status': 'unpaid',
        'subtotal': round(subtotal, 2),
        'tax_rate': tax_rate,
        'tax_amount': round(tax_amount, 2),
        'total_amount': round(total_amount, 2),
        'paid_amount': 0.0,
        'balance_due': round(total_amount, 2),
        'notes': data.get('notes'),
        'items': processed_items,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    invoices_storage.append(invoice)
    invoice_counter += 1
    
    return jsonify(invoice), 201

@invoices_bp.route('/invoices/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    """Get a specific invoice"""
    invoice = next((i for i in invoices_storage if i['id'] == invoice_id), None)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404
    return jsonify(invoice)

@invoices_bp.route('/invoices/<int:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    """Update an invoice (only if draft)"""
    invoice = next((i for i in invoices_storage if i['id'] == invoice_id), None)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404
    
    if invoice['status'] not in ['draft', 'sent']:
        return jsonify({'error': 'Can only edit draft or sent invoices'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update basic fields
    invoice['notes'] = data.get('notes', invoice['notes'])
    if 'payment_terms' in data:
        invoice['payment_terms'] = data['payment_terms']
        # Recalculate due date
        invoice_date = datetime.fromisoformat(invoice['invoice_date'])
        due_date = invoice_date + timedelta(days=data['payment_terms'])
        invoice['due_date'] = due_date.isoformat()
    
    invoice['updated_at'] = datetime.now().isoformat()
    
    return jsonify(invoice)

@invoices_bp.route('/invoices/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    """Delete an invoice"""
    global invoices_storage
    invoice = next((i for i in invoices_storage if i['id'] == invoice_id), None)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404
    
    if invoice['payment_status'] == 'paid':
        return jsonify({'error': 'Cannot delete paid invoices'}), 400
    
    invoices_storage = [i for i in invoices_storage if i['id'] != invoice_id]
    return jsonify({'message': 'Invoice deleted successfully'})

@invoices_bp.route('/invoices/<int:invoice_id>/payment', methods=['POST'])
def record_payment(invoice_id):
    """Record a payment for an invoice"""
    invoice = next((i for i in invoices_storage if i['id'] == invoice_id), None)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404
    
    data = request.get_json()
    if not data or not data.get('amount'):
        return jsonify({'error': 'Payment amount is required'}), 400
    
    payment_amount = float(data['amount'])
    if payment_amount <= 0:
        return jsonify({'error': 'Payment amount must be positive'}), 400
    
    if payment_amount > invoice['balance_due']:
        return jsonify({'error': 'Payment amount exceeds balance due'}), 400
    
    # Update payment information
    invoice['paid_amount'] += payment_amount
    invoice['balance_due'] = invoice['total_amount'] - invoice['paid_amount']
    
    # Update payment status
    if invoice['balance_due'] <= 0:
        invoice['payment_status'] = 'paid'
        invoice['status'] = 'paid'
    elif invoice['paid_amount'] > 0:
        invoice['payment_status'] = 'partial'
    
    invoice['updated_at'] = datetime.now().isoformat()
    
    return jsonify({
        'message': 'Payment recorded successfully',
        'invoice': invoice,
        'payment': {
            'amount': payment_amount,
            'date': datetime.now().isoformat(),
            'method': data.get('method', 'unknown')
        }
    })

@invoices_bp.route('/invoices/<int:invoice_id>/send', methods=['POST'])
def send_invoice(invoice_id):
    """Send an invoice to customer"""
    invoice = next((i for i in invoices_storage if i['id'] == invoice_id), None)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404
    
    invoice['status'] = 'sent'
    invoice['updated_at'] = datetime.now().isoformat()
    
    return jsonify({
        'message': 'Invoice sent successfully',
        'invoice': invoice
    })
