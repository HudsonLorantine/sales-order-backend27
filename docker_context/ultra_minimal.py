import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Ultra minimal API is running"})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/orders', methods=['GET'])
def orders():
    # Simple mock data
    data = [
        {"id": 1, "customer": "Test Customer", "total": 100.00},
        {"id": 2, "customer": "Another Customer", "total": 250.00}
    ]
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
