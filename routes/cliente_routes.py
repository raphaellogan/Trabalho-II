from flask import Blueprint, request, jsonify

from models.cliente import (
    criar_cliente,
    listar_clientes,
    buscar_cliente_por_id,
    buscar_cliente_por_cpf,
    atualizar_cliente,
    cancelar_cliente
)


cliente_bp = Blueprint("cliente", __name__)


# =========================================
# CADASTRAR CLIENTE
# =========================================

@cliente_bp.route("/clientes", methods=["POST"])
def cadastrar():

    dados = request.get_json()

    nome = dados.get("nome")
    cpf = dados.get("cpf")
    telefone = dados.get("telefone")
    email = dados.get("email")
    endereco = dados.get("endereco")
    aceite_lgpd = dados.get("aceite_lgpd")

    if not nome or not cpf:
        return jsonify({
            "erro": "Nome e CPF são obrigatórios"
        }), 400

    if aceite_lgpd is None:
        return jsonify({
            "erro": "É necessário informar se o cliente aceitou a LGPD"
        }), 400

    # Verifica se o CPF já existe
    cliente_existente = buscar_cliente_por_cpf(cpf)

    if cliente_existente:
        return jsonify({
            "erro": "Cliente já cadastrado com este CPF"
        }), 409

    criar_cliente(
        nome,
        cpf,
        telefone,
        email,
        endereco,
        aceite_lgpd
    )

    return jsonify({
        "mensagem": "Cliente cadastrado com sucesso"
    }), 201


# =========================================
# LISTAR CLIENTES
# =========================================

@cliente_bp.route("/clientes", methods=["GET"])
def listar():

    clientes = listar_clientes()

    return jsonify(clientes), 200


# =========================================
# BUSCAR CLIENTE POR ID
# =========================================

@cliente_bp.route("/clientes/<int:id_cliente>", methods=["GET"])
def buscar_por_id(id_cliente):

    cliente = buscar_cliente_por_id(id_cliente)

    if not cliente:
        return jsonify({
            "erro": "Cliente não encontrado"
        }), 404

    return jsonify(cliente), 200


# =========================================
# ALTERAR CLIENTE
# =========================================

@cliente_bp.route("/clientes/<int:id_cliente>", methods=["PUT"])
def alterar(id_cliente):

    cliente = buscar_cliente_por_id(id_cliente)

    if not cliente:
        return jsonify({
            "erro": "Cliente não encontrado"
        }), 404

    dados = request.get_json()

    nome = dados.get("nome")
    cpf = dados.get("cpf")
    telefone = dados.get("telefone")
    email = dados.get("email")
    endereco = dados.get("endereco")
    aceite_lgpd = dados.get("aceite_lgpd")

    if not nome or not cpf:
        return jsonify({
            "erro": "Nome e CPF são obrigatórios"
        }), 400

    if aceite_lgpd is None:
        return jsonify({
            "erro": "É necessário informar se o cliente aceitou a LGPD"
        }), 400

    # Verifica se o novo CPF pertence a outro cliente
    cliente_com_cpf = buscar_cliente_por_cpf(cpf)

    if cliente_com_cpf and cliente_com_cpf["id_cliente"] != id_cliente:
        return jsonify({
            "erro": "Este CPF já está cadastrado para outro cliente"
        }), 409

    atualizar_cliente(
        id_cliente,
        nome,
        cpf,
        telefone,
        email,
        endereco,
        aceite_lgpd
    )

    return jsonify({
        "mensagem": "Cliente alterado com sucesso"
    }), 200


# =========================================
# CANCELAR CLIENTE
# =========================================

@cliente_bp.route("/clientes/<int:id_cliente>", methods=["DELETE"])
def cancelar(id_cliente):

    cliente = buscar_cliente_por_id(id_cliente)

    if not cliente:
        return jsonify({
            "erro": "Cliente não encontrado"
        }), 404

    cancelar_cliente(id_cliente)

    return jsonify({
        "mensagem": "Cliente cancelado com sucesso"
    }), 200