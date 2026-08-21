from config.db import conectar


# ==========================================
# CADASTRAR PRODUTO
# ==========================================
def cadastrar_produto(
    nome,
    descricao,
    preco,
    estoque,
    id_categoria,
    id_fornecedor,
    cor,
    tamanho,
    codigo_de_barra
):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO produto
        (
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
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    valores = (
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

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()


# ==========================================
# LISTAR TODOS OS PRODUTOS
# ==========================================
def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM produto")

    produtos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return produtos


# ==========================================
# BUSCAR PRODUTO POR ID
# ==========================================
def buscar_produto(id_produto):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT *
        FROM produto
        WHERE id_produto = %s
    """

    cursor.execute(sql, (id_produto,))

    produto = cursor.fetchone()

    cursor.close()
    conexao.close()

    return produto


# ==========================================
# ALTERAR PRODUTO
# ==========================================
def alterar_produto(id_produto, dados):
    conexao = conectar()
    cursor = conexao.cursor()

    campos_permitidos = [
        "nome",
        "descricao",
        "preco",
        "estoque",
        "id_categoria",
        "id_fornecedor",
        "cor",
        "tamanho",
        "codigo_de_barra"
    ]

    campos = []
    valores = []

    for campo in campos_permitidos:
        if campo in dados:
            campos.append(f"{campo} = %s")
            valores.append(dados[campo])

    if not campos:
        cursor.close()
        conexao.close()
        return 0

    sql = f"""
        UPDATE produto
        SET {", ".join(campos)}
        WHERE id_produto = %s
    """

    valores.append(id_produto)

    cursor.execute(sql, valores)

    linhas_afetadas = cursor.rowcount

    conexao.commit()

    cursor.close()
    conexao.close()

    return linhas_afetadas


# ==========================================
# DELETAR PRODUTO
# ==========================================
def deletar_produto(id_produto):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        DELETE FROM produto
        WHERE id_produto = %s
    """

    cursor.execute(sql, (id_produto,))

    linhas_afetadas = cursor.rowcount

    conexao.commit()

    cursor.close()
    conexao.close()

    return linhas_afetadas