from flask import Blueprint, request, jsonify
from src.models.database import db, Payment, SalesOrder
from decimal import Decimal

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/orders/<int:order_id>/payments', methods=['GET'])
def get_order_payments(order_id):
    """Get all payments for a specific order"""
    order = SalesOrder.query.get_or_404(order_id)
    payments = Payment.query.filter_by(order_id=order_id).all()
    return jsonify([payment.to_dict() for payment in payments])

@payments_bp.route('/orders/<int:order_id>/payments', methods=['POST'])
def record_payment(order_id):
    """Record a payment for an order"""
    order = SalesOrder.query.get_or_404(order_id)
    data = request.get_json()
    
    if not data or not data.get('payment_amount'):
        return jsonify({'error': 'Payment amount is required'}), 400
    
    payment_amount = Decimal(str(data['payment_amount']))
    
    # Calculate total payments so far
    existing_payments = Payment.query.filter_by(order_id=order_id).all()
    total_paid = sum(Decimal(str(p.payment_amount)) for p in existing_payments)
    
    # Check if payment amount is valid
    if total_paid + payment_amount > order.total_amount:
        return jsonify({'error': 'Payment amount exceeds order total'}), 400
    
    payment = Payment(
        order_id=order_id,
        payment_amount=payment_amount,
        payment_method=data.get('payment_method'),
        reference_number=data.get('reference_number')
    )
    
    try:
        db.session.add(payment)
        
        # Update order payment status
        new_total_paid = total_paid + payment_amount
        if new_total_paid >= order.total_amount:
            order.payment_status = 'paid'
        elif new_total_paid > 0:
            order.payment_status = 'partial'
        else:
            order.payment_status = 'unpaid'
        
        db.session.commit()
        return jsonify(payment.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    """Get a specific payment"""
    payment = Payment.query.get_or_404(payment_id)
    return jsonify(payment.to_dict())

@payments_bp.route('/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    """Delete a payment"""
    payment = Payment.query.get_or_404(payment_id)
    order = payment.order
    
    try:
        db.session.delete(payment)
        
        # Recalculate payment status
        remaining_payments = Payment.query.filter_by(order_id=order.id).filter(Payment.id != payment_id).all()
        total_paid = sum(Decimal(str(p.payment_amount)) for p in remaining_payments)
        
        if total_paid >= order.total_amount:
            order.payment_status = 'paid'
        elif total_paid > 0:
            order.payment_status = 'partial'
        else:
            order.payment_status = 'unpaid'
        
        db.session.commit()
        return jsonify({'message': 'Payment deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

