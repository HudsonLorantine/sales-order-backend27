import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.models.database import db
from src.models.user import bcrypt
from src.routes.auth import auth_bp
from src.routes.customers import customers_bp
from src.routes.products import products_bp
from src.routes.orders import orders_bp
from src.routes.payments import payments_bp
from src.routes.quotes import quotes_bp
from src.routes.invoices import invoices_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app, origins=[
    "http://localhost:5173",  # for local development
    "https://brave-coast-082fed100.2.azurestaticapps.net",  # old frontend
    "https://red-smoke-0b599251e.1.azurestaticapps.net"  # new v1.1 frontend
])

# Register blueprints
app.register_blueprint(customers_bp, url_prefix='/api')
app.register_blueprint(products_bp, url_prefix='/api')
app.register_blueprint(orders_bp, url_prefix='/api')
app.register_blueprint(payments_bp, url_prefix='/api')
app.register_blueprint(quotes_bp, url_prefix='/api')
app.register_blueprint(invoices_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
bcrypt.init_app(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in your production environment!
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

@app.route('/api/dashboard/stats')
def get_dashboard_stats():
    """Get dashboard statistics"""
    from flask import jsonify
    from src.models.database import Customer, Product, SalesOrder
    
    try:
        total_customers = Customer.query.count()
        total_products = Product.query.count()
        total_orders = SalesOrder.query.count()
        
        # Calculate total revenue
        orders = SalesOrder.query.all()
        total_revenue = sum([float(order.total_amount) for order in orders])
        
        return jsonify({
            'total_customers': total_customers,
            'total_products': total_products,
            'total_orders': total_orders,
            'total_revenue': total_revenue
        })
    except Exception as e:
        return jsonify({
            'total_customers': 0,
            'total_products': 0,
            'total_orders': 0,
            'total_revenue': 0.0
        })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

