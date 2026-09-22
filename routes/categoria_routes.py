from flask import Blueprint, request, jsonify

from models.categoria import (
    criar_categoria,
    listar_categorias,
    buscar_categoria_por_id,
    alterar_categoria,
    excluir_categoria
)

categoria_bp = Blueprint("categoria", __name__)


@categoria_bp.route("/categorias", methods=["POST"])
def cadastrar_categoria():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Dados da categoria não foram enviados"}), 400

    nome = dados.get("nome")
    descricao = dados.get("descricao")

    if not nome or not descricao:
        return jsonify({"erro": "Nome e descrição são obrigatórios"}), 400

    criar_categoria(nome, descricao)

    return jsonify({"mensagem": "Categoria cadastrada com sucesso"}), 201


@categoria_bp.route("/categorias", methods=["GET"])
def listar():
    categorias = listar_categorias()
    return jsonify(categorias), 200


@categoria_bp.route("/categorias/<int:id_categoria>", methods=["GET"])
def buscar(id_categoria):
    categoria = buscar_categoria_por_id(id_categoria)

    if categoria is None:
        return jsonify({"erro": "Categoria não encontrada"}), 404

    return jsonify(categoria), 200


@categoria_bp.route("/categorias/<int:id_categoria>", methods=["PUT"])
def alterar(id_categoria):
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Dados da categoria não foram enviados"}), 400

    resultado = alterar_categoria(id_categoria, dados)

    if resultado == 0:
        return jsonify({"erro": "Categoria não encontrada ou nenhum campo foi alterado"}), 404

    return jsonify({"mensagem": "Categoria alterada com sucesso"}), 200


@categoria_bp.route("/categorias/<int:id_categoria>", methods=["DELETE"])
def excluir(id_categoria):
    resultado = excluir_categoria(id_categoria)

    if resultado == 0:
        return jsonify({"erro": "Categoria não encontrada"}), 404

    return jsonify({"mensagem": "Categoria removida com sucesso"}), 200