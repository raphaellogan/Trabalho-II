from datetime import datetime

from flask import Flask, render_template

from models.cliente import listar_clientes
from models.categoria import listar_categorias
from models.fornecedor import listar_fornecedores
from models.produto import listar_produtos
from models.venda import listar_vendas

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


def format_money(value):
    valor = float(value or 0)
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def get_saudacao():
    hora = datetime.now().hour

    if 6 <= hora <= 11:
        return "Bom dia"
    if 12 <= hora <= 17:
        return "Boa tarde"
    return "Boa noite"


@app.route("/")
def index():
    produtos = listar_produtos()
    clientes = listar_clientes()
    vendas = listar_vendas()
    categorias = listar_categorias()
    fornecedores = listar_fornecedores()

    low_stock = [
        item for item in produtos
        if int(item.get("estoque") or 0) <= 5
    ][:4]

    vendas_ordenadas = sorted(
        vendas,
        key=lambda item: item.get("data_venda") or "0000-00-00",
        reverse=True
    )
    recent_sales = vendas_ordenadas[:5]
    total_estoque = sum(int(item.get("estoque") or 0) for item in produtos)
    receita_total = sum(float(item.get("valor_total") or 0) for item in vendas)

    return render_template(
        "index.html",
        produtos=produtos,
        clientes=clientes,
        vendas=vendas,
        categorias=categorias,
        fornecedores=fornecedores,
        low_stock=low_stock,
        recent_sales=recent_sales,
        total_estoque=total_estoque,
        metric_revenue=format_money(receita_total),
        produtos_json=produtos,
        saudacao=get_saudacao()
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)