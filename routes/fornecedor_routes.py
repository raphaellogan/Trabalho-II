from flask import Blueprint, request, jsonify

from models.fornecedor import (
    criar_fornecedor,
    listar_fornecedores,
    buscar_fornecedor_por_id,
    alterar_fornecedor,
    deletar_fornecedor
)

fornecedor_bp = Blueprint("fornecedor", __name__)


@fornecedor_bp.route("/fornecedores", methods=["POST"])
def cadastrar():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Dados do fornecedor não foram enviados"}), 400

    nome = dados.get("nome")
    cnpj = dados.get("cnpj")
    telefone = dados.get("telefone")
    email = dados.get("email")

    if not nome or not cnpj:
        return jsonify({"erro": "Nome e CNPJ são obrigatórios"}), 400

    criar_fornecedor(nome, cnpj, telefone, email)

    return jsonify({"mensagem": "Fornecedor cadastrado com sucesso"}), 201


@fornecedor_bp.route("/fornecedores", methods=["GET"])
def listar():
    fornecedores = listar_fornecedores()
    return jsonify(fornecedores), 200


@fornecedor_bp.route("/fornecedores/<int:id_fornecedor>", methods=["GET"])
def buscar(id_fornecedor):
    fornecedor = buscar_fornecedor_por_id(id_fornecedor)

    if fornecedor is None:
        return jsonify({"erro": "Fornecedor não encontrado"}), 404

    return jsonify(fornecedor), 200


@fornecedor_bp.route("/fornecedores/<int:id_fornecedor>", methods=["PUT"])
def alterar(id_fornecedor):
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Dados do fornecedor não foram enviados"}), 400

    resultado = alterar_fornecedor(id_fornecedor, dados)

    if resultado == 0:
        return jsonify({"erro": "Fornecedor não encontrado ou nenhum campo foi alterado"}), 404

    return jsonify({"mensagem": "Fornecedor alterado com sucesso"}), 200


@fornecedor_bp.route("/fornecedores/<int:id_fornecedor>", methods=["DELETE"])
def deletar(id_fornecedor):
    resultado = deletar_fornecedor(id_fornecedor)

    if resultado == 0:
        return jsonify({"erro": "Fornecedor não encontrado"}), 404

    return jsonify({"mensagem": "Fornecedor removido com sucesso"}), 200