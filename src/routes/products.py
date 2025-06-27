from flask import Blueprint, request, jsonify
from src.models.database import db, Product

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    """Get all products with optional search"""
    search = request.args.get('search', '')
    
    query = Product.query
    if search:
        query = query.filter(
            Product.product_name.contains(search) |
            Product.sku.contains(search) |
            Product.description.contains(search)
        )
    
    products = query.all()
    return jsonify({'products': [product.to_dict() for product in products]})

@products_bp.route('/products', methods=['POST'])
def create_product():
    """Create a new product"""
    data = request.get_json()
    
    if not data or not data.get('sku') or not data.get('name') or not data.get('price'):
        return jsonify({'error': 'SKU, product name, and unit price are required'}), 400
    
    # Check if SKU already exists
    existing_product = Product.query.filter_by(sku=data['sku']).first()
    if existing_product:
        return jsonify({'error': 'Product with this SKU already exists'}), 400
    
    product = Product(
        sku=data['sku'],
        product_name=data['name'],
        description=data.get('description'),
        unit_price=data['price'],
        inventory_quantity=data.get('stock_quantity', 0)
    )
    
    try:
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product"""
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@products_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product"""
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Check if SKU is being changed and if it already exists
    if 'sku' in data and data['sku'] != product.sku:
        existing_product = Product.query.filter_by(sku=data['sku']).first()
        if existing_product:
            return jsonify({'error': 'Product with this SKU already exists'}), 400
    
    product.sku = data.get('sku', product.sku)
    product.product_name = data.get('product_name', product.product_name)
    product.description = data.get('description', product.description)
    product.unit_price = data.get('unit_price', product.unit_price)
    product.inventory_quantity = data.get('inventory_quantity', product.inventory_quantity)
    
    try:
        db.session.commit()
        return jsonify(product.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    product = Product.query.get_or_404(product_id)
    
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@products_bp.route('/products/<int:product_id>/inventory', methods=['PUT'])
def update_inventory(product_id):
    """Update product inventory quantity"""
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    if not data or 'quantity' not in data:
        return jsonify({'error': 'Quantity is required'}), 400
    
    product.inventory_quantity = data['quantity']
    
    try:
        db.session.commit()
        return jsonify(product.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

