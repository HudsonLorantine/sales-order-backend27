import azure.functions as func
import json

app = func.FunctionApp()

@app.route(route="api")
def hello(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"message": "Sales API is running!"}),
        mimetype="application/json"
    )

@app.route(route="api/orders")
def orders(req: func.HttpRequest) -> func.HttpResponse:
    data = [
        {"id": 1, "customer": "Test Customer", "total": 100.00},
        {"id": 2, "customer": "Another Customer", "total": 250.00}
    ]
    return func.HttpResponse(
        json.dumps(data),
        mimetype="application/json"
    )
