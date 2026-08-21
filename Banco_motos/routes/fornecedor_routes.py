from flask import Blueprint, request, jsonify
from Banco_motos.models.fornecedor import criar_fornecedor, listar_fornecedores

fornecedor_bp = Blueprint("fornecedor", __name__)


@fornecedor_bp.route("/fornecedores", methods=["POST"])
def cadastrar():
    dados = request.get_json()

    nome = dados.get("nome")
    cnpj = dados.get("cnpj")
    telefone = dados.get("telefone")
    email = dados.get("email")

    if not nome or not cnpj:
        return jsonify({
            "erro": "Nome e CNPJ são obrigatórios"
        }), 400

    criar_fornecedor(nome, cnpj, telefone, email)

    return jsonify({
        "mensagem": "Fornecedor cadastrado com sucesso"
    }), 201


@fornecedor_bp.route("/fornecedores", methods=["GET"])
def listar():
    fornecedores = listar_fornecedores()

    return jsonify(fornecedores)