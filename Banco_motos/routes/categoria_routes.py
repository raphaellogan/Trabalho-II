from flask import Blueprint, request, jsonify
from Banco_motos.models.categoria import criar_categoria, listar_categorias

categoria_bp = Blueprint("categoria", __name__)


@categoria_bp.route("/categorias", methods=["POST"])
def cadastrar_categoria():
    dados = request.get_json()

    nome = dados.get("nome")
    descricao = dados.get("descricao")

    if not nome or not descricao:
        return jsonify({
            "erro": "Nome e descrição são obrigatórios"
        }), 400

    criar_categoria(nome, descricao)

    return jsonify({
        "mensagem": "Categoria cadastrada com sucesso"
    }), 201


@categoria_bp.route("/categorias", methods=["GET"])
def listar():
    categorias = listar_categorias()

    return jsonify(categorias)