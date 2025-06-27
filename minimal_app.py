import os
import sys
import socket
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

# Debug startup information
print(f"Starting Flask application at {datetime.now().isoformat()}")
print(f"Python version: {sys.version}")
print(f"Environment variables: {dict(os.environ)}")

@app.route('/')
def home():
    return jsonify({
        "message": "Sales Order API is running!",
        "timestamp": datetime.now().isoformat(),
        "environment": "container"
    })

@app.route('/api/health')
def health():
    # Return detailed system information for debugging
    hostname = socket.gethostname()
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "python_version": sys.version,
        "hostname": hostname,
        "ip": socket.gethostbyname(hostname),
        "environment": dict([(k, v) for k, v in os.environ.items() if not k.startswith('PATH')])
    })

@app.route('/api/orders')
def get_orders():
    # Sample mock data
    orders = [
        {"id": 1, "customer": "Test Customer", "total": 100.00, "status": "Pending"},
        {"id": 2, "customer": "Another Customer", "total": 250.00, "status": "Completed"}
    ]
    return jsonify(orders)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
