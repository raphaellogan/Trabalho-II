from flask import Blueprint, request, jsonify

from models.produto import (
    cadastrar_produto,
    listar_produtos,
    buscar_produto,
    alterar_produto
)


produto_bp = Blueprint("produto", __name__)


@produto_bp.route("/produtos", methods=["POST"])
def cadastrar():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Dados do produto não foram enviados"}), 400

    nome = dados.get("nome")
    descricao = dados.get("descricao")
    preco = dados.get("preco")
    estoque = dados.get("estoque")
    id_categoria = dados.get("id_categoria")
    id_fornecedor = dados.get("id_fornecedor")
    cor = dados.get("cor")
    tamanho = dados.get("tamanho")
    codigo_de_barra = dados.get("codigo_de_barra")

    if not nome or preco is None or estoque is None or not codigo_de_barra:
        return jsonify({
            "erro": "Nome, preço, estoque e código de barras são obrigatórios"
        }), 400

    try:
        cadastrar_produto(
            nome,
            descricao or "",
            preco,
            estoque,
            id_categoria,
            id_fornecedor,
            cor,
            tamanho,
            codigo_de_barra
        )
        return jsonify({"mensagem": "Produto cadastrado com sucesso"}), 201
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 400


@produto_bp.route("/produtos", methods=["GET"])
def listar():
    produtos = listar_produtos()
    return jsonify(produtos), 200


@produto_bp.route("/produtos/<int:id_produto>", methods=["GET"])
def buscar(id_produto):
    produto = buscar_produto(id_produto)

    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404

    return jsonify(produto), 200


@produto_bp.route("/produtos/<int:id_produto>", methods=["PUT"])
def alterar(id_produto):
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Dados do produto não foram enviados"}), 400

    resultado = alterar_produto(id_produto, dados)

    if resultado == 0:
        return jsonify({"erro": "Produto não encontrado ou nenhum campo foi alterado"}), 404

    return jsonify({"mensagem": "Produto alterado com sucesso"}), 200