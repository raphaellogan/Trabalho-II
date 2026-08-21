from flask import Blueprint, request, jsonify
import json

from models.produto import (
    cadastrar_produto,
    listar_produtos,
    buscar_produto,
    alterar_produto,
    deletar_produto
)


# ==========================================
# BLUEPRINT PRODUTO
# ==========================================
produto_bp = Blueprint("produto", __name__)


# ==========================================
# CADASTRAR PRODUTO
# ==========================================
@produto_bp.route("/produtos", methods=["POST"])
def cadastrar():

    dados = request.get_json(silent=True)

    print("DADOS RECEBIDOS:", dados)
    print("TIPO DOS DADOS:", type(dados))

    # ==========================================
    # CONVERTER STRING JSON PARA DICIONÁRIO
    # ==========================================
    if isinstance(dados, str):
        try:
            dados = json.loads(dados)
        except json.JSONDecodeError:
            return jsonify({
                "erro": "JSON inválido"
            }), 400

    # ==========================================
    # VALIDAR FORMATO
    # ==========================================
    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Os dados enviados devem estar no formato JSON"
        }), 400

    # ==========================================
    # PEGAR DADOS DO PRODUTO
    # ==========================================
    nome = dados.get("nome")
    descricao = dados.get("descricao")
    preco = dados.get("preco")
    estoque = dados.get("estoque", 0)
    id_categoria = dados.get("id_categoria")
    id_fornecedor = dados.get("id_fornecedor")
    cor = dados.get("cor")
    tamanho = dados.get("tamanho")
    codigo_de_barra = dados.get("codigo_de_barra")

    # ==========================================
    # VALIDAR CAMPOS OBRIGATÓRIOS
    # ==========================================
    if not nome or preco is None or estoque is None:
        return jsonify({
            "erro": "Nome, preço e estoque são obrigatórios"
        }), 400

    # ==========================================
    # CADASTRAR NO BANCO
    # ==========================================
    cadastrar_produto(
        nome,
        descricao,
        preco,
        estoque,
        id_categoria,
        id_fornecedor,
        cor,
        tamanho,
        codigo_de_barra
    )

    return jsonify({
        "mensagem": "Produto cadastrado com sucesso"
    }), 201


# ==========================================
# LISTAR TODOS OS PRODUTOS
# ==========================================
@produto_bp.route("/produtos", methods=["GET"])
def listar():

    produtos = listar_produtos()

    return jsonify(produtos), 200


# ==========================================
# BUSCAR PRODUTO POR ID
# ==========================================
@produto_bp.route("/produtos/<int:id_produto>", methods=["GET"])
def buscar(id_produto):

    produto = buscar_produto(id_produto)

    if produto is None:
        return jsonify({
            "erro": "Produto não encontrado"
        }), 404

    return jsonify(produto), 200


# ==========================================
# ALTERAR PRODUTO
# ==========================================
@produto_bp.route("/produtos/<int:id_produto>", methods=["PUT"])
def alterar(id_produto):

    dados = request.get_json(silent=True)

    print("DADOS RECEBIDOS PARA ALTERAÇÃO:", dados)
    print("TIPO DOS DADOS:", type(dados))

    # ==========================================
    # CONVERTER STRING JSON PARA DICIONÁRIO
    # ==========================================
    if isinstance(dados, str):
        try:
            dados = json.loads(dados)
        except json.JSONDecodeError:
            return jsonify({
                "erro": "JSON inválido"
            }), 400

    # ==========================================
    # VALIDAR FORMATO
    # ==========================================
    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Os dados enviados devem estar no formato JSON"
        }), 400

    # ==========================================
    # ALTERAR PRODUTO
    # ==========================================
    linhas_afetadas = alterar_produto(
        id_produto,
        dados
    )

    if linhas_afetadas == 0:
        return jsonify({
            "erro": "Produto não encontrado ou nenhum campo foi alterado"
        }), 404

    return jsonify({
        "mensagem": "Produto alterado com sucesso"
    }), 200


# ==========================================
# DELETAR PRODUTO
# ==========================================
@produto_bp.route("/produtos/<int:id_produto>", methods=["DELETE"])
def deletar(id_produto):

    linhas_afetadas = deletar_produto(id_produto)

    if linhas_afetadas == 0:
        return jsonify({
            "erro": "Produto não encontrado"
        }), 404

    return jsonify({
        "mensagem": "Produto deletado com sucesso"
    }), 200