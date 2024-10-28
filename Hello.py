from flask import Flask, jsonify
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"


@app.route("/products")
def products():
    response = jsonify([
        {
            "title": "Caneca Personalizada de Porcelana Do Backend",
            "amount": 123.45,
            "installments": {"number": 3, "total": 41.15, "hasFree": True},
        },
        {
            "title": "Caneca de tulipa",
            "amount": 789.45,
            "installments": {"number": 6, "total": 41.15},
        }
    ])

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
