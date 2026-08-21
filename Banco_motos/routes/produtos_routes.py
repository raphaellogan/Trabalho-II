from flask import Blueprint, request, jsonify
from Banco_motos.models.produto import cadastrar_produto, listar_produtos


produto_bp = Blueprint("produto", __name__)


@produto_bp.route("/produtos", methods=["POST"])
def cadastrar():
    dados = request.get_json()

    nome = dados.get("nome")
    descricao = dados.get("descricao")
    preco = dados.get("preco")
    estoque = dados.get("estoque")
    id_categoria = dados.get("id_categoria")
    id_fornecedor = dados.get("id_fornecedor")
    tamanho = dados.get("tamanho")
    codigo_de_barra = dados.get("codigo_de_barra")

    if not nome or preco is None or estoque is None:
        return jsonify({
            "erro": "Nome, preço e estoque são obrigatórios"
        }), 400

    cadastrar_produto(
        nome,
        descricao,
        preco,
        estoque,
        id_categoria,
        id_fornecedor,
        tamanho,
        codigo_de_barra
    )

    return jsonify({
        "mensagem": "Produto cadastrado com sucesso"
    }), 201


@produto_bp.route("/produtos", methods=["GET"])
def listar():
    produtos = listar_produtos()

    return jsonify(produtos)