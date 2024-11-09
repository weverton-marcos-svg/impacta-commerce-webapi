# Inicializa a aplicação  com configurações padrão
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Inicializa a conexão com um banco de dados SQLite em memória
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)


# Cria a entidade de produto
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    amount = db.Column(db.Numeric,  unique=False, nullable=False)
    installments = db.Column(db.Integer, unique=False, nullable=False)
    installments_free = db.Column(db.Boolean, unique=False, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.title

    @property
    def serialized(self):
        return {
            'id': self.id,
            'title': self.title,
            'amount': round(self.amount, 2),
            'installments': {
                "number": self.installments,
                "total": round(self.amount / self.installments, 2)
            }
        }


# Cria o banco de dados em memória
with app.app_context():
    db.create_all()

    # Cria dois produtos
    product1 = Product(
        title="Caneca Personalizada de Porcelana", amount=123.45,
        installments=3, installments_free=False
    )
    product2 = Product(
        title="Caneca de Tulipa", amount=123.45,
        installments=3, installments_free=False
    )

    # Insere os dois produtos no banco de dadso em memória
    db.session.add(product1)
    db.session.add(product2)

    # Commit da transaction do banco de dados
    db.session.commit()


# Cria uma rota para consulta de produtos baseada no parâmetro query.
@app.route("/products", methods=['GET'])
def get_products():
    args = request.args.to_dict()
    query = args.get("query")

    if query is None:
        all_products = Product.query.all()
    else:
        all_products = Product.query.filter(
            Product.title.like(f'%{query}%')).all()

    return jsonify({
        'query': query,
        'size': 10,
        'start': 'MA==',
        'results': [p.serialized for p in all_products],
    })
