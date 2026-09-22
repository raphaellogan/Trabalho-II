from flask import Blueprint, request, jsonify

from models.venda import (
    cadastrar_venda,
    listar_vendas,
    buscar_venda_por_id,
    alterar_venda,
    excluir_venda
)

venda_bp = Blueprint("venda", __name__)


@venda_bp.route("/vendas", methods=["POST"])
def cadastrar():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Dados da venda não foram enviados"}), 400

    data_venda = dados.get("data_venda")
    valor_total = dados.get("valor_total")
    id_cliente = dados.get("id_cliente")

    if not data_venda or valor_total is None or not id_cliente:
        return jsonify({"erro": "Data da venda, valor total e cliente são obrigatórios"}), 400

    try:
        id_venda = cadastrar_venda(data_venda, valor_total, id_cliente)
        return jsonify({"mensagem": "Venda cadastrada com sucesso", "id_venda": id_venda}), 201
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 400


@venda_bp.route("/vendas", methods=["GET"])
def listar():
    try:
        vendas = listar_vendas()
        return jsonify(vendas), 200
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 400


@venda_bp.route("/vendas/<int:id_venda>", methods=["GET"])
def buscar(id_venda):
    try:
        venda = buscar_venda_por_id(id_venda)

        if venda is None:
            return jsonify({"erro": "Venda não encontrada"}), 404

        return jsonify(venda), 200
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 400


@venda_bp.route("/vendas/<int:id_venda>", methods=["PUT"])
def alterar(id_venda):
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Dados da venda não foram enviados"}), 400

    data_venda = dados.get("data_venda")
    valor_total = dados.get("valor_total")
    id_cliente = dados.get("id_cliente")

    if not data_venda or valor_total is None or not id_cliente:
        return jsonify({"erro": "Data da venda, valor total e cliente são obrigatórios"}), 400

    try:
        resultado = alterar_venda(id_venda, data_venda, valor_total, id_cliente)

        if resultado == 0:
            return jsonify({"erro": "Venda não encontrada"}), 404

        return jsonify({"mensagem": "Venda alterada com sucesso"}), 200
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 400


@venda_bp.route("/vendas/<int:id_venda>", methods=["DELETE"])
def excluir(id_venda):
    try:
        resultado = excluir_venda(id_venda)

        if resultado == 0:
            return jsonify({"erro": "Venda não encontrada"}), 404

        return jsonify({"mensagem": "Venda cancelada com sucesso"}), 200
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 400