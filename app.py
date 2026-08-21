from flask import Flask

from routes.cliente_routes import cliente_bp
from routes.categoria_routes import categoria_bp
from routes.fornecedor_routes import fornecedor_bp
from routes.produtos_routes import produto_bp
from routes.venda_routes import venda_bp
from routes.item_venda_routes import item_venda_bp


app = Flask(__name__)


app.register_blueprint(cliente_bp)
app.register_blueprint(categoria_bp)
app.register_blueprint(fornecedor_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(venda_bp)
app.register_blueprint(item_venda_bp)


@app.route("/")
def index():
    return "API funcionando!"


if __name__ == "__main__":
    app.run(debug=True)