from flask import Blueprint, request, jsonify
from Banco_motos.models.cliente import criar_cliente, listar_clientes, buscar_cliente_por_id

cliente_bp = Blueprint("cliente", __name__)


@cliente_bp.route("/clientes", methods=["POST"])
def cadastrar():
    dados = request.get_json()

    nome = dados.get("nome")
    cpf = dados.get("cpf")
    telefone = dados.get("telefone")
    email = dados.get("email")
    endereco = dados.get("endereco")
    aceite_lgpd = dados.get("aceite_lgpd")
    data_consentimento = dados.get("data_consentimento")

    if not nome or not cpf:
        return jsonify({
            "erro": "Nome e CPF são obrigatórios"
        }), 400

    criar_cliente(
        nome,
        cpf,
        telefone,
        email,
        endereco,
        aceite_lgpd,
        data_consentimento
    )

    return jsonify({
        "mensagem": "Cliente cadastrado com sucesso"
    }), 201


@cliente_bp.route("/clientes", methods=["GET"])
def listar():
    clientes = listar_clientes()

    return jsonify(clientes), 200

@cliente_bp.route("/clientes/<int:id_cliente>", methods=["GET"])
def buscar_por_id(id_cliente):
    cliente = buscar_cliente_por_id(id_cliente)

    if not cliente:
        return jsonify({
            "erro": "Cliente não encontrado"
        }), 404

    return jsonify(cliente), 200
