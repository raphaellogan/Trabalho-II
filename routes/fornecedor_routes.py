from flask import Blueprint, request, jsonify


from models.fornecedor import (
    criar_fornecedor,
    listar_fornecedores,
    buscar_fornecedor_por_id,
    alterar_fornecedor,
    deletar_fornecedor
)


fornecedor_bp = Blueprint("fornecedor", __name__)


# CADASTRAR FORNECEDOR
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


# LISTAR FORNECEDORES
@fornecedor_bp.route("/fornecedores", methods=["GET"])
def listar():
    fornecedores = listar_fornecedores()

    return jsonify(fornecedores), 200

# BUSCAR FORNECEDOR POR ID
@fornecedor_bp.route("/fornecedores/<int:id_fornecedor>", methods=["GET"])
def buscar_por_id(id_fornecedor):

    fornecedor = buscar_fornecedor_por_id(id_fornecedor)

    if fornecedor is None:
        return jsonify({
            "erro": "Fornecedor não encontrado"
        }), 404

    return jsonify(fornecedor), 200

# ALTERAR FORNECEDOR
@fornecedor_bp.route("/fornecedores/<int:id_fornecedor>", methods=["PUT"])
def alterar(id_fornecedor):
    dados = request.get_json()

    nome = dados.get("nome")
    telefone = dados.get("telefone")
    email = dados.get("email")

    if not nome or not telefone or not email:
        return jsonify({
            "erro": "Nome, telefone e email são obrigatórios"
        }), 400

    linhas_afetadas = alterar_fornecedor(
        id_fornecedor,
        nome,
        telefone,
        email
    )

    if linhas_afetadas == 0:
        return jsonify({
            "erro": "Fornecedor não encontrado"
        }), 404

    return jsonify({
        "mensagem": "Fornecedor alterado com sucesso"
    }), 200

# DELETAR FORNECEDOR
@fornecedor_bp.route("/fornecedores/<int:id_fornecedor>", methods=["DELETE"])
def deletar(id_fornecedor):

    linhas_afetadas = deletar_fornecedor(id_fornecedor)

    if linhas_afetadas == 0:
        return jsonify({
            "erro": "Fornecedor não encontrado"
        }), 404

    return jsonify({
        "mensagem": "Fornecedor deletado com sucesso"
    }), 200