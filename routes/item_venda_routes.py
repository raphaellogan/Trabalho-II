from flask import Blueprint, request, jsonify

from models.item_venda import (
    cadastrar_item_venda,
    listar_itens_venda,
    buscar_item_venda,
    alterar_item_venda,
    excluir_item_venda
)


# ==========================================
# BLUEPRINT ITEM VENDA
# ==========================================

item_venda_bp = Blueprint("item_venda", __name__)


# ==========================================
# CADASTRAR ITEM DA VENDA - POST
# ==========================================

@item_venda_bp.route("/item_venda", methods=["POST"])
def cadastrar():

    dados = request.get_json()

    if not dados:
        return jsonify({
            "erro": "Envie os dados em formato JSON"
        }), 400

    id_venda = dados.get("id_venda")
    id_produto = dados.get("id_produto")
    quantidade = dados.get("quantidade")
    preco_unitario = dados.get("preco_unitario")

    if (
        id_venda is None
        or id_produto is None
        or quantidade is None
        or preco_unitario is None
    ):
        return jsonify({
            "erro": "Todos os campos são obrigatórios"
        }), 400

    try:

        id_item = cadastrar_item_venda(
            id_venda,
            id_produto,
            quantidade,
            preco_unitario
        )

        return jsonify({
            "mensagem": "Item da venda cadastrado com sucesso!",
            "id_item": id_item
        }), 201

    except Exception as erro:

        return jsonify({
            "erro": str(erro)
        }), 500


# ==========================================
# LISTAR TODOS OS ITENS DA VENDA - GET
# ==========================================

@item_venda_bp.route("/item_venda", methods=["GET"])
def listar():

    try:

        itens = listar_itens_venda()

        return jsonify(itens), 200

    except Exception as erro:

        return jsonify({
            "erro": str(erro)
        }), 500


# ==========================================
# BUSCAR ITEM DA VENDA POR ID - GET
# ==========================================

@item_venda_bp.route("/item_venda/<int:id_item>", methods=["GET"])
def buscar(id_item):

    try:

        item = buscar_item_venda(id_item)

        if not item:
            return jsonify({
                "erro": "Item da venda não encontrado"
            }), 404

        return jsonify(item), 200

    except Exception as erro:

        return jsonify({
            "erro": str(erro)
        }), 500


# ==========================================
# ALTERAR ITEM DA VENDA - PUT
# ==========================================

@item_venda_bp.route("/item_venda/<int:id_item>", methods=["PUT"])
def alterar(id_item):

    dados = request.get_json()

    if not dados:
        return jsonify({
            "erro": "Envie os dados em formato JSON"
        }), 400

    id_produto = dados.get("id_produto")
    quantidade = dados.get("quantidade")
    preco_unitario = dados.get("preco_unitario")

    if (
        id_produto is None
        or quantidade is None
        or preco_unitario is None
    ):
        return jsonify({
            "erro": "Todos os campos são obrigatórios"
        }), 400

    try:

        resultado = alterar_item_venda(
            id_item,
            id_produto,
            quantidade,
            preco_unitario
        )

        if resultado == 0:
            return jsonify({
                "erro": "Item da venda não encontrado"
            }), 404

        return jsonify({
            "mensagem": "Item da venda alterado com sucesso!"
        }), 200

    except Exception as erro:

        return jsonify({
            "erro": str(erro)
        }), 500


# ==========================================
# EXCLUIR ITEM DA VENDA - DELETE
# ==========================================

@item_venda_bp.route("/item_venda/<int:id_item>", methods=["DELETE"])
def excluir(id_item):

    try:

        resultado = excluir_item_venda(id_item)

        if resultado == 0:
            return jsonify({
                "erro": "Item da venda não encontrado"
            }), 404

        return jsonify({
            "mensagem": "Item da venda excluído com sucesso!"
        }), 200

    except Exception as erro:

        return jsonify({
            "erro": str(erro)
        }), 500