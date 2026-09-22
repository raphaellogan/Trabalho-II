from flask import Blueprint, request, jsonify

from models.cliente import (
    criar_cliente,
    listar_clientes,
    buscar_cliente_por_id,
    atualizar_cliente,
    cancelar_cliente
)

cliente_bp = Blueprint("cliente", __name__)


@cliente_bp.route("/clientes", methods=["POST"])
def cadastrar():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Dados do cliente não foram enviados"}), 400

    nome = dados.get("nome")
    cpf = dados.get("cpf")
    telefone = dados.get("telefone")
    email = dados.get("email")
    endereco = dados.get("endereco")
    aceite_lgpd = dados.get("aceite_lgpd")
    data_consentimento = dados.get("data_consentimento")

    if not nome or not cpf:
        return jsonify({"erro": "Nome e CPF são obrigatórios"}), 400

    criar_cliente(
        nome,
        cpf,
        telefone,
        email,
        endereco,
        aceite_lgpd,
        data_consentimento
    )

    return jsonify({"mensagem": "Cliente cadastrado com sucesso"}), 201


@cliente_bp.route("/clientes", methods=["GET"])
def listar():
    clientes = listar_clientes()
    return jsonify(clientes), 200


@cliente_bp.route("/clientes/<int:id_cliente>", methods=["GET"])
def buscar_por_id(id_cliente):
    cliente = buscar_cliente_por_id(id_cliente)

    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    return jsonify(cliente), 200


@cliente_bp.route("/clientes/<int:id_cliente>", methods=["PUT"])
def atualizar(id_cliente):
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Dados do cliente não foram enviados"}), 400

    resultado = atualizar_cliente(id_cliente, dados)

    if resultado == 0:
        return jsonify({"erro": "Cliente não encontrado ou nenhum campo foi alterado"}), 404

    return jsonify({"mensagem": "Cliente alterado com sucesso"}), 200


@cliente_bp.route("/clientes/<int:id_cliente>", methods=["DELETE"])
def cancelar(id_cliente):
    resultado = cancelar_cliente(id_cliente)

    if resultado == 0:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    return jsonify({"mensagem": "Cliente removido com sucesso"}), 200
