from flask import Blueprint, request, jsonify
from models.categoria import (
    criar_categoria,
    listar_categorias,
    buscar_categoria_por_id,
    buscar_categoria_por_nome,
    alterar_categoria,
    excluir_categoria
)

categoria_bp = Blueprint("categoria", __name__)


# ==========================================
# CADASTRAR CATEGORIA
# ==========================================
@categoria_bp.route("/categorias", methods=["POST"])
def cadastrar_categoria():
    dados = request.get_json()

    nome = dados.get("nome")
    descricao = dados.get("descricao")

    if not nome or not descricao:
        return jsonify({
            "erro": "Nome e descrição são obrigatórios"
        }), 400

    # VERIFICAR SE JÁ EXISTE
    categoria_existente = buscar_categoria_por_nome(nome)

    if categoria_existente:
        return jsonify({
            "erro": "Categoria já cadastrada"
        }), 409

    criar_categoria(nome, descricao)

    return jsonify({
        "mensagem": "Categoria cadastrada com sucesso"
    }), 201


# ==========================================
# LISTAR CATEGORIAS
# ==========================================
@categoria_bp.route("/categorias", methods=["GET"])
def listar():
    categorias = listar_categorias()

    return jsonify(categorias), 200


# ==========================================
# BUSCAR CATEGORIA POR ID
# ==========================================
@categoria_bp.route("/categorias/<int:id_categoria>", methods=["GET"])
def buscar_por_id(id_categoria):

    categoria = buscar_categoria_por_id(id_categoria)

    if categoria is None:
        return jsonify({
            "erro": "Categoria não encontrada"
        }), 404

    return jsonify(categoria), 200


# ==========================================
# ALTERAR CATEGORIA
# ==========================================
@categoria_bp.route("/categorias/<int:id_categoria>", methods=["PUT"])
def alterar(id_categoria):
    dados = request.get_json()

    nome = dados.get("nome")
    descricao = dados.get("descricao")

    if not nome or not descricao:
        return jsonify({
            "erro": "Nome e descrição são obrigatórios"
        }), 400

    resultado = alterar_categoria(
        id_categoria,
        nome,
        descricao
    )

    if resultado == 0:
        return jsonify({
            "erro": "Categoria não encontrada"
        }), 404

    return jsonify({
        "mensagem": "Categoria alterada com sucesso"
    }), 200


# ==========================================
# EXCLUIR CATEGORIA
# ==========================================
@categoria_bp.route("/categorias/<int:id_categoria>", methods=["DELETE"])
def excluir(id_categoria):

    resultado = excluir_categoria(id_categoria)

    if resultado == 0:
        return jsonify({
            "erro": "Categoria não encontrada"
        }), 404

    return jsonify({
        "mensagem": "Categoria deletada com sucesso"
    }), 200