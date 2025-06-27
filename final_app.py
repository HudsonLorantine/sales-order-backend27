import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Sales API is running!"})

@app.route('/api/orders')
def orders():
    data = [
        {"id": 1, "customer": "Test Customer", "total": 100.00},
        {"id": 2, "customer": "Another Customer", "total": 250.00}
    ]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
